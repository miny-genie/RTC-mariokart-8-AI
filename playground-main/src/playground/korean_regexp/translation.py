from playground.korean_regexp.constants import KEYS
from playground.korean_regexp.implode import implode

EN_TO_KR = {en:kr for kr, en in KEYS}


def eng_to_kor(text: str):
    converted_chars = [EN_TO_KR.get(char, char) for char in text]
    return implode(converted_chars)


def kor_to_eng():
    return