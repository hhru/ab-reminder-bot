import logging

import requests

import settings

logger = settings.logging.getLogger(__name__)


class NogaClient:
    def __init__(self):
        self.url = settings.slack_settings['url']
        self.channel_name = settings.slack_settings['channel']

    def send_message(self, message, to=None):
        json_data = {
            "name": "AB Reminder",
            "text": message,
            "channel": self.channel_name if to is None else to
        }

        response = requests.post(
            f'{self.url}',
            json=json_data,
            timeout=(
                settings.connection_connect_timeout_s,
                settings.connection_read_timeout_s
            ),
        )

        if response.status_code != 200:
            reason = ''
            try:
                reason = response.json()['error']
            except Exception as ignored:
                pass
            logging.warning(f'Error sending message to {to}: {reason}')
