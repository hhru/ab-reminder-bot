import json
import codecs

import settings
from lib.api_clients.confluence import ConfluenceClient
from lib.api_clients.crab import CrabClient


def generate_users():
    confluence_client = ConfluenceClient(
        settings.confluence_settings['wiki_username'],
        settings.confluence_settings['wiki_password']
    )
    crab_client = CrabClient()

    teams_users = crab_client.get_users()
    parsed_teams = []
    force_include = list(settings.crab_settings['force_include_users'])

    for team in teams_users:
        if team['name'] in settings.crab_settings['force_exclude_teams']:
            continue
        parsed_team = []
        team_users = team['activeMembers'] + ([team['manager']] if 'manager' in team else [])
        for user in team_users:
            username = user['employee']['login']
            if username not in settings.crab_settings['force_exclude_users'] and (
                user['direction'] in settings.crab_settings['user_directions'] or
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
            if settings.crab_settings['team_name_prefix']:
                team_name = team['name'].replace(settings.crab_settings['team_name_prefix'], '')
            parsed_teams.append({
                'name': team_name,
                'users': parsed_team,
            })

    if len(force_include) > 0:
        parsed_team = []
        for username in force_include:
            if username not in settings.crab_settings['force_exclude_users']:
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

    with open('./cache/users.json', 'w') as file:
        file.write(codecs.decode(json.dumps(parsed_teams, indent=4, sort_keys=True), 'unicode-escape'))
        file.close()
