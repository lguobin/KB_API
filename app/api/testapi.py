from flask import jsonify, Blueprint, request
from app.models import *
from app.common.helper import *
from app.common.decorator import jwt_role
from app.common.notify import send_email
from app.common.session import send_and_save_report, send_and_save_report_BySuite


startAPI = Blueprint("startAPI", __name__)
_err = {'status': 'failed', 'data': '提交的数据存在找不到可用的[ 环境、项目、接口] 的参数'}



# 获取单步用例最后一次的结果
@startAPI.route('/DebugLastResult/<object_id>', methods=['GET'])
@jwt_role()
def test_case_last_manual_result(object_id):
    __model = get_model(TestCase, object_id)
    if __model == None:
        return jsonify({'status': 'failed', 'data': '找不到测试用例'})
    result = __model.responseBody
    return jsonify(
        {'status': 'ok', 'result': eval(result)}) if result != None and result != "" else \
        jsonify({'status': 'failed', 'data': '未找到用例或当前用例没有执行结果'})


@startAPI.route('/ByDebug', methods=['POST'])
@jwt_role()
def ByDebug():
    """
    {
        "CaseList":[
            "7a51834824a3456faf6e0135489ebc3f",
            "8c947bb9ac9c4ccab4b382c18644f2f0",
            "610cfcd215200abc48507cbb"
        ],
        "EnvId":"fce67bb495534c4d81152696885b44a1",
        "uid":"1@1.cn",
        "executionMode":"manual"
    }
    """
    # try:
    request_data = request.get_json(force=True)
    request_data.update({
        "executionMode": "manual",
    })

    EnvId = request_data.get("EnvId")
    CaseList = request_data.get("CaseList")

    execution_user = None
    execution_mode = None
    env_name = None
    env_domain = None
    env_mysql = None
    env_redis = None

    __caseList = composeCaseWorkshop(EnvId=EnvId, Tcase=CaseList)
    if __caseList == None:
        return _err

    send_and_save_report(__caseList)
    return jsonify({'status': 'ok', 'data': '测试完毕, 稍后前往「DebugLastResult」中获取结果'})
    # except BaseException as e:
    #     return jsonify({'status': 'failed', 'data': '状态错误%s' % e})


@startAPI.route('/ByInterface', methods=['POST'])
@jwt_role()
def ByInterface():
    """
    {
        "Interface":[
            "75cc456d9c4d41f6980e02f46d611a5c",
            "75cc456d9c4d41f6980e02f46d611a55"
        ],
        "EnvId":"9d289cf07b244c91b81ce6bb54f2d627",
        "ProjectId":"c3009c8e62544a23ba894fe5519a6b64",
        "uid":"1@1.cn",
        "executionMode":"manual"
    }
    """
    request_data = request.get_json(force=True)
    __ENV = request_data.get("EnvId")
    __Pid = request_data.get("ProjectId")
    __Inf = request_data.get("Interface")

    action = {
        "uid": request_data.get("uid"),
        "executionMode": "manual",
    }
    case = composeCaseWorkshop(EnvId=__ENV, ProjectId=__Pid, Interface=__Inf)
    if case == None:
        return _err

    send_and_save_report_BySuite(case, action=action)
    return jsonify({'status': 'ok', 'data': '测试完毕, 稍后前往「测试报告」查看结果'})


