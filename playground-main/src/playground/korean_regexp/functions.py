import logging

from playground.korean_regexp.constants import (
    BASE, INITIALS, MEDIALS, FINALES, MIXED, MEDIAL_RANGE,
)
from playground.korean_regexp.decomposition import get_phonemes
from playground.korean_regexp.escape import escape_regexp
from playground.korean_regexp.string_utils import assemble, implode, explode
from playground.korean_regexp.translation import eng_to_kor, kor_to_eng

logger = logging.getLogger(__name__)


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