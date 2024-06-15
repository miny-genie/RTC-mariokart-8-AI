from playground.korean_regexp.constants import (
    BASE, INITIALS, MEDIALS, FINALES,
)


def get_phonemes(char: str) -> tuple:
    init, mid, final = "", "", ""
    init_offset, mid_offset, final_offset = -1, -1, -1

    if ord("ㄱ") <= ord(char) <= ord("ㅎ"):
        init = char
        init_offset = INITIALS.index(char)
        
    elif ord("가") <= ord(char) <= ord("힣"):
        unicode = ord(char) - BASE
        len_mid, len_final = len(MEDIALS), len(FINALES)
        
        init_offset = (unicode // len_final) // len_mid
        mid_offset = (unicode // len_final) % len_mid
        final_offset = unicode % len_final
        
        init = INITIALS[init_offset]
        mid = MEDIALS[mid_offset]
        final = FINALES[final_offset]
        
    return init, mid, final, init_offset, mid_offset, final_offset