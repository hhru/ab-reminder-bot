from lib.utils import get_nearest_day_of_week


defaults = {
    'date': get_nearest_day_of_week(4), # если не передана дата - считаем, что передана ближайшая следующая пятница
}

confluence_settings = {
    'space_key': 'HHDEV',  # wiki space key
    'parent_page': 0,  # parent page for created pages
    'add_team_header': True,
}

crab_settings = {
    'url': 'crab.pyn.ru',
    'user_directions': ('frontend', ),  # frontend, backend, qa, mobile, analytics, datascience
    'force_include_users': (),  # tuple of user logins
    'force_exclude_users': (),  # tuple of user logins
    'force_exclude_teams': ('Технический департамент',),  # crab returns director's team separately
    'team_name_prefix': 'Команда ',  # this will be omitted in team name
}

slack_settings = {
    'channel': 'frontend',  # slack channel to post to, for private channels bot must be installed
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
