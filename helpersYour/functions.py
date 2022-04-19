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

def remove_dic_none_values(dic):
    remove_fields = []
    for key,value in dic.items():
        if value is None and key is not None:
            remove_fields.append(key)
    final_dic = remove_dic_key(dic,remove_fields)
    return final_dic

def remove_dic_key(dic,keys):
    for remove in keys:
        try:
            del dic[remove]
        except:
            continue
    return dic

def rename_dic_key(dic={},naming=[]):
    for row in naming:
        old = row.get('old',None)
        new = row.get('new',None)
        if old:
            dic[new] = dic.pop(old)
    return dic

