APP_ERROR_CODES_PREFIX_MAP = {
    1: "core",
    2: "users",
    3: "dictionary",
    4: "inventory",
}

import inspect
from . import translations


def is_dict(member):
    return isinstance(member, dict)


translations = inspect.getmembers(translations)


def get_default_error(lang: str = "ru"):
    error_messages = {
        "ru": "Ошибка сервера",
        "uz": "Server xatosi",
    }
    return error_messages[lang] if lang in error_messages else error_messages["ru"]


def get_error_message(error_code: int = 0, ctx: dict = None, lang: str = "ru"):
    for name, translation in translations:
        if name.endswith(lang.upper()):
            message = translation.get(error_code, get_default_error(lang))

            return message.format(**ctx) if ctx else message


def generate_error_response(error_code, ctx, lang=["ru", "uz"]):
    result = dict()
    for lang_code in lang:
        result[f"name_{lang_code}"] = get_error_message(error_code, ctx, lang_code)

    result["code"] = error_code
    return result
