import json
import codecs

import bot_settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.crab import CrabClient


def generate_users():
    confluence_client = ConfluenceClient(
        bot_settings.confluence_settings['login'],
        bot_settings.confluence_settings['password']
    )
    crab_client = CrabClient()

    teams_users = crab_client.get_users()
    parsed_teams = []
    force_include = list(bot_settings.crab_settings['force_include_users'])

    for team in teams_users:
        if team['name'] in bot_settings.crab_settings['force_exclude_teams']:
            continue
        parsed_team = []
        team_users = team['activeMembers'] + ([team['manager']] if 'manager' in team else [])
        print(team_users)
        for user in team_users:
            username = user['employee']['login']
            if username not in bot_settings.crab_settings['force_exclude_users'] and (
                user['direction'] in bot_settings.crab_settings['user_directions'] or
                username in force_include
            ):
                if username in force_include:
                    force_include.remove(username)

                user_info = confluence_client.get_user_info(username)
                parsed_team.append({
                    'userName': username,
                    'userKey': user_info['userKey'],
                    'displayName': user['employee']['fullname'],
                })
        parsed_team.sort(key=lambda item: item['displayName'])
        if len(parsed_team) > 0:
            team_name = team['name']
            if bot_settings.crab_settings['team_name_prefix']:
                team_name = team['name'].replace(bot_settings.crab_settings['team_name_prefix'], '')
            parsed_teams.append({
                'name': team_name,
                'users': parsed_team,
            })

    if len(force_include) > 0:
        parsed_team = []
        for username in force_include:
            if username not in bot_settings.crab_settings['force_exclude_users']:
                user_info = confluence_client.get_user_info(username)
                parsed_team.append({
                    'userName': username,
                    'userKey': user_info['userKey'],
                    'displayName': user_info['displayName']
                })
        parsed_team.sort(key=lambda item: item['displayName'])
        parsed_teams.append({
            'name': 'Unknown',
            'users': parsed_team,
        })

    parsed_teams.sort(key=lambda item: item['name'])

    with open('users.json', 'w') as file:
        file.write(codecs.decode(json.dumps(parsed_teams, indent=4, sort_keys=True), 'unicode-escape'))
        file.close()
