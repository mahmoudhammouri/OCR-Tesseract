from typing import List
import re
from unidecode import unidecode


def generate_keywords_regex(keyword: str) -> List[str]:
    """
    generates regexs for search keyword that accepts 1 possible spelling mistake
        Parameters:
            keyword (str): the base search keyword written correctly
        Returns:
            regexs (list[str]): list of all regexs made of that keyword
    """
    regexs = [keyword]
    for i in range(len(keyword)):
        new_key = keyword
        new_key = new_key[:i] + r"\w?" + new_key[i + 1:]
        regexs.append(new_key)
    return regexs


def get_possible_floats(keyword: str, lines: dict, exact=False) -> dict:
    possible_floats = {}
    flag_next_item = True
    for line_index, line_value in lines.items():

        for item_index in range(len(line_value)):
            result = search_by_keyword(
                keyword, line_value[item_index], exact)
            if len(result) != 0:
                try:
                    possible_floats[line_index] = [line_value[item_index], line_value[item_index + 1]]
                except:
                    possible_floats[line_index] = [line_value[item_index], line_value[item_index - 1]]
                    flag_next_item = False

                finally:
                    key_value = possible_floats[line_index][0]
                    str_value = possible_floats[line_index][1]
                    try:
                        float_value = extract_possible_float(str_value)
                    except:
                        float_value = 0
                    if float_value == 0:
                        try:
                            float_value = extract_integer(str_value)
                        except:
                            float_value = 0
                    if float_value == 0:
                        del possible_floats[line_index]
                    else:
                        possible_float = {
                            "key": key_value,
                            "str_value": str_value,
                            "float_value": float_value
                        }
                        possible_floats[line_index] = possible_float

                        if flag_next_item:
                            possible_floats[line_index]["value_index"] = line_index + 1
                        else:
                            possible_floats[line_index]["value_index"] = line_index - 1

    return possible_floats


def search_by_keyword(keyword: str, text: str, exact=False) -> List[re.Match]:
    text = text.lower()
    keyword = keyword.lower()
    if not exact:
        regexs = generate_keywords_regex(keyword)
    else:
        regexs = [keyword]
    matchs: List[re.Match] = []
    for regex in regexs:
        match: re.Match = re.search(regex, text)
        if match is not None:
            matchs.append(match)
    return matchs


def extract_possible_float(text: str):
    match = re.search(
        "(\s?\d+\s?[,|.|;|،]\s?)+\d+", text)
    possible_float = match.group(0)
    possible_float = unidecode(possible_float)
    possible_float = extract_clean_float(possible_float)
    return possible_float


def extract_clean_float(possible_float: str) -> float:
    # remove spaces
    possible_float = possible_float.replace(' ', '')
    # correct possible wrong the float point
    last_index = [m.start()
                  for m in re.finditer("[,|.|;|،]", possible_float)][-1]
    float_point_index = last_index - len(possible_float) + 1
    # completely clean the float
    possible_float = possible_float.replace(',', '')
    possible_float = possible_float.replace('.', '')
    # re-insert float point
    possible_float = possible_float[:float_point_index] + \
                     '.' + possible_float[float_point_index:]
    # return clean float value
    return float(possible_float)


def extract_integer(text: str) -> int:
    integer_string = re.search('\d+', text).group(0)
    return int(integer_string)
