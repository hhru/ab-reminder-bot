from enum import Enum

CHECKED_MESSAGE_REACTION = 'heavy_check_mark'
BOT_PROCESSED_REACTION = 'ok_hand'


class PageUpdateStates(str, Enum):
    IDLE = 'idle'
    GATHERING = 'gathering'


class ApiOperationException(Exception):
    pass



