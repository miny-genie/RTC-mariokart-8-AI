from playground.korean_regexp.constants import (
    BASE, INITIALS, MEDIALS, FINALES, MIXED, MEDIAL_RANGE,
)


def decompose_korean(char: str) -> tuple[str]:
    if not char: return ""
    elif char == " ": return " "
    elif ord("ㄱ") <= ord(char) <= ord("ㅎ"): return char
    
    unicode = ord(char) - BASE
    len_jung, len_jong = len(MEDIALS), len(FINALES)
    
    cho  = (unicode // len_jong) // len_jung
    jung = (unicode // len_jong) % len_jung
    jong = unicode % len_jong

    if FINALES[jong] == " ": return INITIALS[cho], MEDIALS[jung]
    else: return INITIALS[cho], MEDIALS[jung], FINALES[jong]