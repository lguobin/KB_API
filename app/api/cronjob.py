from flask import jsonify, Blueprint, request
from app.common.decorator import jwt_role
from app.models import *
from app.models.base import timestamp
from app.extensions import cron_manager
from app.common.helper import *
from app.common.helper import get_post_items
from app.common.helper import create_model



cron = Blueprint("cron", __name__)


def Run_Times(**require_items):
    # 小于 12 小时 一律不允许保存
    if require_items.get("triggerType") == "interval" and require_items.get("interval") <= 43200:
        return {'status': 'failed', 'data': '新建失败[ 定时任务间隔时间不允许少于12小时 ]'}

    # 小于 60秒 一律不允许保存
    if require_items.get("triggerType") == "runDate" and require_items.get("runDate") < timestamp() + 60:
        return {'status': 'failed', 'data': '新建失败[ 指定日期时间要比当前时间晚[ 60 ] 秒以上 ]'}
    return True


# 该路由负责任务的控制
@cron.route('/Taskslist', methods=['POST'])
@jwt_role("admin")
def Taskslist():
    """
    {"mission":"定时服务名字AAA", "TaskOption":"dels"}
    """
    result = lambda msg:{'status': 'ok', "mission_Option": msg}
    _body = request.get_json(force=True)
    mission = _body.get("mission")
    task = _body.get("TaskOption")

    try:
        if task != None:
            if task == "add":
                # obj = cron_manager.add_cron(**{"mission_name": mission, "mode":"runDate", "run_Date": 1629699809})
                # obj = cron_manager.add_cron(**{"mission_name": mission, "mode":"interval", "seconds": 5})
                # get_jobs = cron_manager.get_jobs()
                return jsonify(result("该功能不会开放，得充值开通"))

            elif task == "pause":
                cron_manager.pause_cron(cron_id=mission)
                return jsonify(result("暂停任务"))

            elif task == "resume":
                cron_manager.resume_cron(cron_id=mission)
                return jsonify(result("恢复任务"))

            elif task == "dels":
                cron_manager.del_cron(cron_id=mission)
                return jsonify(result("删除任务"))

            elif task == "delall":
                cron_manager.del_cron(del_all=True)
                return jsonify(result("删除所有任务"))

            elif task == "jobs":
                get_jobs = cron_manager.get_jobs()
                _jobs = [get_jobs[x] for x in range(len(get_jobs))]
                return {"jobs": str(_jobs)}

            elif task == "status":
                a = cron_manager.monitor()
                return "OK"

            else:
                return jsonify(result("任务不存在"))

        else:
            return jsonify(result("任务不存在"))

    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '获取任务失败 [ %s ]' %e})


@cron.route('/addcron', methods=['POST'])
@jwt_role()
def addcron():
    """
    {
        "uid": "张三",
        "mission_name": "定时服务名字",
        "pid": "c3009c8e62544a23ba894fe5519a6b64",
        "EnvId": "9d289cf07b244c91b81ce6bb54f2d627",
        "SuiteIdList": ["75cc456d9c4d41f6980e02f46d611a5c"],
        "runDate": 1239863854,
        "interval": 60,
        "alwaysSendMail": true,
        "alarmMailGroupList": "['4dc0e648e61846a4aca01421aa1202e2', '2222222222222']",
        "triggerType": "interval"
    }
    """
    try:
        require_items = get_post_items(request, CronJob.REQUIRE_ITEMS, throwable=True)
        option_items = get_post_items(request, CronJob.OPTIONAL_ITEMS)
        require_items.update(option_items)
        require_items.update({"uid": g.user_object_id})
        mission_name = get_models_filter(CronJob, CronJob.mission_name == require_items["mission_name"])

        if mission_name != []:
            return jsonify({'status': 'failed', 'data': '名字已存在'})

        temp = require_items.get("alarmMailGroupList")
        require_items["alarmMailGroupList"] = str(temp)

        times = Run_Times(**require_items)
        if times == True:
            _model = create_model(CronJob, **require_items)
            cron_manager.add_cron(
                **{
                    "mission_name": require_items.get("mission_name"),
                    "mode": require_items.get("triggerType"),
                    "seconds": require_items.get("interval"),
                    "run_Date": require_items.get("runDate"),
                    "task_Job": require_items,
                    "object_id": _model.object_id,
                })
            return jsonify({'status': 'ok', 'object_id': _model.object_id})
        else:
            return jsonify(times)
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '新建失败 %s' % e})


