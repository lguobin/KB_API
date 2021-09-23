import time
from flask import jsonify, Blueprint, request
from werkzeug.security import check_password_hash
from app.models import *
from app.common.helper import *
from app.common.notify import send_email
from app.common.decorator import jwt_role, jwt_encode, current_identity
from settings import Config
from sqlalchemy import desc, and_


_user = Blueprint("_user", __name__)


@_user.route('/register', methods=['GET', 'POST'])
def register():
    """
    {
        "user":"admin",
        "password":"admin",
        "role_id":1,
        "nickname":"",
        "email":""
    }
    """
    try:
        require_items = get_post_items(request,
                                       Users.REQUIRE_ITEMS,
                                       throwable=True)
        option_items = get_post_items(request, Users.OPTIONAL_ITEMS)
        require_items.update(option_items)
        require_items["nickname"] = require_items.get("user")
        require_items["role_id"] = 0

        _temp = get_model_by(Users, user=require_items.get("user"))
        if _temp != None:
            return jsonify({'status': 'failed', 'msg': '名字已存在'})

        if require_items.get("password") and len(require_items.get("password")) <= 6:
            return jsonify({'status': 'failed', 'data': '密码长度至少要 6 位数以上'})

        if Config.USER_REGISTER_SENDEMAIL:
            send_email(
                [require_items.get("email")], 
                Config.REGISTER_SUBJECT,
                Config.REGISTER_CONTENT
            )
            require_items.update({"confirm": True})
        else:
            require_items.update({"confirm": True})

        _model = create_model(Users, **require_items)
        return jsonify({'status': 'ok', 'register':'已授权登录', 'object_id': _model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '注册用户错误 %s' % e})


# 激活用户
@_user.route('/activate/<token>', methods=['GET'])
def activate(token):
    print(1111111111111111111111111)
    return jsonify(data="激活成功 请登录")


# 获取用户信息
@_user.route('/getuser/<object_id>', methods=['GET'])
@jwt_role()
def getuser(object_id):
    _model = get_model(Users, object_id)
    if _model != None:
        return jsonify({
            'status': 'ok',
            'user_object_id': _model.object_id,
            'user': _model.user,
            'nickname': _model.nickname,
            'email': _model.email,
            'role_id': _model.role_id,
        })
    else:
        return jsonify({'status': 'failed', 'data': '获取用户信息错误, 用户不存在或已停用'})


@_user.route('/modify/<object_id>', methods=['PUT'])
@jwt_role()
def modify(object_id):
    """
    {
        "password":"admin",
        "nickname":"",
        "email":""
    }
    """
    try:
        _model = get_model(Users, object_id)
        if _model != None:
            password = get_post_data(request, "password", throwable=True)
            nickname = get_post_data(request, "nickname", throwable=True)
            email = get_post_data(request, "email", throwable=True)

            if password and len(password) >= 6:
                _model.password = password
            else:
                return jsonify({'status': 'failed', 'data': '密码长度至少要 6 位数以上'})

            if nickname:
                _model.nickname = nickname
            if email:
                _model.email = email
            update_models(_model)
            return {
                "object_id": object_id,
            }
        else:
            return jsonify({'status': 'failed', 'data': '获取用户错误, 用户不存在或已停用'})

    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})


@_user.route('/login', methods=['GET', 'POST'])
def login():
    loginjson = request.get_json(force=True)
    if loginjson == None or loginjson == {}:
        return jsonify(msg="未找到可用参数")
    user = loginjson.get("user")
    password = loginjson.get("password")

    print("登录信息 ：", user, password)

    if user != None and password != None:
        if len(user) == 0 or len(password) == 0:
            return jsonify(msg='请输入正确的用户名或密码')

        _userInfo = Users.query.filter(Users.user == user).first()  # Manager仅作为示例
        if not _userInfo:
            return jsonify(code='2100', msg='未找到用户')

        if _userInfo.confirm == False and _userInfo.role_id == None:
            return jsonify(code='2100', msg='用户未激活或已禁用')

        if not check_password_hash(_userInfo._password, password):
            return jsonify(code='2100', msg='密码错误')

        token = jwt_encode({
            'object_id':  _userInfo.object_id,
            'name': _userInfo.user,
            'role': _userInfo.role_id
        })

        _userInfo.token = str(token)
        _userInfo.login_at = int(time.time())
        update_models(_userInfo)
        return jsonify({'status':'ok', 'access_token': token})
    else:
        return jsonify(code='2100', msg="请填写用户名或密码")


