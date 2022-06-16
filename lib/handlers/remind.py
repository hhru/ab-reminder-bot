import json
import logging

from bs4 import BeautifulSoup

import settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.noga import NogaClient
from lib.templates import TITLE_TEMPLATE, SLACK_REMIND_PRIVATE_MESSAGE
from lib.utils import get_usable_date, get_confluence_page


def remind_users(params_date=None):
    date = get_usable_date(params_date, settings.defaults)

    confluence = ConfluenceClient(
        settings.confluence_settings['wiki_username'],
        settings.confluence_settings['wiki_password']
    )
    noga = NogaClient()

    page = get_confluence_page(confluence, TITLE_TEMPLATE.format(date=date))

    soup = BeautifulSoup(page['content'], 'html.parser')

    users_to_remind_keys = []

    for task in soup.find_all('ac:task'):
        task_status = task.find('ac:task-status').get_text()
        if task_status != 'complete':
            users_to_remind_keys.append(task.find('ri:user')['ri:userkey'])

    if len(users_to_remind_keys) > 0:
        with open('./cache/users.json', 'r', encoding='UTF-8') as file:
            teams_users = json.loads(file.read())
            file.close()

        users_to_remind = []

        for team in teams_users:
            for user in team['users']:
                if user['userKey'] in users_to_remind_keys:
                    users_to_remind.append(user)

        for user in users_to_remind:
            to = user['email'] or user['messenger']
            if to is not None:
                noga.send_message(
                    to=to,
                    message=SLACK_REMIND_PRIVATE_MESSAGE.format(message_link=page['url'])
                )
            else:
                logging.error('Error sending message to %s: no contacts available', user['displayName'])
