from .core import STATUS_CODES as CORE_STATUS_CODES
from .users import STATUS_CODES as USERS_STATUS_CODES
from .dictionary import STATUS_CODES as DICTIONARY_STATUS_CODES
from .inventory import STATUS_CODES as INVENTORY_STATUS_CODES


STATUS_CODES = dict()

STATUS_CODES.update(CORE_STATUS_CODES)
STATUS_CODES.update(USERS_STATUS_CODES)
STATUS_CODES.update(DICTIONARY_STATUS_CODES)
STATUS_CODES.update(INVENTORY_STATUS_CODES)