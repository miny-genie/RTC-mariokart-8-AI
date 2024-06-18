# import playground.ui

# print("TEST")


from playground.korean_regexp.functions import get_reg_exp as re_korean

text = "gr"
exp = re_korean(text, initial_search=True, _eng_to_kor=True)

import re
print(exp)
for word in ["gksr", "한글", "한국", "대한민국"]:
    ans = re.findall(exp, word)
    if ans: print(word)