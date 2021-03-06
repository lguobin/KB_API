# decorator.py
import jwt
from datetime import datetime
from functools import wraps
from threading import Thread
from werkzeug.local import LocalProxy
from flask import request, jsonify, _request_ctx_stack, current_app, g

def async_test(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
        return f
    return wrapper



# 原文链接：https://blog.csdn.net/weixin_43262264/article/details/108628334
# LocalProxy的使用说明，很好的一篇文章:https://www.jianshu.com/p/3f38b777a621
current_identity = LocalProxy(
    lambda: getattr(_request_ctx_stack.top, 'current_identity', None))
#
# headers 加入 Authorization: JWT + token
#


def jwt_payload(identity):
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    token = {'exp': exp, 'iat': iat, 'identity': identity}
    return token


def jwt_encode(identity):
    secret = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

    payload = jwt_payload(identity)
    missing_claims = list(set(required_claims) - set(payload.keys()))

    if missing_claims:
        raise RuntimeError('Payload is missing required claims: %s' %
                           ', '.join(missing_claims))
    return jwt.encode(payload, secret, algorithm=algorithm, headers=None)


def jwt_decode(token):
    secret = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    leeway = current_app.config['JWT_LEEWAY']

    verify_claims = current_app.config['JWT_VERIFY_CLAIMS']
    required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

    options = {'verify_' + claim: True for claim in verify_claims}
    options.update({'require_' + claim: True for claim in required_claims})
    token_decode = jwt.decode(token,
                              secret,
                              options=options,
                              algorithms=[algorithm],
                              leeway=leeway)
    return token_decode


# 权限控制
def jwt_role(role=None):
    def _role(func):
        @wraps(func)
        def _re(*args, **kwargs):
            auth_header_value = request.headers.get('Authorization', None)
            if not auth_header_value:
                return jsonify(status='failed', data='Authorization缺失')

            parts = auth_header_value.split()
            if len(parts) == 1:
                return jsonify(status='failed', data='Token缺失')  # code 仅作为示例

            elif len(parts) > 2:
                return jsonify(status='failed', data='Token无效')

            token = parts[1]
            if token is None:
                return jsonify(status='failed', data='Token异常')

            try:
                payload = jwt_decode(token)
            except jwt.InvalidTokenError as e:
                return jsonify(status='failed', data=str(e))

            _request_ctx_stack.top.current_identity = payload.get('identity')

            identity = payload.get('identity')
            if identity is None:
                return jsonify(status='failed', data='用户不存在或已停用')

            g.user = identity.get("name")
            g.user_object_id = identity.get("object_id")
            if role == 'admin':
                if identity.get("role") == 1:
                    return func(*args,**kwargs)
                else:
                    return jsonify(status='failed', data='Permission Denied')
            else:
                return func(*args,**kwargs)

        return _re
    return _role

