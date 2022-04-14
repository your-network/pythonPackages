import re

def get_digits(string):
    digits = re.findall(r'\d+', string)
    if len(digits) == 0:
        return None
    elif len(digits) > 1:
        return float(".".join(map(str,digits)))
    elif len(digits) == 1:
        return int(digits[0])

def remove_nulls(d):
    none_filtered = {k: v for k, v in d.items() if v is not None}
    return {k: v for k, v in none_filtered.items() if v != ''}
