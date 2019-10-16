import json
import codecs

import bot_settings
from lib.api_clients.confluence import ConfluenceClient


def generate_users():
    client = ConfluenceClient(bot_settings.confluence_settings['login'], bot_settings.confluence_settings['password'])

    teams_users = client.get_users()
    parsed_teams = []
    force_include = list(bot_settings.confluence_settings['force_include_users'])

    for team in teams_users:
        parsed_team = []
        for user in team['activeMembers']:
            username = user['employee']['login']
            if username not in bot_settings.confluence_settings['force_exclude_users'] and (
                    user['role'] in bot_settings.confluence_settings['user_role']
                    or username in force_include
            ):
                if username in force_include:
                    force_include.remove(username)

                user_info = client.get_user_info(username)
                parsed_team.append({
                    'userName': username,
                    'userKey': user_info['userKey'],
                    'displayName': user_info['displayName'],
                })
        if len(parsed_team) > 0:
            parsed_teams.append({
                'name': team['name'],
                'users': parsed_team,
            })

    if len(force_include) > 0:
        parsed_team = []
        for username in force_include:
            if username not in bot_settings.confluence_settings['force_exclude_users']:
                user_info = client.get_user_info(username)
                parsed_team.append({
                    'userName': username,
                    'userKey': user_info['userKey'],
                    'displayName': user_info['displayName']
                })
        parsed_teams.append({
            'name': 'Unknown',
            'users': parsed_team,
        })

    with open('users.json', 'w') as file:
        file.write(codecs.decode(json.dumps(parsed_teams, indent=4, sort_keys=True), 'unicode-escape'))
        file.close()
