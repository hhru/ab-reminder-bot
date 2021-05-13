import logging
from lib.utils import get_nearest_day_of_week

defaults = {
    'date': get_nearest_day_of_week(4),  # nearest friday
}

confluence_settings = {
    'jira_base_url': 'jira.hh.ru',
    'wiki_base_url': 'wiki.hh.ru',
    'login': '',  # confluence login
    'password': '',  # confluence password
    'space_key': 'HHDEV',  # wiki space key
    'parent_page': 0,  # parent page for created pages
    'add_team_header': True,
}

crab_settings = {
    'crab_base_url': 'crab.pyn.ru',
    'user_directions': ('frontend', ),  # frontend, backend, qa, mobile, analytics, datascience
    'force_include_users': (),  # tuple of user logins
    'force_exclude_users': (),  # tuple of user logins
    'team_name_prefix': 'Команда ',  # this will be omitted in team name
}

slack_settings = {
    'slack_api_url': 'https://slack.com/api',
    'channel': 'frontend',  # slack channel to post to, for private channels bot must be installed
    'oauth_token': '',  # oAUTH authorization token
    'email_override': {},  # dict of confluence_logins to emails mapping
}

# templates mapping to override default values, if none or not exists - values will be taken from lib/templates.py
templates_overrides = {
    'TITLE_TEMPLATE': u'Front-end AB {date}',
    'PAGE_TEMPLATE': None,
    'TEAM_ROW_TEMPLATE': None,
    'USER_ROW_TEMPLATE': None,
    'SLACK_PAGE_MESSAGE_TEMPLATE': None,
    'SLACK_REMIND_MESSAGE_TEMPLATE': None,
    'SLACK_REMIND_ALL_CHECKED_TEMPLATE': None,
    'SLACK_REMIND_HAS_UNCHECKED_TEMPLATE': None,
}

# Optional: labels for creating page
labels = [
    "some label text"  # e.g 'технологизация_android'
]

connection_connect_timeout_s = 0.5
connection_read_timeout_s = 2
logging = logging
