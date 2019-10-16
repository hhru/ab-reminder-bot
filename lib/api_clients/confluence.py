import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

import bot_settings

logger = bot_settings.logging.getLogger(__name__)


class ConfluenceClient:
    def __init__(self, login, password):
        self.auth = requests.auth.HTTPBasicAuth(login, password)

    def get_users(self):
        return self.get(
            bot_settings.confluence_settings['jira_base_url'],
            '/rest/jirastat/1.0/team/list'
        )

    def get_user_info(self, user_name):
        return self.get(
            bot_settings.confluence_settings['wiki_base_url'],
            '/rest/api/user?username={user_name}'.format(user_name=user_name)
        )

    def get_page(self, space_key, title, expand=('body.storage',)):
        return self.get(
            bot_settings.confluence_settings['wiki_base_url'],
            '/rest/api/content/?spaceKey={space_key}&title={title}&expand={expand}'.format(
                space_key=quote(space_key),
                title=quote(title),
                expand=','.join(expand)
            )
        )

    def post_page(self, title, content, space_key, parent_id=None):
        return self.post(
            bot_settings.confluence_settings['wiki_base_url'],
            '/rest/api/content/',
            {
                'type': 'page',
                'title': title,
                'space': {
                    'key': space_key,
                },
                'ancestors': [{'id': int(parent_id)}],
                'body': {
                    'storage': {
                        'value': content,
                        'representation': 'storage',
                    }
                }
            },
        )

    def get(self, host, url):
        full_url = 'https://{host}{url}'.format(host=host, url=url)
        response = requests.get(
            full_url,
            auth=self.auth,
            timeout=(
                bot_settings.connection_connect_timeout_s,
                bot_settings.connection_read_timeout_s
            ),
            verify=False
        )

        if response.status_code != 200:
            raise Exception('{url} {status}: {content}'.format(
                url=full_url,
                status=response.status_code,
                content=response.content
            ))

        return response.json()

    def post(self, host, url, json_data):
        full_url = 'https://{host}{url}'.format(host=host, url=url)
        response = requests.post(
            full_url,
            None,
            json_data,
            auth=self.auth,
            timeout=(
                bot_settings.connection_connect_timeout_s,
                bot_settings.connection_read_timeout_s
            ),
            verify=False
        )

        if response.status_code != 200:
            raise Exception('{url} {status}: {content}'.format(
                url=full_url,
                status=response.status_code,
                content=response.content
            ))

        return response.json()
