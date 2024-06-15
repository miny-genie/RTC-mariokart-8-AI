from playground.korean_regexp.constants import KEYS
from playground.korean_regexp.string_utils import explode, implode

KO_TO_EN = {kr:en for kr, en in KEYS}
EN_TO_KR = {en:kr for kr, en in KEYS}


def kor_to_eng(text: str) -> str:
    converted_chars = explode(text)
    return ''.join(KO_TO_EN.get(char, char) for char in converted_chars)


def eng_to_kor(text: str) -> str:
    converted_chars = [EN_TO_KR.get(char, char) for char in text]
    return implode(converted_chars)