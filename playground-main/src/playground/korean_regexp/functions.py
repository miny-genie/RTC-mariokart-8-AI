import logging
import re

from playground.korean_regexp.constants import (
    BASE, INITIALS, MEDIALS, FINALES, MIXED, MEDIAL_RANGE,
)
from playground.korean_regexp.decomposition import get_phonemes
from playground.korean_regexp.escape import escape_regexp
from playground.korean_regexp.string_utils import assemble, implode, explode
from playground.korean_regexp.translation import eng_to_kor, kor_to_eng

logger = logging.getLogger(__name__)

FUZZY = f"__{int('fuzzy', 36)}__"
IGNORE_SPACE = f"__{int('ignorespace', 36)}__"


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


def get_initial_search_regexp(initial, allow_only_initial=False):
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


last_search = ""
last_pattern = []


def get_reg_exp(
    search: str,
    initial_search = False, starts_with = False, ends_with = False,
    ignore_space = False, ignore_case = True, _global = False,
    fuzzy = False, non_capture_group = False, eng_to_kor = False
):
    global last_search, last_pattern
    
    if last_search == search:
        return last_pattern
    
    _search = search
    add_patterns = []
    
    if eng_to_kor and re.match(r'^([a-zA-Z0-9\s]{2,})$', search.strip()):
        kor = eng_to_kor(search.strip())
        if re.match(r'^[가-힣ㄱ-ㅎ0-9]', kor):
            _search = kor
            add_patterns.append(escape_regexp(search.strip()))
    
    front_chars = list(_search)
    last_char = front_chars.pop() if front_chars else ""
    
    phonemes = get_phonemes(last_char)
    init, mid, final, init_offset, mid_offset, final_offset = phonemes
    
    # 마지막 글자가 한글인 경우에만 실행
    if init_offset != -1:
        
        # 해당 초성으로 시작하는 첫 문자: 가, 나, 다, ..., 하
        base_code = init_offset * len(MEDIALS) * len(FINALES) + BASE
        patterns = []
        
        # case 1) 종성으로 끝나는 경우(받침이 있는 경우)
        if final:
            patterns.append(last_char)  # 마지막 글자
            if final in INITIALS:   # 종성이 초성으로 사용 가능한 경우
                exp_fir = chr(base_code + mid_offset * len(FINALES))
                exp_sec = get_initial_search_regexp(final)
                patterns.append(f"{exp_fir}{exp_sec}")
                
            if final in MIXED:  # 종성이 복합 자음인 경우, 분리 후 받침과 초성으로 사용
                mixed_init, mixed_final = MIXED[final]
                exp_fir = chr(base_code + mid_offset * len(FINALES) + FINALES.index(mixed_init))
                exp_sec = get_initial_search_regexp(mixed_final)
                patterns.append(f"{exp_fir}{exp_sec}")
        
        # case 2) 중성으로 끝나는 경우(받침이 없는 경우)
        elif mid:
            if mid in MEDIAL_RANGE: # 중성이 복합 모음인 경우
                mixed_fir, mixed_sec = MEDIAL_RANGE[mid]
                _from = base_code + MEDIALS.index(mixed_fir) * len(FINALES)
                to = base_code + MEDIALS.index(mixed_sec) * len(FINALES) + len(FINALES) - 1
            else:
                _from = base_code + mid_offset * len(FINALES)
                to = _from + len(FINALES) - 1
            patterns.append(f"{chr(_from)}-{chr(to)}")
        
        # case 3) 초성만 입력된 경우
        elif init:
            patterns.append(get_initial_search_regexp(init, True))
                
        # last_char_pattern 선언
        if patterns:
            if non_capture_group:
                last_char_pattern = f"(?:{'|'.join(patterns)})"
            else:
                last_char_pattern = f"({'|'.join(patterns)})"
        else:
            last_char_pattern = patterns[0]
    
    # 정규식 생성용 변수 선언
    glue = FUZZY if fuzzy else (IGNORE_SPACE if ignore_space else "")
    
    if initial_search:
        front_chars_pattern = glue.join(
            get_initial_search_regexp(char, True) if re.search(r'[ㄱ-ㅎ]', char) else escape_regexp(char)
            for char in front_chars
        )
    else:
        front_chars_pattern = escape_regexp(glue.join(front_chars))
        
    pattern = (
        f"{'^' if starts_with else ''}"
        f"{front_chars_pattern}"
        f"{glue}"
        f"{last_char_pattern}"
        f"{'$' if ends_with else ''}"
    )
    
    # 정규식 생성
    if glue:
        pattern = re.sub(FUZZY, ".*", pattern)
        pattern = re.sub(IGNORE_SPACE, r'\s*', pattern)
        
    if add_patterns:
        combined = add_patterns + [pattern]
        print(combined)
        pattern = "|".join(f'({comb})' for comb in combined)
        
    flags = re.IGNORECASE if ignore_case else 0
    last_pattern = re.compile(pattern, flags)
    return last_pattern