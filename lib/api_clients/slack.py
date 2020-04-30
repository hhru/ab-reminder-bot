import requests

import bot_settings

logger = bot_settings.logging.getLogger(__name__)


class SlackClient:
    def get_users_list(self):
        cursor = ''
        slack_members = []
        while True:
            response = requests.get(
                'https://{host}/api/users.list'.format(host=bot_settings.slack_settings['slack_hook_url']),
                {
                    'token': bot_settings.slack_settings['oauth_token'],
                    'cursor': cursor,
                }
            )

            if response.status_code != 200:
                raise Exception(response.content)

            json_data = response.json()
            slack_members += json_data['members']
            cursor = json_data['response_metadata']['next_cursor']

            if not cursor:
                break

        return slack_members

    def post_message(self, message):
        return self.post(
            bot_settings.slack_settings['slack_hook_url'],
            bot_settings.slack_settings['channel_hook'],
            {'text': message},
        )

    def post(self, host, url, json_data):
        response = requests.post(
            'https://{host}{url}'.format(host=host, url=url),
            None,
            json_data,
            headers={
                'Content-type': 'application/json'
            },
            timeout=(
                bot_settings.connection_connect_timeout_s,
                bot_settings.connection_read_timeout_s
            ),
            verify=False
        )

        if response.status_code != 200:
            raise Exception(response.content)

        return True
