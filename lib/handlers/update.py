from datetime import datetime

from bs4 import BeautifulSoup

import bot_settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.slack import SlackClient
from lib.templates import TITLE_TEMPLATE, SLACK_PAGE_MESSAGE_TEMPLATE, SLACK_STALE_THREAD_MESSAGE
from lib.utils import get_confluence_user_key_by_slack_user, get_confluence_page, get_message_html
from lib.cache_storage import Storage
from lib.constants import PageUpdateStates, BOT_PROCESSED_REACTION, CHECKED_MESSAGE_REACTION


TWO_DAYS_SECONDS = 2 * 24 * 60 * 60

logger = bot_settings.logging.getLogger(__name__)


def has_check_mark(message):
    message_author = message['user']
    if 'reactions' not in message:
        return False

    for reaction in message['reactions']:
        if reaction['name'] == CHECKED_MESSAGE_REACTION and message_author in reaction['users']:
            return True

    return False


def get_last_message_update(message):
    if 'edited' in message:
        return message['edited']['ts']

    return message['ts']


def get_current_messages(slack):
    last_bot_message = slack.get_last_bot_message()
    replies = slack.get_replies(last_bot_message)
    users = slack.get_users_id_mapping()

    replies = filter(
        lambda item: not('bot_id' in item and item['bot_id'] == slack.bot_id()) and has_check_mark(item),
        replies
    )

    current_messages = {}

    max_last_update = 0
    for message in replies:
        last_update = get_last_message_update(message)
        if float(last_update) > float(max_last_update):
            max_last_update = last_update

        user_key = get_confluence_user_key_by_slack_user(users[message['user']])

        if user_key not in current_messages:
            current_messages[user_key] = []

        current_messages[user_key].append({
            'text': message['text'],
            'ts': message['ts'],
            'last_update': last_update,
        })

    return current_messages, last_bot_message, max_last_update


def needs_processing(user_key, current_messages, processed_messages):
    if user_key not in processed_messages:
        return True

    current_updates = sorted([message['last_update'] for message in current_messages[user_key]])
    processed_updates = sorted([message['last_update'] for message in processed_messages[user_key]])

    return current_updates != processed_updates


def update_state():
    slack = SlackClient()
    confluence = ConfluenceClient(
        bot_settings.confluence_settings['login'],
        bot_settings.confluence_settings['password']
    )
    storage = Storage('state')

    current_state = storage.get('state', PageUpdateStates.IDLE)
    if current_state == PageUpdateStates.IDLE:
        logger.info('Nothing to update, state is idle, exiting')
        return

    page_date = storage.get('date', bot_settings.defaults['date'])

    processed_messages = storage['processed_messages']

    current_messages, last_bot_message, last_updated = get_current_messages(slack)

    page = get_confluence_page(confluence, TITLE_TEMPLATE.format(date=page_date))

    soup = BeautifulSoup(page['content'], 'html.parser')

    page_need_update = False
    for task in soup.find_all('ac:task'):
        user_key = task.find('ri:user')['ri:userkey']
        if user_key in current_messages and needs_processing(user_key, current_messages, processed_messages):
            page_need_update = True
            task_cell = task.find_parent('tr').find_all('td')[1]
            new_cell = soup.new_tag('td')
            for message in current_messages[user_key]:
                html = get_message_html(message['text'])
                new_cell.append(BeautifulSoup(html, 'html.parser'))

            task_cell.replace_with(new_cell)
            task.find('ac:task-status').string.replace_with('complete')

    if page_need_update:
        page.update({
            'version_number': page['version_number'] + 1,
            'content': str(soup),
        })

        confluence.update_page(page)

        processed_messages.update(current_messages)
        storage['processed_messages'] = processed_messages

        for user_key in current_messages:
            for message in current_messages[user_key]:
                slack.react_to_message(BOT_PROCESSED_REACTION, message)

    if int(last_updated.split('.')[0]) < int(datetime.now().timestamp()) - TWO_DAYS_SECONDS:
        storage['state'] = PageUpdateStates.IDLE
        slack.update_message(
            SLACK_PAGE_MESSAGE_TEMPLATE.format(
                thread_messages_text=SLACK_STALE_THREAD_MESSAGE,
                date=page_date,
                url=page['url']
            ),
            message_ts=last_bot_message['ts']
        )
