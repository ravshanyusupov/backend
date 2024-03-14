from .core import ERROR_CODES as CORE_ERROR_CODES
from .users import ERROR_CODES as USER_ERROR_CODES
from .dictionary import ERROR_CODES as DICTIONARY_ERROR_CODES
from .inventory import ERROR_CODES as INVENTORY_ERROR_CODES


ERROR_CODES_UZ = dict()

ERROR_CODES_UZ.update(CORE_ERROR_CODES)
ERROR_CODES_UZ.update(USER_ERROR_CODES)
ERROR_CODES_UZ.update(DICTIONARY_ERROR_CODES)
ERROR_CODES_UZ.update(INVENTORY_ERROR_CODES)