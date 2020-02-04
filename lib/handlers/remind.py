import json

from bs4 import BeautifulSoup

import bot_settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.slack import SlackClient
from lib.templates import TITLE_TEMPLATE, SLACK_REMIND_MESSAGE_TEMPLATE, SLACK_REMIND_ALL_CHECKED_TEMPLATE, \
    SLACK_REMIND_HAS_UNCHECKED_TEMPLATE


def remind_users(date):
    confluence = ConfluenceClient(
        bot_settings.confluence_settings['login'],
        bot_settings.confluence_settings['password']
    )
    slack = SlackClient()

    result = confluence.get_page(
        bot_settings.confluence_settings['space_key'],
        TITLE_TEMPLATE.format(date=date)
    )

    if result['size'] == 0:
        raise Exception('Page not found')

    if result['size'] > 1:
        raise Exception('Page ambiguous')

    page_content = result['results'][0]['body']
    page_url = 'https://{host}{url}'.format(
        host=bot_settings.confluence_settings['wiki_base_url'],
        url=result['results'][0]['_links']['webui']
    )

    soup = BeautifulSoup('<html>{content}</html>'.format(content=page_content), 'html.parser')

    users_to_remind_keys = []

    for task in soup.find_all('ac:task'):
        task_status = task.find('ac:task-status').get_text()
        if task_status != 'complete':
            users_to_remind_keys.append(task.find('ri:user')['ri:userkey'])

    if len(users_to_remind_keys) > 0:
        with open('users.json', 'r') as file:
            teams_users = json.loads(file.read())
            file.close()

        users_to_remind = []

        for team in teams_users:
            for user in team['users']:
                if user['userKey'] in users_to_remind_keys:
                    users_to_remind.append(user)

        slack_users_list = slack.get_users_list()
        slack_email_to_name_map = {}

        for slack_member in slack_users_list['members']:
            if 'email' in slack_member['profile'] and slack_member['profile']['email'] != '':
                slack_email_to_name_map.update({slack_member['profile']['email']: slack_member['name']})

        users_to_remind_slack = []
        for user in users_to_remind:
            if user['userName'] in bot_settings.slack_settings['email_override']:
                corporate_email = bot_settings.slack_settings['email_override'][user['userName']]
            else:
                corporate_email = '{user_name}@hh.ru'.format(user_name=user['userName'])
            if corporate_email in slack_email_to_name_map:
                users_to_remind_slack.append(
                    '<@{slack_username}>'.format(slack_username=slack_email_to_name_map[corporate_email])
                )
            else:
                bot_settings.logging.warning(
                    'Not found slack name for confluence user {confluence_username}'.format(
                        confluence_username=user['userName']
                    )
                )
                users_to_remind_slack.append(user['displayName'])

        remind_condition = SLACK_REMIND_HAS_UNCHECKED_TEMPLATE.format(users=', '.join(users_to_remind_slack))
    else:
        remind_condition = SLACK_REMIND_ALL_CHECKED_TEMPLATE

    slack.post_message(SLACK_REMIND_MESSAGE_TEMPLATE.format(
        remind_condition=remind_condition,
        url=page_url,
    ))
