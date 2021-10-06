import json

from bs4 import BeautifulSoup

import settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.slack import SlackClient
from lib.templates import TITLE_TEMPLATE, SLACK_REMIND_MESSAGE_TEMPLATE, SLACK_REMIND_ALL_CHECKED_TEMPLATE, \
    SLACK_REMIND_PRIVATE_MESSAGE
from lib.utils import get_usable_date, get_confluence_page


def remind_users(params_date=None):
    date = get_usable_date(params_date, settings.defaults)

    confluence = ConfluenceClient(
        settings.confluence_settings['wiki_username'],
        settings.confluence_settings['wiki_password']
    )
    slack = SlackClient()

    page = get_confluence_page(confluence, TITLE_TEMPLATE.format(date=date))

    soup = BeautifulSoup(page['content'], 'html.parser')

    users_to_remind_keys = []

    for task in soup.find_all('ac:task'):
        task_status = task.find('ac:task-status').get_text()
        if task_status != 'complete':
            users_to_remind_keys.append(task.find('ri:user')['ri:userkey'])

    if len(users_to_remind_keys) > 0:
        with open('./cache/users.json', 'r') as file:
            teams_users = json.loads(file.read())
            file.close()

        users_to_remind = []

        for team in teams_users:
            for user in team['users']:
                if user['userKey'] in users_to_remind_keys:
                    users_to_remind.append(user)

        slack_users_map = slack.get_users_email_mapping()
        last_bot_message_link = slack.get_message_link(slack.get_last_bot_message())
        for user in users_to_remind:
            if user['userName'] in settings.slack_settings['email_override']:
                corporate_email = settings.slack_settings['email_override'][user['userName']]
            else:
                corporate_email = '{user_name}@hh.ru'.format(user_name=user['userName'])
            if corporate_email in slack_users_map:
                slack.post_private_message(
                    corporate_email,
                    SLACK_REMIND_PRIVATE_MESSAGE.format(message_link=last_bot_message_link)
                )
            else:
                settings.logging.warning(
                    'Not found slack name for confluence user {confluence_username}'.format(
                        confluence_username=user['userName']
                    )
                )
    else:
        slack.post_channel_message(SLACK_REMIND_MESSAGE_TEMPLATE.format(
            remind_condition=SLACK_REMIND_ALL_CHECKED_TEMPLATE,
            url=page['url'],
        ))
