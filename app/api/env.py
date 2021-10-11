from flask import jsonify, Blueprint, request
from app.models import *
from app.common.helper import *
from app.common.decorator import  jwt_role


env = Blueprint("env", __name__)


@env.route('/addenv', methods=['POST'])
@jwt_role()
def addenv():
    """
    {
        "name":"AAAAA",
        "projectTestType": 1,
        "domain":"http://test-api.inmeng.vip",
        "mysql":"",
        "redis":"",
        "uid":"张三",
        "description":"描述一大堆东西"
    }
    """
    try:
        require_items = get_post_items(request, EnvConfig.REQUIRE_ITEMS, throwable=True)
        option_items = get_post_items(request, EnvConfig.OPTIONAL_ITEMS)
        require_items.update(option_items)
        require_items.update({"uid": g.user_object_id})

        _model = get_models_filter(EnvConfig, EnvConfig.name == require_items["name"])
        if _model != []:
            return jsonify({'status': 'failed', 'data': '名字已存在'})

        _model = create_model(EnvConfig, **require_items)
        return jsonify({'status': 'ok', 'object_id':_model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '新建失败 %s' % e})


@env.route('/putenv/<object_id>', methods=['PUT'])
@jwt_role()
def putenv(object_id):
    """
    {
        "name":"AAAAA",
        "projectTestType": "1",
        "domain":"http://test-api.inmeng.vip",
        "mysql":"",
        "redis":"",
        "uid":"张三",
        "description":"描述一大堆东西"
    }
    """
    try:
        _model = get_model(EnvConfig, object_id)

        name = get_post_data(request, "name", throwable=True)
        projectTestType = get_post_data(request, "projectTestType", throwable=True)
        domain = get_post_data(request, "domain", throwable=True)

        mysql = get_post_data(request, "mysql", throwable=True)
        redis = get_post_data(request, "redis", throwable=True)
        uid = get_post_data(request, "uid", throwable=True)

        description = get_post_data(request, "description", throwable=True)

        _temp = get_models_filter(EnvConfig, EnvConfig.name == name)
        if len(_temp) > 1:
            return jsonify({'status': 'failed', 'data': '名字已存在'})

        _model.name = name
        _model.uid = uid
        _model.projectTestType = projectTestType
        _model.domain = domain
        _model.mysql = mysql
        _model.redis = redis
        _model.description = description
        update_models(_model)
        return {
            'status': 'ok',
            'object_id': object_id,
        }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '修改错误%s' % e})


@env.route('/delenv/<object_id>', methods=['DELETE'])
@jwt_role()
def delenv(object_id):
    """
    {}
    """
    try:
        _model = get_model_by(EnvConfig, object_id=object_id)
        if _model is None:
            return jsonify({'status': 'failed', 'data': '删除不存在的对象'})
        delete_model(EnvConfig, object_id)
        return {
            'status': 'ok',
            "object_id": object_id,
        }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '删除错误%s' % e})
