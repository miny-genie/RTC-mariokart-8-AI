import re


cho_string  = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
jung_string = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
jong_string = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"


def decompose_korean(char: str) -> tuple[str]:
    if ord("ㄱ") <= ord(char) <= ord("ㅎ"):
        return char, '', ''
    
    unicode = ord(char) - ord("가")
    len_jung, len_jong = len(jung_string), len(jong_string)
    cho  = (unicode // len_jong) // len_jung
    jung = (unicode // len_jong) % len_jung
    jong = unicode % len_jong
    return cho_string[cho], jung_string[jung], jong_string[jong]