@cron.route('/putcron/<object_id>', methods=['PUT'])
@jwt_role()
def putcron(object_id):
    """
    {
        "uid": "张三",
        "mission_name": "定时服务名字",
        "pid": "c3009c8e62544a23ba894fe5519a6b64",
        "EnvId": "9d289cf07b244c91b81ce6bb54f2d627",
        "SuiteIdList": ["75cc456d9c4d41f6980e02f46d611a5c"],
        "runDate": 1239863854,
        "interval": 60,
        "alwaysSendMail": true,
        "alarmMailGroupList": "['4dc0e648e61846a4aca01421aa1202e2', '2222222222222']",
        "triggerType": "interval"
    }
    """
    try:
        _model = get_model(CronJob, object_id)
        mission_name = get_post_data(request, "mission_name", throwable=True)
        uid = get_post_data(request, "uid", throwable=True)
        EnvId = get_post_data(request, "EnvId", throwable=True)
        pid = get_post_data(request, "pid", throwable=True)
        SuiteIdList = get_post_data(request, "SuiteIdList", throwable=True)

        runDate = get_post_data(request, "runDate", throwable=True)
        interval = get_post_data(request, "interval", throwable=True)
        triggerType = get_post_data(request, "triggerType", throwable=True)

        times = Run_Times(**request.get_json(force=True))
        if times == True:
            _model.mission_name = mission_name
            _model.uid = uid
            _model.pid = pid
            _model.EnvId = EnvId
            _model.SuiteIdList = SuiteIdList

            _model.triggerType = triggerType
            _model.runDate = runDate
            _model.interval = interval

            require_items = {
                "EnvId": EnvId,
                "ProjectId": pid,
                "Interface": SuiteIdList,
            }
            cron_manager.add_cron(
                **{
                    "mission_name": mission_name,
                    "mode": triggerType,
                    "seconds": interval,
                    "run_Date": runDate,
                    "object_id": _model.object_id,
                    "task_Job": require_items,
                })
            update_models(_model)
            return {'status': 'ok', "object_id": object_id, 'data': '调度器修改成功'}
        else:
            return jsonify(times)
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '修改错误%s' % e})


@cron.route('/delcron/<object_id>', methods=['DELETE'])
@jwt_role()
def delcron(object_id):
    """
    {}
    """
    try:
        _model = get_model_by(CronJob, object_id=object_id)
        if _model is None:
            return jsonify({'status': 'failed', 'data': '删除不存在的对象'})
        cron_manager.del_cron(cron_id=_model.mission_name)
        _model.job_status = 1
        update_models(_model)
        delete_model(CronJob, object_id)
        return {
            "status": "ok",
            "object_id": object_id,
        }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '删除错误%s' % e})



# 任务启动 与 关闭
@cron.route('/nodifycron/<object_id>', methods=['POST'])
@jwt_role()
def nodifycron(object_id):
    """
    {"job_status": 0}
    """
    try:
        _model = get_model_by(CronJob, object_id=object_id)
        if _model is None:
            return jsonify({'status': 'failed', 'data': '对象不存在'})
        job_status = get_post_data(request, "job_status", throwable=True)

        if type(job_status) == int and job_status == 0:
            _model.job_status = 0
            update_models(_model)
            msg = "恢复任务"
            cron_manager.resume_cron(cron_id=_model.mission_name)
        elif type(job_status) == int and job_status == 1:
            _model.job_status = 1
            update_models(_model)
            msg = "暂停任务"
            cron_manager.pause_cron(cron_id=_model.mission_name)
        else:
            return jsonify({'status': 'failed', 'data': '无法修改定时任务状态, [nodify参数：0 开启 | 1 关闭]'})

        return jsonify({
            "status": "ok",
            "object_id": _model.object_id,
            "mission_name": _model.mission_name,
            "job_status": _model.job_status,
            "data": msg,
        })
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '删除错误%s' % e})

