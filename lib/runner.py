import sys
import urllib3

from lib.handlers.users import generate_users
from lib.handlers.page import generate_page
from lib.handlers.remind import remind_users

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AVAILABLE_COMMANDS = {
    'users': {
        'handler': generate_users,
        'description': 'Generate teams users list from confluence',
    },
    'page': {
        'handler': generate_page,
        'description': 'Creates wiki page',
    },
    'remind': {
        'handler': remind_users,
        'description': 'Reminds users not fulfilled their cell in'
    }
}


class Runner:
    def __init__(self):
        command_name = sys.argv[1] if len(sys.argv) > 1 else None
        if command_name is None or command_name not in AVAILABLE_COMMANDS:
            if command_name is None:
                print('Usage: python {} COMMAND [OPTIONS]'.format(sys.argv[0]))
            else:
                print('Command "{}" does not exists'.format(command_name))

            print('Available commands:{}'.format(Runner.format_commands()))
            return

        AVAILABLE_COMMANDS[command_name]['handler'](*sys.argv[2:])

    @staticmethod
    def format_commands():
        res = ''
        for command_name, command in AVAILABLE_COMMANDS.items():
            res = res + '\n{}\t\t{}'.format(command_name, command['description'])

        return res
