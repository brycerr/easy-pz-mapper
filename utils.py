import re


def sanitize_input(input_str):
    return re.sub(r"[^\w\-. ]+$", "", input_str)    # returns a string that is a valid windows filepath
