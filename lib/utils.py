import bot_settings
import datetime
import json
import os
import re
import uuid

from markdown import markdown


def get_confluence_page(confluence, search):
    result = confluence.get_page(bot_settings.confluence_settings['space_key'], search)

    if result['size'] == 0:
        raise Exception(f'Page not found, searched for {search}')

    if result['size'] > 1:
        raise Exception(f'Page ambiguous, searched for {search}')

    page_content = result['results'][0]['body']['storage']['value']
    page_url = 'https://{host}{url}'.format(
        host=bot_settings.confluence_settings['wiki_base_url'],
        url=result['results'][0]['_links']['webui']
    )

    return {
        'id': result['results'][0]['id'],
        'space_key': result['results'][0]['space']['key'],
        'title': result['results'][0]['title'],
        'content': page_content,
        'url': page_url,
        'version_number': result['results'][0]['version']['number'],
    }


def get_message_html(message_text):
    def postprocess(html):
        # Вики так умеет сама только в интерфейсе
        def replacer(match):
            return (
                f'<ac:structured-macro ac:macro-id="{uuid.uuid4()}" ac:name="jira" ac:schema-version="1">'
                u'<ac:parameter ac:name="server">HH JIRA</ac:parameter>'
                u'<ac:parameter ac:name="serverId">6faef456-0f82-358f-a362-1f1e9692b9b8</ac:parameter>'
                f'<ac:parameter ac:name="key">{match.group(1)}</ac:parameter>'
                u'</ac:structured-macro>'
            )

        return re.sub('<a.*href=\"[^\"]*https:\\/\\/jira.hh.ru\\/browse\\/([^\"]*)[^<]*<\\/a>', replacer, html, re.M)

    def preprocess(text):
        # Формат списков и ссылок
        return re.sub('<([^|]*)\\|([^>]+)>', '[\\2](\\1)', text.replace('•', '*'))

    return postprocess(markdown(preprocess(message_text), extensions=['nl2br']))


def get_confluence_users_map_by_name():
    with open('users.json', 'r') as file:
        teams_users = json.loads(file.read())
        file.close()

    mapping = {}

    for team in teams_users:
        for user in team['users']:
            mapping.update({
                user['userName']: {
                    'displayName': user['displayName'],
                    'userKey': user['userKey'],
                    'teamName': team['name'],
                }
            })

    return mapping


def get_confluence_user_key_by_slack_user(user):
    overrides_swap = {value: key for key, value in bot_settings.slack_settings['email_override'].items()}
    confluence_users_map = get_confluence_users_map_by_name()

    if user['email'] in overrides_swap:
        user_name = overrides_swap[user['email']]
    else:
        user_name = user['email'].split('@')[0]

    return confluence_users_map[user_name]['userKey']


def load_json_file(name, default=None, absolute_path=False) -> dict:
    content = default
    file_name = name if absolute_path else f'./cache/{name}'
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            try:
                content = json.loads(file.read())
            except json.decoder.JSONDecodeError:
                os.remove(file_name)
                pass
            file.close()

    return content


def save_json_file(name, content):
    with open(f'./cache/{name}', 'w') as file:
        file.write(json.dumps(content, indent=4))
        file.close()


def get_nearest_day_of_week(index):
    date = datetime.date.today()
    while date.weekday() != index:
        date += datetime.timedelta(1)

    return date.strftime('%Y-%m-%d')


def get_usable_date(params_date=None, defaults=None):
    if params_date is not None:
        return params_date

    if defaults is not None and 'date' in defaults and defaults['date'] is not None:
        return defaults['date']

    raise AttributeError('You must provide date either as parameter or bot settings default value')
