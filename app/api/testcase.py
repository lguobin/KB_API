from flask import jsonify, Blueprint, request, g
from app.common.decorator import jwt_role
from app.models import *
from app.common.helper import *



tcase = Blueprint("tcase", __name__)



@tcase.route('/tcase/<object_id>', methods=['GET'])
@jwt_role()
def tcase_details(object_id):
    _model = get_model(TestCase, object_id)
    if _model != None:
        return jsonify({'status': 'ok', 'object_id':_model.get_json()})
    else:
        return jsonify({'status': 'failed', 'data':'找不到用例'})


@tcase.route('/addcase', methods=['POST'])
@jwt_role()
def addcase():
    """
    {
        "name":"测试用例AAA",
        "pid":"归属项目",
        "Iid":"归属接口",
        "route":"/shopadm/auth/shop-token",
        "headers":[
            {
                "Content-Type":"application/json"
            }
        ],
        "requestMethod":"POST",
        "requestBody":[
            {
                "auth_type":"pwd",
                "username":"testadminwuyling",
                "password":"123456",
                "noncestr":"DQdwmgUBSPiLdYJB",
                "validation":1,
                "timestamp":1628042818,
                "vs":"984265d028fed3507e759eb3eadec944"
            }
        ],

        "setGlobalVars": [],

        "checkoptions": 0,
        "checkSpendSeconds":"",
        "checkResponseCode":"",
        "checkResponseBody":"",
        "checkResponseNumber":"",

        "optionsValue":"",
        "generate_params":"",
        "delay":1,
        "variable_1":"",
        "variable_2":"",
        "uid":"张三",
        "description":"测试用例",
        "parameterType":"json",
        "filePath":"pwd"
    }
    """
    try:
        require_items = get_post_items(request, TestCase.REQUIRE_ITEMS, throwable=True)
        option_items = get_post_items(request, TestCase.OPTIONAL_ITEMS)
        require_items.update(option_items)
        require_items.update({"uid": g.user_object_id})

        if type(require_items["headers"]) == list:
            require_items["headers"] = str(require_items["headers"])[1:-1]

        if type(require_items["requestBody"]) == list:
            require_items["requestBody"] = str(require_items["requestBody"])[1:-1]


        _model = get_models_filter(TestCase, TestCase.name == require_items["name"])
        if _model != []:
            return jsonify({'status': 'failed', 'data': '名字已存在'})
        case_model = create_model(TestCase, **require_items)
        return jsonify({'status': 'ok', 'object_id':case_model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '新建失败%s' % e})


@tcase.route('/putcase/<object_id>', methods=['PUT'])
@jwt_role()
def putcase(object_id):
    """
    {
        "name":"测试用例AAA",
        "uid":"张三",
        "pid":"归属项目",
        "Iid":"归属接口",
        "route":"/shopadm/auth/shop-token",
        "headers":[],
        "requestMethod":"POST",
        "requestBody":[],

        "setGlobalVars": [],

        "checkSpendSeconds":"",
        "checkResponseCode":"",
        "checkResponseBody":"",
        "checkResponseNumber":"",

        "checkoptions": 0,
        "optionsValue":"",
        "generate_params": 0,
        "delay":1,
        "variable_1":"",
        "variable_2":"",
        "description":"测试用例",
        "parameterType":"json",
        "filePath":"PWD"
    }
    """
    try:
        _model = get_model(TestCase, object_id)
        name = get_post_data(request, "name", throwable=True)
        uid = get_post_data(request, "uid", throwable=True)
        pid = get_post_data(request, "pid", throwable=True)
        Iid = get_post_data(request, "Iid", throwable=True)
        route = get_post_data(request, "route", throwable=True)
        headers = get_post_data(request, "headers", throwable=True)
        
        requestMethod = get_post_data(request, "requestMethod", throwable=True)
        requestBody = get_post_data(request, "requestBody", throwable=True)

        setGlobalVars = get_post_data(request, "setGlobalVars", throwable=True)

        checkResponseBody = get_post_data(request, "checkResponseBody", throwable=True)
        checkResponseCode = get_post_data(request, "checkResponseCode", throwable=True)
        checkSpendSeconds = get_post_data(request, "checkSpendSeconds", throwable=True)
        checkoptions = get_post_data(request, "checkoptions", throwable=True)
        optionsValue = get_post_data(request, "optionsValue", throwable=True)
        generate_params = get_post_data(request, "generate_params", throwable=True)
        variable_1 = get_post_data(request, "variable_1", throwable=True)
        variable_2 = get_post_data(request, "variable_2", throwable=True)

        delay = get_post_data(request, "delay", throwable=False)
        description = get_post_data(request, "description", throwable=True)
        parameterType = get_post_data(request, "parameterType", throwable=True)
        filePath = get_post_data(request, "filePath", throwable=True)


        if type(headers) == list:
            headers = str(headers)[1:-1]

        if type(requestBody) == list:
            requestBody = str(requestBody)[1:-1]

        _model.name = name
        _model.uid = uid
        _model.pid = pid
        _model.Iid = Iid

        _model.route = route
        _model.headers = headers
        _model.requestMethod = requestMethod
        _model.setGlobalVars = setGlobalVars
        _model.requestBody = requestBody

        _model.checkoptions = checkoptions
        _model.checkResponseBody = checkResponseBody
        _model.checkResponseCode = checkResponseCode
        _model.checkSpendSeconds = checkSpendSeconds

        _model.optionsValue = optionsValue
        _model.generate_params = generate_params

        _model.delay = delay
        _model.variable_1 = variable_1
        _model.variable_2 = variable_2
        _model.description = description
        _model.parameterType = parameterType
        _model.filePath = filePath

        update_models(_model)
        return {
            'status': 'ok',
            "object_id": object_id,
        }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '修改错误%s' % e})


@tcase.route('/delcase/<object_id>', methods=['DELETE'])
@jwt_role()
def delcase(object_id):
    """
    {}
    """
    try:
        _model = get_model_by(TestCase, object_id=object_id)
        if _model is None:
            return jsonify({'status': 'failed', 'data': '删除不存在的对象'})
        delete_model(TestCase, object_id)
        return {
            "status": "ok",
            "object_id": object_id,
        }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '删除错误%s' % e})

