import re

from playground.korean_regexp.constants import (
    BASE, INITIALS, MEDIALS, FINALES, MIXED, MEDIAL_RANGE,
)


def decompose_korean(char: str) -> tuple[str]:
    if not char: return ""
    elif char == " ": return " "
    elif ord("ㄱ") <= ord(char) <= ord("ㅎ"): return char
    
    unicode = ord(char) - ord("가")
    len_jung, len_jong = len(MEDIALS), len(FINALES)
    
    cho  = (unicode // len_jong) // len_jung
    jung = (unicode // len_jong) % len_jung
    jong = unicode % len_jong

    if FINALES[jong] == " ": return INITIALS[cho], MEDIALS[jung]
    else: return INITIALS[cho], MEDIALS[jung], FINALES[jong]


class KMP:
    def compute_lps(self, word) -> list:
        word_length = len(word)
        lps = [0] * word_length
        length = 0  # length of match prefix and suffix
        index = 1
        
        while index < word_length:
            if word[index] == word[length]:
                length += 1
                lps[index] = length
                index += 1
            else:
                if length:
                    length = lps[length - 1]
                else:
                    lps[index] = 0
                    index += 1
                    
        return lps
    
    def search(self, origin_text, find_text) -> bool:
        olength = len(origin_text)
        flength = len(find_text)
        lps = self.compute_lps(find_text)
        
        oidx, fidx = 0, 0
        
        while oidx < olength:
            if find_text[fidx] == origin_text[oidx]:
                oidx += 1
                fidx += 1
                
            if fidx == flength:
                return True
            
            elif oidx < olength and origin_text[oidx] != find_text[fidx]:
                if fidx:
                    fidx = lps[fidx - 1]
                else:
                    oidx += 1
                    
        return False


def get_initial_search_reg_exp(initial, allow_only_initial=False):
    try:
        initial_offset = INITIALS.index(initial)
    except ValueError:
        return initial

    base_code = initial_offset * len(MEDIALS) * len(FINALES) + BASE
    start_char = chr(base_code)
    end_char = chr(base_code + len(MEDIALS) * len(FINALES) - 1)
    if allow_only_initial:
        return f"[{initial}{start_char}-{end_char}]"
    else:
        return f"[{start_char}-{end_char}]"






COMPLEX_DICT = {''.join(map(str, v)): k for k, v in MIXED.items()}


def assemble(lst: list):
    start_index = next((i for i, s in enumerate(lst) if s in MEDIALS), -1)
    end_condition = start_index != -1 and lst[start_index+1] in MEDIALS
    end_index = start_index + 1 if end_condition else start_index
    
    initial = ''.join(lst[:start_index])
    medial = ''.join(lst[start_index : end_index+1])
    finale = ''.join(lst[end_index+1:])
    
    tmp = COMPLEX_DICT.get(initial, initial)
    initial_offset = INITIALS.index(tmp) if tmp in INITIALS else -1
    
    tmp = COMPLEX_DICT.get(medial, medial)
    medial_offset = MEDIALS.index(tmp) if tmp in MEDIALS else -1
    tmp = COMPLEX_DICT.get(finale, finale)
    finale_offset = FINALES.index(tmp) if tmp in FINALES else -1
    
    if initial_offset != -1 and medial_offset != -1:
        init_unicode = initial_offset * len(MEDIALS) * len(FINALES)
        mid_unicode = medial_offset * len(FINALES)
        unicode = BASE + init_unicode + mid_unicode + finale_offset
        return chr(unicode)
    
    return ''.join(lst)