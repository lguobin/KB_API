import time
from flask import make_response, jsonify, Blueprint, request
from app.models import *
from app.common.helper import *
from app.common.decorator import jwt_role


mock = Blueprint("mock", __name__)

request_method_list = [
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'
]


def get_mock_data(method, path, responseBody=None):
    try:
        if method not in request_method_list:
            raise ValueError("method should in {}".format(str(request_method_list)))
        res = {
            "delaySeconds" : 0.0,
            "isDeleted" : False,
            "status" : True,
            "category" : "Try_Mock_Server",
            "requestMethod" : method,
            "path" : path,
            "responseCode" : "200",
            "responseBody" : {},
        }
        mock_data = None
        if responseBody == None:
            res["responseBody"] = {"TryMock" : "OK"}
        else:
            res["responseBody"] = responseBody

        if res:
            mock_data = res
        if mock_data and 'responseBody' in mock_data and 'responseCode' in mock_data:
            return mock_data
        else:
            return None
    except BaseException as e:
        print(e)
        return e


@mock.route('/mock/<path:path>', methods=request_method_list)
@jwt_role()
def mock_call(path):
    try:
        if not path.startswith('/'):
            path = "/" + path
        method = request.method
        mock_data = get_mock_data(method, path, request.get_json(force=True))

        if mock_data:
            if 'delaySeconds' in mock_data and mock_data.get('delaySeconds') > 0:
                time.sleep(mock_data.get('delaySeconds'))
            return make_response(
                jsonify(mock_data.get('responseBody')), 
                mock_data.get('responseCode')
                )
        else:
            return make_response(jsonify({
                'status': 'failed',
                'data': 'TryMock不存在'
            }), 404)
    except BaseException as e:
        return make_response(jsonify({'status': 'failed',"error": str(e)}), 500)