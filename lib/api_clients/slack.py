from datetime import datetime
import requests

import bot_settings
from lib.cache_storage import Storage
from lib.constants import ApiOperationException

logger = bot_settings.logging.getLogger(__name__)


def get_two_week_from_now_ts():
    return int(datetime.now().timestamp()) - (2 * 7 * 24 * 60 * 60)  # две недели назад


def get_response_json(response):
    if response.status_code != 200:
        raise ApiOperationException(response.content)

    json = response.json()
    if not json['ok']:
        raise ApiOperationException(json['error'])

    return json


class SlackClient:
    def __init__(self):
        self.url = bot_settings.slack_settings['slack_api_url']
        self.token = bot_settings.slack_settings['oauth_token']
        self.channel_name = bot_settings.slack_settings['channel']
        self.storage = Storage('slack')
        self.__cached_users = []

    def bot_id(self):
        if 'bot_id' not in self.storage:
            self.storage['bot_id'] = self.api_get('auth.test')['bot_id']

        return self.storage['bot_id']

    def join_channel(self, channel):
        if not channel['is_member']:
            self.api_post('conversations.join', {'channel': channel['id']})
            channel.update({'is_member': True})

        cached_channels = self.storage.get('channels', {})
        cached_channels.update({
            self.channel_name: channel
        })

        self.storage['channels'] = cached_channels
        return channel['id']

    def get_channel_id(self):
        cached_channels = self.storage.get('channels', {})
        if self.channel_name in cached_channels:
            return cached_channels[self.channel_name]['id']

        cursor = ''
        while True:
            json_data = self.api_get('conversations.list', {'cursor': cursor, 'exclude_archived': True})

            for channel in json_data['channels']:
                if channel['name'] == self.channel_name:
                    return self.join_channel(channel)
            cursor = json_data['response_metadata']['next_cursor']

            if not cursor:
                break

    def get_users_list(self):
        if len(self.__cached_users) == 0:
            cursor = ''
            slack_members = []
            while True:
                json_data = self.api_get('users.list', {'cursor': cursor})

                slack_members += json_data['members']
                cursor = json_data['response_metadata']['next_cursor']

                if not cursor:
                    break

            self.__cached_users = slack_members

        return self.__cached_users

    def get_replies(self, message, channel=None):
        channel = self.get_channel_id() if channel is None else channel

        cursor = ''
        replies = []
        while True:
            next_page = self.api_get(
                'conversations.replies',
                {'channel': channel, 'ts': message['ts'], 'cursor': cursor}
            )

            replies += next_page['messages']

            cursor = next_page['response_metadata']['next_cursor'] if next_page['has_more'] else False

            if not cursor:
                break

        return replies

    def get_users_email_mapping(self):
        users = self.get_users_list()
        mapping = {}

        for user in users:
            if 'email' in user['profile'] and user['profile']['email'] != '':
                mapping.update({user['profile']['email']: {
                    'id': user['id'],
                    'name': user['name']
                }})

        return mapping

    def get_users_id_mapping(self):
        users = self.get_users_list()
        mapping = {}

        for user in users:
            if 'email' in user['profile'] and user['profile']['email'] != '':
                mapping.update({user['id']: {
                    'email': user['profile']['email'],
                    'name': user['name']
                }})

        return mapping

    def get_message_link(self, message, channel=None):
        channel = self.get_channel_id() if channel is None else channel
        ts = ''.join(message['ts'].split('.'))

        return f'https://hhru.slack.com/archives/{channel}/p{ts}'

    def get_last_bot_message(self, channel=None):
        channel = self.get_channel_id() if channel is None else channel
        cursor = ''
        while True:
            json_data = self.api_get(
                'conversations.history',
                {
                    'channel': channel,
                    'oldest': get_two_week_from_now_ts(),
                    'cursor': cursor,
                }
            )

            for message in json_data['messages']:
                if 'bot_id' in message and message['bot_id'] == self.bot_id():
                    return message

            cursor = json_data['response_metadata']['next_cursor'] if json_data['has_more'] else False
            if not cursor:
                break

        return None

    def post_private_message(self, user_email, message):
        if user_email not in self.storage['im_channels']:
            users = self.get_users_email_mapping()
            if user_email not in users:
                raise KeyError

            create_im_response = self.api_post(
                'conversations.open',
                {'users': [users[user_email]['id']]}
            )

            current_channels = self.storage['im_channels']
            current_channels.update({
                user_email: create_im_response['channel']['id']
            })

            self.storage['im_channels'] = current_channels

        self.post_channel_message(message, self.storage['im_channels'][user_email])

    def react_to_message(self, reaction, message, channel=None):
        channel = self.get_channel_id() if channel is None else channel
        try:
            self.api_post('reactions.add', {'timestamp': message['ts'], 'channel': channel, 'name': reaction})
        except ApiOperationException as exception:
            if str(exception) == 'already_reacted':
                pass

    def post_channel_message(self, message, channel=None, thread_ts=None):
        channel = self.get_channel_id() if channel is None else channel
        params = {'text': message, 'channel': channel}
        if thread_ts is not None:
            params.update({
                'thread_ts': thread_ts
            })

        response = self.api_post('chat.postMessage', params)
        return response['message']

    def api_get(self, endpoint, params=None):
        response = requests.get(
            f'{self.url}/{endpoint}',
            params,
            headers={
                'Authorization': f'Bearer {self.token}',
            },
            timeout=(
                bot_settings.connection_connect_timeout_s,
                bot_settings.connection_read_timeout_s
            )
        )

        return get_response_json(response)

    def api_post(self, endpoint, json_data):
        response = requests.post(
            f'{self.url}/{endpoint}',
            None,
            json_data,
            headers={
                'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}',
            },
            timeout=(
                bot_settings.connection_connect_timeout_s,
                bot_settings.connection_read_timeout_s
            ),
        )

        return get_response_json(response)
