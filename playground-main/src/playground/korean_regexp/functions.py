import re

from playground.korean_regexp.constants import (
    BASE, INITIALS, MEDIALS, FINALES, MIXED, MEDIAL_RANGE,
)

COMPLEX_DICT = {''.join(map(str, v)): k for k, v in MIXED.items()}


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


def assemble(lst: list) -> str:
    start_index = next((i for i, s in enumerate(lst) if s in MEDIALS), -1)
    try:
        end_condition = start_index != -1 and lst[start_index+1] in MEDIALS
        end_index = start_index + 1 if end_condition else start_index
    except IndexError:
        end_index = start_index
    
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


def implode(_input: str|list[str]) -> str:
    chars = []
    
    # 인접한 모음을 하나의 복합 모음으로 결합.
    for i, char in enumerate(_input):
        is_str = isinstance(char, str)
        is_medial = chars and char in MEDIALS
        is_twice = _input[i-1] in MEDIALS and f"{_input[i-1]}{char}" in COMPLEX_DICT
        
        if is_str and is_medial and is_twice:
            chars[-1] = COMPLEX_DICT[f"{_input[i-1]}{char}"]
        else:
            chars.append(char)
    
    cursor = {"medial": None, "finale": []}
    items = [cursor]
    
    # 모음으로 시작하는 그룹 생성. (grouped 항목 유지)
    for i, char in enumerate(chars):
        if isinstance(char, list):
            cursor = {"medial": None, "finale": []}
            items.append({"grouped": char, "finale": []})
            items.append(cursor)
        
        elif char in MEDIALS:
            cursor = {"medial": char, "finale": []}
            items.append(cursor)
        
        else:
            cursor["finale"].append(char)
    
    # 그룹을 순회하며 복합 자음을 정리.
    # 앞그룹에서 종성으로 사용하고 남은 자음은 뒷그룹의 초성으로 이동.
    for i, cur in enumerate(items):
        if i > 0:
            prev = items[i - 1]
            if prev["medial"] is None or len(prev["finale"]) == 1:
                cur["initial"] = prev["finale"]
                prev["finale"] = []
            else:
                finale, *initial = prev["finale"]
                cur["initial"] = initial
                prev["finale"] = [finale] if finale else []
            
            remain_prev_finale = len(cur["finale"]) > 2
            last_char = i == len(items) - 1 and len(cur["finale"]) > 1
            if remain_prev_finale or last_char:
                fir, sec, *remain = cur["finale"]
                if f"{fir}{sec}" in COMPLEX_DICT:
                    cur["finale"] = [COMPLEX_DICT[f"{fir}{sec}"]] + remain
        
    groups = []
    
    # 각 글자에 해당하는 블록 단위로 조합.
    for item in items:
        initials = item.get("initial", [])
        medial = item.get("medial")
        finales = item.get("finale", [])
        grouped = item.get("grouped", False)
        
        if grouped:
            groups.append(grouped)
        
        else:
            # struct: pre, init, medial, final, post
            pre = initials[:]
            init = pre.pop() if pre else None
            try:
                final, *post = finales
            except ValueError:
                final, post = None, []
            
            if final not in FINALES:
                post = [final] + post
                final = ""
                        
            for p in filter(lambda x: x is not None, pre):
                groups.append([p])
            groups.append(list(filter(lambda x: x, [init, medial, final])))
            for p in filter(lambda x: x is not None, post):
                groups.append([p])
        
    return ''.join(assemble(group) for group in groups)