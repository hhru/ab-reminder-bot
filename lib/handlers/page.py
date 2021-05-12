import json

import bot_settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.slack import SlackClient
from lib.templates import SLACK_PAGE_MESSAGE_TEMPLATE, TITLE_TEMPLATE, PAGE_TEMPLATE, USER_ROW_TEMPLATE, \
    TEAM_ROW_TEMPLATE
from lib.utils import get_usable_date
from lib.cache_storage import Storage
from lib.constants import PageUpdateStates, CHECKED_MESSAGE_REACTION


def generate_page(params_date=None):
    date = get_usable_date(params_date, bot_settings.defaults)
    state_storage = Storage('state')
    if 'processed_messages' in state_storage:
        del state_storage['processed_messages']
    state_storage['state'] = PageUpdateStates.GATHERING

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

    if bot_settings.labels:
        page_id = result['id']
        confluence.add_labels(page_id, bot_settings.labels)

    page_url = 'https://{host}{url}'.format(
        host=bot_settings.confluence_settings['wiki_base_url'],
        url=result['_links']['webui']
    )

    slack.post_channel_message(SLACK_PAGE_MESSAGE_TEMPLATE.format(
        checked_message_reaction=CHECKED_MESSAGE_REACTION,
        date=date,
        url=page_url
    ))
