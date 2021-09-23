import csv
from itertools import islice
from io import StringIO, BytesIO
from app.models import *
from app.common.helper import *
from app.common.decorator import jwt_role
from app.common.globalParams import _Cache
from flask import render_template, jsonify, Blueprint, request, Response, stream_with_context, send_file



common = Blueprint("common", __name__)



@common.route('/', methods=['GET'])
@common.route('s', methods=['GET'])
def doc_API():
    # print("API 说明文档")
    return render_template("apis.html")


@common.route('/<function>', methods=['GET'])
@jwt_role()
def GetPages(function=None):
    try:
        if function == "email":
            return jsonify(Pages(request, Email))
        elif function == "env":
            return jsonify(Pages(request, EnvConfig))
        elif function == "project":
            return jsonify(Pages(request, Project))
        elif function == "inters":
            return jsonify(Pages(request, Interfaces))
        elif function == "tcase":
            return jsonify(Pages(request, TestCase))
        elif function == "report":
            return jsonify(Pages(request, TestReport))
        elif function == "cronjob":
            return jsonify(Pages(request, CronJob))
        elif function == "scene":
            return jsonify(Pages(request, Scenes))
        else:
            return jsonify({
                    'status': 'failed',
                    'msg': '请求分页出错或不存在',
                })
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取分页数据出错误 %s' %e})


@common.route('/search', methods=['GET'])
@jwt_role()
def searchData():
    try:
        search_data = request.args
        q = search_data.get("q")
        _projResults = None
        _interResults = None
        _caseResults = None
        _envResults = None

        if q != None and q != "":
            results =  get_like(EnvConfig, q)
            _envResults = {
                "results": [{results[index].object_id:results[index].name} for index in range(len(results))]
            }

            results =  get_like(Project, q)
            _projResults = {
                "results": [{results[index].object_id:results[index].name} for index in range(len(results))]
            }

            results =  get_like(Interfaces, q)
            _interResults = {
                "results": [{results[index].object_id:results[index].name} for index in range(len(results))]
            }

            results =  get_like(TestCase, q)
            _caseResults = {
                "results": [{results[index].object_id:results[index].name} for index in range(len(results))]
            }
        return jsonify({
            "status": "ok",
            "results": {
                "ENVConfig": _envResults,
                "Project":  _projResults,
                "interface": _interResults,
                "TestCase": _caseResults,
            }
        })

    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})


# 搜索指定分类报告
@common.route('/searchreport', methods=['GET'])
@jwt_role()
def search_report():
    return_NULL = {"report": [], "status": "ok"}
    try:
        search_data = request.args
        if search_data.get("Project") != None and search_data.get("Project") != "":
            _model = get_models(TestReport, Project_id=search_data.get("Project"))
            if _model != None:
                return jsonify({
                    'status': 'ok',
                    'report': [get_TestReport(_model[x]) for x in range(len(_model))],
                    })
            else:
                return return_NULL

        elif search_data.get("executionMode") != None and search_data.get("executionMode") != "":
            _model = get_models(TestReport, executionMode=search_data.get("executionMode"))
            if _model != None:
                return jsonify({
                    'status': 'ok',
                    'report': [get_TestReport(_model[x]) for x in range(len(_model))],
                    })
            else:
                return return_NULL

        elif search_data.get("uid") != None and search_data.get("uid") != "":
            _model = get_models(TestReport, uid=search_data.get("uid"))
            if _model != None:
                return jsonify({
                    'status': 'ok',
                    'report': [get_TestReport(_model[x]) for x in range(len(_model))],
                    })
            else:
                return return_NULL
        else:
            return return_NULL

    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})


@common.route('/<env_object_id>/globalParams', methods=['GET'])
@jwt_role()
def getparams(env_object_id):
    try:
        _model = get_model_by(EnvConfig, object_id=env_object_id)
        if _model != None:
            return jsonify({
                    "status": "ok",
                    "globalParams": _Cache(**_model.redis).get_GlobalParams(),
                })
        else:
            return jsonify({"msg": "该环境变量未启用 Redis 设置, 也就没有全局变量"})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取错误 %s' % e})


@common.route('/<env_object_id>/globalParams', methods=['POST'])
@jwt_role()
def addparams(env_object_id):
    try:
        _model = get_model_by(EnvConfig, object_id=env_object_id)
        if _model != None:
            data = request.get_json(force=True)
            params_name = data.get("name")
            params_val = data.get("value")
            uid = data.get("uid")
            if params_name != None and uid != None:
                # _name = "手动添加_%s_%s_%s" %(params_name, uid, str(timestamp()))
                _name = "手动添加_%s_%s" %(params_name, uid)
                _Cache(**_model.redis).save_GlobalParams(_name, {params_name:params_val})
                return jsonify({"status": "ok", "data": "添加完成"})
            else:
                return jsonify({"status": "failed", "data": "参数错误，缺少必要参数"})
        else:
            return jsonify({"msg": "该环境变量未启用 Redis 设置, 也就没有全局变量"})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '添加错误 %s' % e})


@common.route('/export_csvDemo', methods=['GET', 'POST'])
def export_csvDemo():
    def generate():
        string_io = StringIO()
        user_data = [
            ["接口名称（接口不存则会自动创建）", "用例名称", "用例描述", "请求协议", 
            "请求域名", "请求接口地址", "请求头部", "请求方式", "请求参数", 
            "请求参数类型（默认为json）", "设置全局变量", 
            "是否断言（默认为false）", "检查是否在规定时间内响应", 
            "检查响应代码", "检查响应体", "创建人"
            ],
            [
                "登录", "登录测试", "就是个例子", 
                "HTTP", "http://0.0.0.0", "/user/login", 
                '{"Content-Type": "application/json"}', 
                'POST', "{'test':'test'}", "json",
                [{"name": "BBB", "query": ["msg"]}], 
                "Y", "0.3", [{"query": ["msg"], "regex": "msg"}], "200", "屎三香"
            ],
        ]
        w = csv.writer(string_io)
        for i in user_data:
            # writer
            w.writerow(i)
            yield string_io.getvalue()
            string_io.seek(0)
            string_io.truncate(0)
    response = Response(stream_with_context(generate()), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="TestCase_Demo.csv")
    return response
    # return send_file(response, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@common.route('/<pid>/inputTestCases', methods=['POST'])
@jwt_role()
def input_test_cases(pid):
    try:
        file = request.files.get("files")
        stream = StringIO(file.stream.read().decode(), newline=None)
        file_content = csv.reader(stream)
        for row in  islice(file_content, 1, None):
            input_files(pid, *row)
        return jsonify({"msg": "导入成功"})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '导入失败，原因: %s' %e})