import re
import time
import random
import datetime
from faker import Faker


# ----------------------------------------------------------------------
# # Do something
# ----------------------------------------------------------------------
def str_list(_str):
    _str = _str.strip("['").strip("']")
    _list = _str.replace("', '", "|")
    return _list.split('|')


def set_global(set_global_vars, response_text):
    # 请求返回结果
    # response_text = {"headers": {"Host": "666666"}}
    # set_global_vars = [{'name': 'test', 'query': ['headers', 'Host']}]
    global_vars = dict()
    new_temp_suite_params = dict()
    temp_suite_params = dict()

    if set_global_vars == None:
        return False

    if set_global_vars and isinstance(set_global_vars, list):
        for set_global_var in set_global_vars:
            if isinstance(set_global_var, dict) and isinstance(
                    set_global_var.get('name'),
                    str) and set_global_var.get('name'):
                name = set_global_var.get('name')
                query = set_global_var.get('query')
                if query and isinstance(query, list):
                    query = replace_global_var_for_list(
                        init_var_list=query, global_var_dic=global_vars)
                    # print(query)
                value = dict_get(response_text, query)
                global_vars[name] = str(value) if value else value
                new_temp_suite_params[name] = str(value) if value else value
    temp_suite_params.update(new_temp_suite_params)
    # temp_suite_params -> 全局变量操作
    return temp_suite_params


def replace_global_var_for_list(init_var_list,
                                global_var_dic,
                                global_var_regex='\${.*?}',
                                match2key_sub_string_start_index=2,
                                match2key_sub_string_end_index=-1):
    if not isinstance(init_var_list, list):
        raise TypeError('init_var_list must be list!')

    if len(init_var_list) < 1:
        raise ValueError('init_var_list should not be empty!')

    replaced_var = []
    for init_var_str in init_var_list:
        replaced_str = replace_global_var_for_str(
            init_var_str=init_var_str, global_var_dic=global_var_dic)
        replaced_var.append(replaced_str)
    return replaced_var


def replace_global_var_for_str(init_var_str,
                               global_var_dic,
                               global_var_regex='\${.*?}',
                               match2key_sub_string_start_index=2,
                               match2key_sub_string_end_index=-1):

    if not isinstance(init_var_str, str):
        raise TypeError('init_var_str must be str！')

    if not isinstance(global_var_dic, dict):
        raise TypeError('global_var_dic must be dict！')

    if not isinstance(global_var_regex, str):
        raise TypeError('global_var_regex must be str！')

    if not isinstance(match2key_sub_string_start_index, int):
        raise TypeError('match2key_sub_string_start_index must be int！')

    if not isinstance(match2key_sub_string_end_index, int):
        raise TypeError('match2key_sub_string_end_index must be int！')

    regex_pattern = re.compile(global_var_regex)

    def global_var_repl(match_obj):
        start_index = match2key_sub_string_start_index
        end_index = match2key_sub_string_end_index
        match_value = global_var_dic.get(
            match_obj.group()[start_index:end_index])
        # 将一些数字类型转成str，否则re.sub会报错, match_value可能是0！
        match_value = str(
            match_value) if match_value is not None else match_value
        return match_value if match_value else match_obj.group()

    replaced_var = re.sub(pattern=regex_pattern,
                          string=init_var_str,
                          repl=global_var_repl)
    return replaced_var


def is_slice_expression(expression):
    if re.match("(-?\d+)?:(-?\d+)?", expression):
        return True
    else:
        return False


def can_convert_to_int(input):
    try:
        int(input)
        return True
    except BaseException:
        return False


def is_specific_search_by_dict_value(expression):
    if re.match(r'(.)+=(.)+\.(.)+', expression):
        return True
    else:
        return False


def dict_get(dic, locators, default=None):
    if not isinstance(dic, dict):
        if isinstance(dic, str) and len(locators) == 1:
            if is_slice_expression(locators[0]):
                slice_indexes = locators[0].split(':')
                start_index = int(
                    slice_indexes[0]) if slice_indexes[0] else None
                end_index = int(
                    slice_indexes[-1]) if slice_indexes[-1] else None
                value = dic[start_index:end_index]
                return value
            else:
                # 如果不满足切片规则，就直接进行正则匹配
                match_obj = re.search(locators[0], dic)
                return match_obj.group() if match_obj else None
        return dic

    if dic == {} or len(locators) < 1:
        return str(dic)  # 用于后续 re.search

    value = None
    for locator in locators:
        locator = locator.replace(' ', '').replace('\n', '').replace('\t', '')
        if not type(value) in [dict, list] and isinstance(
                locator, str) and not is_slice_expression(locator):
            try:
                value = dic[locator]
            except KeyError:
                return default
            continue
        if isinstance(value, str) and is_slice_expression(locator):
            try:
                slice_indexes = locator.split(':')
                start_index = int(
                    slice_indexes[0]) if slice_indexes[0] else None
                end_index = int(
                    slice_indexes[-1]) if slice_indexes[-1] else None
                value = value[start_index:end_index]
            except KeyError:
                return default
            continue
        if isinstance(value, dict):
            try:
                value = dict_get(value, [locator])
            except KeyError:
                return default
            continue
        if isinstance(value, list) and len(value) > 0:
            if can_convert_to_int(locator):
                try:
                    value = value[int(locator)]
                except IndexError:
                    return default
                continue
            elif is_specific_search_by_dict_value(locator) and all(
                [isinstance(v, dict) for v in value]):
                # e.g.
                # locator:  email=michael(.)+.first_name
                # 含义为 取 （key = email, value = michael开头） 的那个 dict的 key 为 first_name 的value
                first_equal_index = locator.index('=')
                last_dot_index = locator.rindex('.')
                matched_key_re = locator[:first_equal_index]  # 字典中存在满足的正则条件的键
                # matched_key对应的值需要满足的正则条件
                matched_value_re = locator[first_equal_index +
                                           1:last_dot_index]
                # 满足正则条件的字典中待取的值的键
                needed_value_key = locator[last_dot_index + 1:]

                for dic in value:
                    for k, v in dic.items():
                        if re.match(matched_key_re, str(k)) and re.match(
                                matched_value_re, str(v)):
                            needed_value = dic.get(needed_value_key)
                            value = needed_value
                            break
                    else:
                        continue
                    break
                else:
                    return default
                continue
            elif locator == 'random':
                try:
                    value = value[random.randint(0, len(value) - 1)]
                except IndexError:
                    return default
                continue
    return value


