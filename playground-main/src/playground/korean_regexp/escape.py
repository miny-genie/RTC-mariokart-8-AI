import re

re_regexp_char = re.compile(r'[\\^$.*+?()[\]{}|]')
re_has_regexp_char = re_regexp_char.search


def escape_regexp(string: str):
    if string and re_has_regexp_char(string):
        return re_regexp_char.sub(r'\\\g<0>', string)
    else:
        return string or ''