@_user.route('/token/update', methods=['POST'])
@jwt_role()
def update_token():
    _userInfo = Users.query.filter(
        and_(
        Users.user == current_identity.get('name'),
        Users.confirm == True,
        Users.role_id != None,
        )).first()

    if _userInfo != None:
        token = jwt_encode({
            'object_id':  _userInfo.object_id,
            'name': _userInfo.user,
            'role': _userInfo.role_id
        })
        return jsonify({'status':'ok', "token_Up": token})
    else:
        return jsonify(code='2100', msg='用户不存在或已停用')


@_user.route('/logout', methods=['GET'])
def logout():
    print("JWT 没有主动注销的说法")
    return jsonify({'status':'ok', 'access_token': "没有主动注销的说法, 以后再加入 redis"})


@_user.route('list', methods=['GET','PUT'])
@jwt_role("admin")
def User_Management():
    try:
        _request = request.get_json()
        if _request == None:
            page = get_page_value(request)
            per_page = get_per_page_value(request, Config.PER_PAGE, Config.MAX_PER_PAGE)
            paging = get_query_data(request, "paging", 1)
            filter_params = [Users.state == Users.STATE_NORMAL]
            if bool(int(paging)):
                pagination = get_models_filter_with_pagination(Users, None, page, per_page, desc, *filter_params)
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

        elif _request.get("Option") == "adduser" and _request.get("adduser") != None:
            _adduser = _request.get("adduser")
            _model = create_model(Users, **_adduser)
            return {"object_id": _model.object_id}


        elif _request.get("object_id") != None:
            __object = _request.get("object_id")
            _model = get_model(Users, __object)
            if _model is None:
                return jsonify({'status': 'failed', 'data': '删除不存在的对象'})


            elif _request.get("Option") == "modifyuser":
                _adduser = _request.get("modifyuser")
                password = _adduser.get("password")
                nickname = _adduser.get("nickname")
                role_id = _adduser.get("role_id")
                email = _adduser.get("email")
                if password and len(password) >= 6:
                    _model.password = password
                else:
                    return jsonify({'status': 'failed', 'data': '密码长度至少要 6 位数以上'})
                if nickname:
                    _model.nickname = nickname
                if email:
                    _model.email = email
                _model.role_id = role_id
                update_models(_model)
                return {
                    "object_id": __object,
                }

            elif _request.get("Option") == "delete":
                _model.state = 1
                _model.confirm = False
                update_models(_model)
                return jsonify({'status': 'ok', 'data': '用户已被清理'})

            elif _request.get("Option") == "reset_password":
                _model.password = Config.RESET_Password
                update_models(_model)
                return jsonify({'status': 'ok', 'data': '重置密码为: %s' %Config.RESET_Password})

            elif _request.get("Option") == "role":
                _model.role = _request.get("role")
                update_models(_model)
                return jsonify({'status': 'ok', 'data': '权限分配成功'})

            else:
                return jsonify({'status': 'failed', 'data': 'Option 参数找不到对应的方法'})
        else:
            return jsonify({'status': 'failed', 'data': '传入用户参数不对'})

    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})


@_user.route('/search', methods=['GET'])
@jwt_role()
def searchData():
    try:
        search_data = request.args
        q = search_data.get("q")
        _userResults = None
        if q != None and q != "":
            results =  get_like(Users, q)
            _userResults = {
                "results": [{results[index].object_id: results[index].user} for index in range(len(results))]
                }
        return jsonify({
            "status": "ok",
            "userlist": _userResults,
         })
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})

