from time import time
from flask import jsonify, Blueprint, request
from app.models import *
from app.common.helper import *
from app.common.decorator import jwt_role


report = Blueprint("report", __name__)


# 详情报告页
@report.route('/report/<object_id>', methods=['GET'])
@jwt_role()
def reportDetail(object_id):
    try:
        _model = get_model(TestReport, object_id)
        return jsonify(get_TestReport(_model))
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})


@report.route('/cleanReports', methods=['POST'])
@jwt_role()
def cleanReports():
    """
    {"cleanDate":0, "projectId":"6110e55b78f5bbbe3d9e2a6c","operator":"1@1.cn","executionMode":"cronJob"}
    {"cleanDate":30,"projectId":"6110e55b78f5bbbe3d9e2a6c","operator":"1@1.cn","executionMode":"cronJob"}
    """
    try:
        request_data = request.get_json(force=True)
        clean_date = request_data.get('cleanDate')

        # 参数未启用 - 先预留参数
        operator = request_data.pop('operator')
        project_id = request_data.get('projectId')
        execution_mode = request_data.get('executionMode')

        # 测试报告 - 时间戳
        TIMESTAMP = 86400

        if clean_date != None:
            if clean_date == 1:
                print("清除全部报告")
            elif clean_date > 1 and clean_date < 31:
                clean_date = int(time()) - ( TIMESTAMP * clean_date )
            else:
                return jsonify({'status': 'failed', 'data': '日期格式不对!'})
            _model = get_models_timestamp(TestReport, clean_date)
            if _model != []:
                for x in range(len(_model)):
                    if _model[x].state == 0:
                        delete_model(TestReport, _model[x].object_id)
                    else:
                        return jsonify({'status': 'ok', 'data': '未找到要删除的报告'})
                return jsonify({'status': 'ok', 'data': '删除报告成功'})
            else:
                return jsonify({'status': 'ok', 'data': '未找到要删除的报告'})
        else:
            return jsonify({'status': 'failed', 'data': '日期格式不对!'})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})
