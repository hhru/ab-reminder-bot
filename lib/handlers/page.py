import json

import bot_settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.slack import SlackClient
from lib.templates import SLACK_PAGE_MESSAGE_TEMPLATE, TITLE_TEMPLATE, PAGE_TEMPLATE, USER_ROW_TEMPLATE, \
    TEAM_ROW_TEMPLATE
from lib.utils import get_usable_date

def generate_page(date):
    confluence = ConfluenceClient(
        bot_settings.confluence_settings['login'],
        bot_settings.confluence_settings['password']
    )
    slack = SlackClient()

    with open('users.json', 'r') as file:
        teams_users = json.loads(file.read())
        file.close()

    rows = ''
    task_id = 1

    for team in teams_users:
        if bot_settings.confluence_settings['add_team_header']:
            rows += TEAM_ROW_TEMPLATE.format(name=team['name'])
        for user in team['users']:
            rows += USER_ROW_TEMPLATE.format(task_id=task_id, user_key=user['userKey'])
            task_id += 1

    page = PAGE_TEMPLATE.format(date=date, rows=rows)

    result = confluence.post_page(
        TITLE_TEMPLATE.format(date=date),
        page,
        bot_settings.confluence_settings['space_key'],
        bot_settings.confluence_settings['parent_page']
    )

    page_url = 'https://{host}{url}'.format(
        host=bot_settings.confluence_settings['wiki_base_url'],
        url=result['_links']['webui']
    )

    slack.post_message(SLACK_PAGE_MESSAGE_TEMPLATE.format(
        date=date,
        url=page_url
    ))