def resolve_faker_var(
        init_faker_var,
        faker_var_regex=r'\$faker{([a-z]{2}_[A-Z]{2})?\.?(.*?)(\(.*?\))}'):
    re_global_var = re.compile(faker_var_regex)

    def faker_var_repl(match_obj):
        locale_index = match_obj.group(1)
        method_name = match_obj.group(2)
        _args = match_obj.group(3)
        _faker = Faker(locale_index)
        _kwargs = str_args_2_dict(_args) if '=' in _args else {}
        match_value = getattr(_faker, method_name)(**_kwargs)
        # 将一些数字类型转成str，否则re.sub会报错, match_value可能是0！
        match_value = str(
            match_value) if match_value is not None else match_value
        return match_value if match_value else match_obj.group()

    resolved_var = re.sub(pattern=re_global_var,
                          string=init_faker_var,
                          repl=faker_var_repl)
    return resolved_var


def str_args_2_dict(args: str) -> dict:
    args = args.replace(' ', '')
    args = args.replace('(', '')
    args = args.replace(')', '')
    args_list = args.split(',')
    dic = {}
    for param in args_list:
        equal_sign_index = param.index('=')
        key = param[:equal_sign_index]
        value = param[equal_sign_index + 1:]
        if '<int>' in value:
            value = int(value[value.find('<int>') + 5:])
        elif '<float>' in value:
            value = float(value[value.find('<float>') + 7:])
        dic[key] = value
    return dic


def resolve_func_var(init_func_var,
                     func_var_regex=r'\$func{([a-zA-Z0-9_]*)(\(.*?\))}'):
    re_global_var = re.compile(func_var_regex)

    def func_var_repl(match_obj):
        method_name = match_obj.group(1)
        _args = match_obj.group(2)
        _func = Func()
        _kwargs = str_args_2_dict(_args) if '=' in _args else {}
        match_value = getattr(_func, method_name)(**_kwargs)
        # 将一些数字类型转成str，否则re.sub会报错, match_value可能是0！
        match_value = str(
            match_value) if match_value is not None else match_value
        return match_value if match_value else match_obj.group()

    resolved_var = re.sub(pattern=re_global_var,
                          string=init_func_var,
                          repl=func_var_repl)
    return resolved_var


class Func:
    def __init__(self):
        pass

    def get_milli_second_timestamp(self):
        now_timetuple = time.time()
        return int(round(now_timetuple * 1000))  # 毫秒级时间戳

    def get_micro_second_timestamp(self):
        now_timetuple = time.time()
        return int(round(now_timetuple * 1000000))  # 微秒级时间戳

    def get_second_timestamp(self):
        now_timetuple = time.time()
        return int(now_timetuple)  # 秒级时间戳

    def get_current_time(self, format_str="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.now().strftime(format_str)


def replace_global_var_for_str(init_var_str,
                               global_var_dic,
                               global_var_regex='\${.*?}',
                               match2key_sub_string_start_index=2,
                               match2key_sub_string_end_index=-1):
    if not isinstance(init_var_str, str):
        raise TypeError('init_var_str must be str！')

    if not isinstance(global_var_dic, dict):
        raise TypeError('global_var_dic must be dict！')

    if not isinstance(global_var_regex, str):
        raise TypeError('global_var_regex must be str！')

    if not isinstance(match2key_sub_string_start_index, int):
        raise TypeError('match2key_sub_string_start_index must be int！')

    if not isinstance(match2key_sub_string_end_index, int):
        raise TypeError('match2key_sub_string_end_index must be int！')

    regex_pattern = re.compile(global_var_regex)

    def global_var_repl(match_obj):
        start_index = match2key_sub_string_start_index
        end_index = match2key_sub_string_end_index
        match_value = global_var_dic.get(
            match_obj.group()[start_index:end_index])
        # 将一些数字类型转成str，否则re.sub会报错, match_value可能是0！
        match_value = str(
            match_value) if match_value is not None else match_value
        return match_value if match_value else match_obj.group()

    replaced_var = re.sub(pattern=regex_pattern,
                          string=init_var_str,
                          repl=global_var_repl)
    return replaced_var


def resolve_int_var(init_int_str, int_var_regex='\'?<int>([0-9]+)</int>\'?'):
    re_int_var = re.compile(int_var_regex)
    def int_var_repl(match_obj):
        return match_obj.group(1) if match_obj.group(1) else match_obj.group()

    resolved_var = re.sub(pattern=re_int_var,
                          string=init_int_str,
                          repl=int_var_repl)
    return resolved_var
