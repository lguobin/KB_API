from flask import jsonify, Blueprint, request
from sqlalchemy.sql.expression import intersect
from app.common.decorator import jwt_role

from app.models import *
from app.extensions import db

from app.common.helper import *
from app.common.helper import get_post_items
from app.common.helper import create_model
from sqlalchemy import desc
from settings import Config

email = Blueprint("email", __name__)



@email.route('/addemail', methods=['POST'])
@jwt_role()
def addemail():
    """
    {"uid":"1@1.cn","name":"测试组","email":"通过该邮箱发送","mailGroup":"['邮箱地址 - A', '邮箱地址 - B']"}
    """
    try:
        require_items = get_post_items(request, Email.REQUIRE_ITEMS, throwable=True)
        option_items = get_post_items(request, Email.OPTIONAL_ITEMS)
        require_items.update(option_items)
        _model = get_models_filter(Email, Email.name == require_items["name"])
        if _model != []:
            return jsonify({'status': 'failed', 'msg': '名字已存在'})
        _model = create_model(Email, **require_items)
        return jsonify({'status': 'ok', 'object_id':_model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '新建失败 %s' % e})


@email.route('/putemail/<object_id>', methods=['PUT'])
@jwt_role()
def putemail(object_id):
    """
    {"uid":"1@1.cn","name":"测试组","email":"通过该邮箱发送","mailGroup":"['邮箱地址 - A', '邮箱地址 - B']"}
    """
    try:
        _model = get_model(Email, object_id)

        name = get_post_data(request, "name", throwable=True)
        email = get_post_data(request, "email", throwable=True)
        mailGroup = get_post_data(request, "mailGroup", throwable=True)

        uid = get_post_data(request, "uid", throwable=True)
        description = get_post_data(request, "description", throwable=True)

        _temp = get_models_filter(Email, Email.name == name)
        if len(_temp) > 1:
            return jsonify({'status': 'failed', 'msg': '名字已存在'})

        _model.name = name
        _model.uid = uid
        _model.email = email
        _model.mailGroup = mailGroup
        _model.description = description
        update_models(_model)
        return jsonify({'status': 'ok', 'object_id':_model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '新建失败 %s' % e})


@email.route('/delemail/<object_id>', methods=['DELETE'])
@jwt_role()
def delemail(object_id):
    """
    {}
    """
    try:
        _model = get_model_by(Email, object_id=object_id)
        if _model is None:
            return jsonify({'status': 'failed', 'data': '删除不存在的对象'})
        delete_model(Email, object_id)
        return { "object_id": object_id}
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '删除错误%s' % e})

