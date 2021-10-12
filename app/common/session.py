import re
import ast
import ssl
import json
import time
import requests
from app.common.utils import *
from app.common.globalParams import _Cache
from app.common.decorator import async_test
from app.common.helper import single_Save_response, save_TestReport


resp_status = {
    0: "pass",
    1: "failed",
    2: "error",
    3: "notRun"
}


# 单一用例调试
@async_test
def send_and_save_report(test_list):
    result_list = manual_test_by_case(test_list)
    if result_list == []:
        return {'status': 'failed', 'data': '测试接口引发异常错误'}
    else:
        for x in range(len(result_list)):
            __obj = result_list[x].get("object_id")
            if __obj != None:
                single_Save_response(result_list[x], __obj)
            else:
                return {'status': 'failed', 'data': '找不到测试用例无法保存测试结果'}
    return True


# 异步多套接口测试
@async_test
def send_and_save_report_BySuite(test_list, action={}):
    """
    {
        "object_id" : "object_id",
        "EnvName" : "测试",
        "EnvId" : "测试环境 ID",
        "executionMode" : "manual",
        "cronJobId" : "定时服务 ID",
        "projectId" : "项目 ID",
        "接口测试套件" : {
            "接口 ID AAA":"【测试用例...........】",
            "接口 ID BBB":"【测试用例...........】"
        },
        "启动时间" : 123456789,
        "totalCount" : 1,
        "passCount" : 1,
        "failCount" : 0,
        "errorCount" : 0,
        "spendTimeInSec" : 0.029
    }
    """
    if test_list != []:
        Detail = {}
        totalCount = 0
        passCount = 0
        failCount = 0
        errorCount = 0
        report_StartTime = time.time()

        result_list = manual_test_by_case(test_list)
        if result_list == []:
            return {'status': 'failed', 'data': '测试接口引发异常错误'}
        else:
            for x in range(len(result_list)):
                totalCount = len(result_list)
                status = result_list[x].get("status")
                if status == resp_status.get(0):
                    passCount += 1
                elif status == resp_status.get(1):
                    failCount += 1
                elif status == resp_status.get(2):
                    errorCount += 1

                Detail.update({
                    # result_list[x].get("Interface_id") : [result_list[x] for x in range(len(result_list))],
                    result_list[x].get("Interface_id") : [
                        result_list[index] for index in range(len(result_list))
                        if result_list[index].get("Interface_id") == result_list[x].get("Interface_id")
                    ],
                })

        result_report = {
            "uid" : action.get("uid"),
            "executionMode": action.get("executionMode"),
            "cronJobId": action.get("cronJobId"),
            "EnvName": test_list[0].get("EnvName"),
            "EnvId": test_list[0].get("EnvId"),

            "StartTime": int(report_StartTime),
            "Project_id": test_list[0].get("Project_id"),
            "interfaces_Suites_CaseDetail": Detail,
            "totalCount": totalCount,
            "passCount": passCount,
            "failCount": failCount,
            "errorCount": errorCount,
            "spendTimeInSec": round(time.time() - report_StartTime, 3),
        }
        save_TestReport(result_report)
    else:
        _err_msg = "因为找不到项目或接口下的用例，无法执行测试"
        result_report = {'status': 'failed', 'data': _err_msg}
        return result_report
    return True


def manual_test_by_case(test_case_list):
    test_results = []
    for test_case in test_case_list:
        test_result = execute_single_case_test(**test_case)
        if test_result == None:
            return {"msg": "有bug要修复了!"}
        test_results.append(test_result)
    return test_results


