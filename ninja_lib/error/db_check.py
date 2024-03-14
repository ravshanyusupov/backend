def get_integrity_error_code(exc):
    error_message = str(exc)

    if "FOREIGN KEY" in error_message.upper():
        return 1003

    elif "UNIQUE" in error_message.upper():
        return 1004

    return 0
