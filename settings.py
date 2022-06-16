import json
import logging

from bot_settings import *


general_config_file = open('./general_config.json')
general_config = json.load(general_config_file)
general_config_file.close()

config = general_config['ab_reminder_bot']

slack_settings['url'] = config['slack_url']

confluence_settings['jira_url'] = config['jira_url']
confluence_settings['wiki_url'] = config['wiki_url']
confluence_settings['wiki_username'] = config['wiki_username']
confluence_settings['wiki_password'] = config['wiki_password']

connection_connect_timeout_s = config['connect_timeout_s']
connection_read_timeout_s = config['read_timeout_s']

logging = logging

