import logging

confluence_settings = {
    'jira_base_url': 'jira.hh.ru',
    'wiki_base_url': 'wiki.hh.ru',
    'login': '',  # confluence login
    'password': '',  # confluence password
    'space_key': 'HHDEV',  # wiki space key
    'parent_page': 0,  # parent page for created pages
    'user_role': '',  # FE - Frontend, BE - Backend, TS - QA, TL - Teamlead
    'force_include_users': (),  # tuple of confluence logins
    'force_exclude_users': (),
    'add_team_header': True,
}

slack_settings = {
    'slack_hook_url': 'hooks.slack.com',
    'channel_hook': '',  # channel hook URL
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

connection_connect_timeout_s = 0.5
connection_read_timeout_s = 2
logging = logging
