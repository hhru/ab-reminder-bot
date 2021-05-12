import json
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

import bot_settings
from lib.constants import ApiOperationException

logger = bot_settings.logging.getLogger(__name__)


class ConfluenceClient:
    def __init__(self, login, password):
        self.auth = requests.auth.HTTPBasicAuth(login, password)

    def get_users(self):
        return self.api_get(
            bot_settings.confluence_settings['jira_base_url'],
            '/rest/jirastat/1.0/team/list'
        )

    def get_user_info(self, user_name):
        return self.api_get(
            bot_settings.confluence_settings['wiki_base_url'],
            '/rest/api/user?username={user_name}'.format(user_name=user_name)
        )

    def get_page(self, space_key, title, expand=('body.storage', 'version', 'space')):
        return self.api_get(
            bot_settings.confluence_settings['wiki_base_url'],
            '/rest/api/content/?spaceKey={space_key}&title={title}&expand={expand}'.format(
                space_key=quote(space_key),
                title=quote(title),
                expand=','.join(expand)
            )
        )

    def post_page(self, title, content, space_key, parent_id=None):
        return self.api_post(
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

    def update_page(self, page):
        return self.api_put(
            bot_settings.confluence_settings['wiki_base_url'],
            f'/rest/api/content/{page["id"]}',
            {
                'id': page['id'],
                'title': page['title'],
                'space': {
                    'key': page['space_key'],
                },
                'type': 'page',
                'body': {
                    'storage': {
                        'value': page['content'],
                        'representation': 'storage',
                    }
                },
                'version': {
                    'number': page['version_number'],
                }
            }
        )

    def add_labels(self, page_id, labels):
        json_labels = list(map(lambda label: {"name": '{label_name}'.format(label_name=label)}, labels))
        return self.api_post(
            bot_settings.confluence_settings['wiki_base_url'],
            '/rest/api/content/{page_id}/label'.format(page_id=page_id),
            json_labels
        )

    def api_get(self, host, url):
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
            raise ApiOperationException(f'{full_url} {response.status_code}: {response.content}')

        return response.json()

    def api_post(self, host, url, json_data):
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
            raise ApiOperationException(f'{full_url} {response.status_code}: {response.content}')

        return response.json()

    def api_put(self, host, url, json_data):
        full_url = 'https://{host}{url}'.format(host=host, url=url)
        response = requests.put(
            full_url,
            json.dumps(json_data),
            auth=self.auth,
            headers={
                'Content-type': 'application/json',
            },
            timeout=(
                bot_settings.connection_connect_timeout_s,
                bot_settings.connection_read_timeout_s
            ),
            verify=False
        )

        if response.status_code != 200:
            raise ApiOperationException(f'{full_url} {response.status_code}: {response.content}')

        return response.json()
