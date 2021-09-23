from sqlalchemy import desc
from settings import Config
from flask import jsonify, Blueprint, request
from app.common.decorator import jwt_role
from app.models import *
from app.common.helper import *


inter = Blueprint("inter", __name__)


@inter.route('/addinter', methods=['POST'])
@jwt_role()
def add_inter():
    """
    {
        "name":"测试名称",
        "pid":"所属项目",
        "i_type":"http",
        "route":"/shopadm/auth/shop-token",
        "headers":"{}",
        "requestMethod":"POST",
        "delay":0,
        "uid":"1@1.cn",
        "description":"测试名称"
    }
    """
    try:
        require_items = get_post_items(request, Interfaces.REQUIRE_ITEMS, throwable=True)
        option_items = get_post_items(request, Interfaces.OPTIONAL_ITEMS)
        _model = get_models_filter(Interfaces, Interfaces.name == require_items["name"])
        require_items.update(option_items)
        if _model != []:
            return jsonify({'status': 'failed', 'msg': '名字已存在'})
        inter_model = create_model(Interfaces, **require_items)
        return jsonify({'status': 'ok', 'object_id':inter_model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '新建失败 %s' % e})


@inter.route('/putinter/<object_id>', methods=['PUT'])
@jwt_role()
def put_inter(object_id):
    """
    {
        "name":"测试名称",
        "pid":"所属项目",
        "i_type":"http",
        "route":"/shopadm/auth/shop-token",
        "headers":"{}",
        "requestMethod":"POST",
        "delay":1,
        "uid":"1@1.cn",
        "description":"测试名称"
    }
    """
    try:
        _model = get_model(Interfaces, object_id)

        name = get_post_data(request, "name", throwable=True)
        uid = get_post_data(request, "uid", throwable=True)
        pid = get_post_data(request, "pid", throwable=True)

        i_type = get_post_data(request, "i_type", throwable=True)
        route = get_post_data(request, "route", throwable=True)
        headers = get_post_data(request, "headers", throwable=True)
        if headers == None or headers == "":
            headers = {"Accept": "application/json","Content-Type":"application/json"}

        requestMethod = get_post_data(request, "requestMethod", throwable=True)
        delay = get_post_data(request, "delay", throwable=False)

        description = get_post_data(request, "description", throwable=True)

        _model.name = name
        _model.uid = uid
        _model.pid = pid
        _model.i_type = i_type
        _model.route = route
        _model.headers = headers
        _model.requestMeth = requestMethod
        _model.delay = delay
        _model.description = description

        update_models(_model)
        return {
            "object_id": object_id,
        }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '修改错误%s' % e})


@inter.route('/deleteinter/<object_id>', methods=['DELETE'])
@jwt_role()
def delete_inter(object_id):
    """
    {}
    """
    try:
        _model = get_model_by(Interfaces, object_id=object_id)
        if _model is None:
            return jsonify({'status': 'failed', 'data': '删除不存在的对象'})
        delete_model(Interfaces, object_id)
        return {}
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '删除错误%s' % e})



@inter.route('/checkcase/<object_id>', methods=['GET'])
@jwt_role()
def checkcase(object_id):
    """
    {}
    """
    try:
        page = get_page_value(request)
        per_page = get_per_page_value(request, Config.PER_PAGE, Config.MAX_PER_PAGE)
        paging = get_query_data(request, "paging", 1)
        filter_params = [TestCase.state == TestCase.STATE_NORMAL, TestCase.Iid == object_id]
        if bool(int(paging)):
            pagination = get_models_filter_with_pagination(TestCase, "", page, per_page, desc, *filter_params)

            total = pagination['total']
            models = pagination['models']
            data = [model.get_json() for model in models]
            return {
                'total': total,
                'page': page,
                'pages': get_pages(total, per_page),
                'per_page': per_page,
                'results': data
            }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})