def execute_single_case_test(max_retries=5, **params):
    # useless
    ssl._create_default_https_context = ssl._create_unverified_context
    requests.packages.urllib3.disable_warnings()
    session = requests.Session()

    if isinstance(max_retries, int) and max_retries > 0:
        # 设置连接重试
        adapters = requests.adapters.HTTPAdapter(max_retries=max_retries)
        session.mount("https://", adapters)
        session.mount("http://", adapters)
    session.cookies.clear()
    returned_data = {
        "Conclusion": [],
        "status": None,
    }
    if params is not None and len(params) > 0:
        # returned_data["Project_id"] = params["Project_id"]
        returned_data["Interface_id"] = params["Interface_id"]
        returned_data["testcase_name"] = params["name"]
        returned_data["object_id"] = params["object_id"]

        # 把断言数据穿透到报告中
        returned_data["checkoptions"] = params["checkoptions"]
        returned_data["checkSpendSeconds"] = params["checkSpendSeconds"]
        returned_data["checkResponseCode"] = params["checkResponseCode"]
        returned_data["checkResponseBody"] = params["checkResponseBody"]

        # 调整初始化参数
        params["parameterType"] = params["parameterType"].lower()

        response_json = dict()
        check_response_code = None
        check_spend_seconds = None
        check_response_body = None
        # check_response_number = None

        check_connect_redis = None
        if params["redis"] != None:
            try:
                global_vars = _Cache(**params["redis"]).get_GlobalParams()
            except BaseException as e:
                global_vars = {}
                check_connect_redis = False
                print("由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败!")
        else:
            global_vars = {}

        check_connect_mysql = None
        if params["mysql"] != None:
            check_connect_mysql = False
            print("暂没做 Mysql 连接校验")
        else:
            pass

        request_url = params["route"]
        if params["Method"].lower() == 'get' and params['Body'] != None:
            request_url += "?"
            for key, value in ast.literal_eval(params['Body']).items():
                if value is not None:
                    request_url += '%s=%s&' % (key, value)
                    request_url = resolve_faker_var(init_faker_var=request_url)
                    request_url = resolve_func_var(init_func_var=request_url)
                    request_url = replace_global_var_for_str(
                                    init_var_str=request_url,
                                    global_var_dic=global_vars)
            request_url = resolve_int_var(init_int_str=request_url)
            request_url = request_url[0:(len(request_url) - 1)]
            params['route'] = request_url


        elif params['parameterType'] == "json" and params['Body'] != None:
        # if params['parameterType'] == "json" and params['Body'] != None:
            if params["Body"] != None or params["Body"] != "":
                # 替换faker变量
                request_body_str = resolve_faker_var(init_faker_var=params["Body"])
                # 替换自定义函数function变量
                request_body_str = resolve_func_var(init_func_var=params["Body"])
                # 全局替换
                request_body_str = replace_global_var_for_str(
                            init_var_str=request_body_str,
                            global_var_dic=global_vars,
                            )
                # 替换requestBody中的Number类型(去除引号)
                request_body_str = replace_global_var_for_str(
                            init_var_str=request_body_str,
                            global_var_dic=global_vars,
                            global_var_regex=r'\'\$num{.*?}\'',
                            match2key_sub_string_start_index=6,
                            match2key_sub_string_end_index=-2,
                            )
                # 替换 需要去除引号的 int变量
                request_body_str = resolve_int_var(init_int_str=request_body_str)
                params["Body"] = ast.literal_eval(request_body_str)

        if type(params["Headers"]) == str and params["Headers"] != "":
            params["Headers"] = eval(params["Headers"])
        elif type(params["Headers"]) == list:
            params["Headers"] = eval(str(params["Headers"])[1:-1])
            # return False
        else:
            params["Headers"] = {}



        if "parameterType" in params and params["parameterType"] == "form" or params["parameterType"] == "form-data":
            response = session.request(
                url=params["route"],
                method=params["Method"],
                data=params["Body"],
                headers=params["Headers"],
                verify=False
                )
        elif "parameterType" in params and params["parameterType"] == "file" or params["parameterType"] == "files":
            # 保证 Body 不能为 Null
            # print("打印 - filePath  ---> ", params["filePath"])
            if params["Body"] == None or params["Body"] == "":
                params["Body"] = {}
            else:
                params["Body"] = eval(params["Body"])
            try:
                response = session.request(
                    url=params["route"],
                    method=params["Method"],
                    data=params["Body"],
                    headers=params["Headers"],
                    files=Open_Upfiles(params["filePath"]),
                    verify=False
                )
            except BaseException as e:
                print("Body转换成 form-data 可能出错了, 需要检查参数", e)
        else:
            response = session.request(
                url=params["route"],
                method=params["Method"],
                json=params["Body"],
                headers=params["Headers"],
                verify=False
                )
        returned_data["elapsedSeconds"] = round(response.elapsed.total_seconds(), 3)
        returned_data["responseStatusCode"] = response.status_code
        try:
            response_json = json.loads(response.text) if isinstance(
                response.text, str
                ) and response.text.strip() else {}

            returned_data["responseData"] = response_json

            # 保存临时变量
            if "setGlobalVars" in params and params["setGlobalVars"] not in ["", None] and params["redis"] != None:
                tempParams = set_global(params["setGlobalVars"], response_json)
                _Cache(**params["redis"]).save_GlobalParams(params["object_id"], tempParams)

        except BaseException as e:
            # 如果出现异常，表示接口返回格式不是json
            returned_data["responseData"] = response.text
            print("用例ID: ", params["object_id"])
            print("如果出现异常，表示接口返回格式不是json，以后再优化处理")

        # ==========================================
        # 校验控制
        # ==========================================
        if params["checkoptions"]:
            # checkSpendSeconds 校验处理
            if params["checkSpendSeconds"] != None and params["checkSpendSeconds"] > 0:
                check_spend_seconds = float(params["checkSpendSeconds"])
                returned_data["checkSpendSeconds"] = check_spend_seconds

            # checkResponseCode 校验处理
            if "checkResponseCode" in params and params["checkResponseCode"] not in ["", None]:
                check_response_code = params["checkResponseCode"]
                returned_data["checkResponseCode"] = check_response_code

            # checkResponseBody 校验处理
            if "checkResponseBody" in params and params["checkResponseBody"] not in [[], {}, "", None]:
                if not isinstance(params["checkResponseBody"], list):
                    raise TypeError("checkResponseBody must be list！")
                need_check_response_body = False
                for index, check_item in enumerate(params["checkResponseBody"]):
                    if not isinstance(check_item, dict) or "regex" not in check_item or "query" not in check_item or \
                            not isinstance(check_item["regex"], str) or not isinstance(check_item["query"], list):
                        raise TypeError("checkResponseBody is not valid!")
                    # 对校验结果进行全局替换
                    if len(check_item["regex"]) > 0:
                        need_check_response_body = True
                        params["checkResponseBody"][index]["regex"] = replace_global_var_for_str(
                            init_var_str=check_item["regex"], global_var_dic=global_vars) if check_item.get(
                            "regex") and isinstance(check_item.get("regex"), str) else ""  # 警告！python判断空字符串为False
                        if check_item.get("query") and isinstance(check_item.get("query"), list):
                            params["checkResponseBody"][index]["query"] = replace_global_var_for_list(
                                init_var_list=check_item["query"], global_var_dic=global_vars)
                if need_check_response_body:
                    check_response_body = params["checkResponseBody"]
                    returned_data["checkResponseBody"] = check_response_body



            # 结果导出
            if check_spend_seconds and check_spend_seconds < returned_data['elapsedSeconds']:
                returned_data["status"] = "failed"
                returned_data["Conclusion"].append(
                    {"resultType": resp_status.get(1),
                        "reason": "请求超时, 期待耗时: %s s, 实际耗时: %s s。\t" % (
                            check_spend_seconds, returned_data["elapsedSeconds"])})
                return returned_data

            if check_response_code and not str(returned_data["responseStatusCode"]) == str(check_response_code):
                returned_data["status"] = "failed"
                returned_data["Conclusion"].append(
                    {"resultType": resp_status.get(1),
                        "reason": "响应状态码错误, 期待值: <%s>, 实际值: <%s>。\t" % (check_response_code, returned_data["responseStatusCode"])})
                return returned_data

            if check_response_body:
                for check_item in check_response_body:
                    regex = check_item["regex"]
                    query = check_item["query"]
                    real_value = dict_get(response.text, query)

                    if real_value is None:
                        returned_data["status"] = "failed"
                        returned_data["Conclusion"].append(
                            {"resultType": resp_status.get(1),
                                "reason": "未找到匹配的正则校验的值(查询语句为: %s), 服务器响应为: %s" % (query, response.text)})
                        return returned_data
                    result = re.search(regex, str(real_value))  # python 将regex字符串取了r""(原生字符串)

                    if not result:
                        returned_data["status"] = "failed"
                        returned_data["Conclusion"].append({
                                "resultType": resp_status.get(1),
                                "reason": "判断响应值错误(查询语句为: %s),\
                                响应值应满足正则: <%s>, 实际值: <%s> (%s)。\
                                (正则匹配时会将数据转化成string)\t"
                                % (query, regex, real_value, type(real_value))
                                })
            if returned_data["status"] == "pass":
                returned_data["Conclusion"].append({"resultType": resp_status.get(0), 'reason': '测试通过'})

        # 如果链接 redis 或 Mysql 出错，直接测试失败
        if check_connect_redis == False:
            returned_data["status"] = "failed"
            returned_data["Conclusion"].append(
                {"resultType": resp_status.get(1),
                "reason": "连接 Redis 主机没有反应，尝试连接失败。"}
            )

        if check_connect_mysql == False:
            returned_data["status"] = "failed"
            returned_data["Conclusion"].append(
                {"resultType": resp_status.get(1),
                "reason": "连接 Mysql 主机没有反应，尝试连接失败。"}
            )

        if not returned_data["Conclusion"]:
            returned_data["status"] = "pass"
            returned_data["Conclusion"].append({"resultType": resp_status.get(0),'reason': '测试通过'})

        returned_data["test_CaseDetail"] = [{
                "url": params["route"],
                "requestMethod": params["Method"],
                "requestBody": params["Body"],
            }]
        # returned_data["delaySeconds"] = "延时请求"
        # returned_data["dataInitResult"] = "数据初始化结果"
    else:
        return None
    return returned_data


def Open_Upfiles(_file):
    # 返回:
    #     [
    #       {"file": "test.txt", "name": "文件的上传名字叫啥", "Content-Type": "文件内容默认为Null"},
    #       {"file": "AAAAA.txt", "name": "ccccc", "Content-Type": Null}
    #     ]
    Open_list = []
    try:
        from settings import Config
        files = lambda name, file:('files',(name, open(
            Config.UPLOAD_PATH +"/"+ Config.UPLOAD_FOLDER +"/"+ file,'rb')))
        for _ in range(len(_file)):
            Open_list.append(files(_file[_].get("name"), _file[_].get("file"), _file[_].get("Content-Type")))
        return Open_list
    except BaseException as e:
        return None

