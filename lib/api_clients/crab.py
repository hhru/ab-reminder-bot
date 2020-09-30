import requests

import bot_settings

logger = bot_settings.logging.getLogger(__name__)


class CrabClient:
    def get_users(self):
        return self.get(bot_settings.crab_settings['crab_base_url'], '/users')

    @staticmethod
    def get(host, url):
        full_url = 'https://{host}{url}'.format(host=host, url=url)
        response = requests.get(
            full_url,
            headers={'Content-Type': 'application/json'},
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
