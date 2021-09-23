# from app.common.utils import *
from sqlalchemy import desc
from settings import Config
from app.models import *
from app.extensions import db
from app.models.base import _BaseModel
from app.common.errors import DBError



def Pages(_request, _TABLE):
    # 获取分页数据
    page = get_page_value(_request)
    per_page = get_per_page_value(_request, Config.PER_PAGE, Config.MAX_PER_PAGE)
    paging = get_query_data(_request, "paging", 1)
    filter_params = [_TABLE.state == _TABLE.STATE_NORMAL]
    if bool(int(paging)):
        pagination = get_models_filter_with_pagination(_TABLE, None, page, per_page, desc, *filter_params)
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

def input_files(pid, *row):
    # 批量导入接口测试用例，不存在就创建
    _interss = get_model_by(Interfaces, name=row[0])
    if _interss != None:
        _input = {
            "name": row[1],
            "description": "导入用例__" + str(row[2]),
            "pid": pid,
            "Iid": _interss.object_id,
            "route": row[5],
            "headers": row[6],
            "requestMethod": row[7],
            "requestBody": row[8],
            "parameterType": row[9],
            "setGlobalVars": eval(row[10]),
            "checkoptions": None,
            "checkSpendSeconds": row[12],
            "checkResponseBody": eval(row[13]),
            "checkResponseCode": row[14],
            "uid": row[-1],
        }
        if row[11] == "Y" or row[11] == "True":
            _input["checkoptions"] = True
        else:
            _input["checkoptions"] = False
        create_model(TestCase, **_input)
    else:
        require_items = {
            "pid": pid,
            "uid": row[-1],
            "name": row[0],
            "route": row[5],
            "headers": row[6],
            "requestMethod": row[7],
            "i_type": "HTTP",
            "description": "导入用例__" + str(row[2])
        }
        _model = create_model(Interfaces, **require_items)
        _input = {
            "name": row[1],
            "description": "导入用例__" + str(row[2]),
            "pid": pid,
            "Iid": _model.object_id,
            "route": row[5],
            "headers": row[6],
            "requestMethod": row[7],
            "requestBody": row[8],
            "parameterType": row[9],
            "setGlobalVars": row[10],
            "checkoptions": None,
            "checkSpendSeconds": row[12],
            "checkResponseBody": row[13],
            "checkResponseCode": row[14],
            "uid": row[-1],
            }
        if row[11] == "Y" or row[11] == "True":
            _input["checkoptions"] = True
        else:
            _input["checkoptions"] = False
        create_model(TestCase, **_input)
    return True


def get_Env(test_env_id):
    # 获取环境变量信息
    Temp_env_list = get_model(EnvConfig, test_env_id)
    if Temp_env_list != None:
        if Temp_env_list.domain == "" or Temp_env_list.domain == None:
            return {'status': 'failed', 'data': '环境配置存在异常, 请前往环境设置检查'}
        _env_list = [
            Temp_env_list.object_id,
            Temp_env_list.name,
            Temp_env_list.domain,
            Temp_env_list.redis,
            Temp_env_list.mysql,
            ]
        return _env_list
    else:
        return None


def composeCaseWorkshop(EnvId, ProjectId=None, Interface=None, Tcase=None):
    if EnvId != None:
        _EnvList = get_Env(EnvId)
        if _EnvList == None:
            return None


        _CASE = []
        if ProjectId != None:
            _Pro_object_id = get_models(Project, object_id=ProjectId)
            if _Pro_object_id != []:
                __case = get_models(TestCase, pid=_Pro_object_id[0].object_id)

                for x in range(len(__case)):
                    if __case[x].route:

                        reqs = {
                            "EnvId": _EnvList[0],
                            "EnvName": _EnvList[1],
                            "route": _EnvList[2] + __case[x].route,

                            "redis": _EnvList[3],
                            "mysql": _EnvList[4],

                            "name": __case[x].name,
                            "Project_id": __case[x].pid,
                            "Interface_id": __case[x].Iid,
                            "object_id": __case[x].object_id,
                            "Method": __case[x].requestMethod,
                            "Body":  __case[x].requestBody,
                            "Headers": __case[x].headers,

                            "setGlobalVars":  __case[x].setGlobalVars,

                            "checkoptions": __case[x].checkoptions,
                            "checkSpendSeconds": __case[x].checkSpendSeconds,
                            "checkResponseCode": __case[x].checkResponseCode,
                            "checkResponseBody": __case[x].checkResponseBody,
                            "checkResponseNumber": __case[x].checkResponseNumber,
                        }

                        _CASE.append(reqs)
            else:
                return None

        elif Interface != None and Interface != []:
            for index in range(len(Interface)):
                _Inter_object_id = get_models(Interfaces, object_id=Interface[index])

                if _Inter_object_id != []:
                    __case = get_models(TestCase, Iid=_Inter_object_id[0].object_id)

                    for x in range(len(__case)):
                        if __case[x].route:
                            reqs = {
                                "EnvId": _EnvList[0],
                                "EnvName": _EnvList[1],
                                "route": _EnvList[2] + __case[x].route,

                                "redis": _EnvList[3],
                                "mysql": _EnvList[4],

                                "name": __case[x].name,
                                "Project_id": __case[x].pid,
                                "Interface_id": __case[x].Iid,
                                "object_id": __case[x].object_id,
                                "Method": __case[x].requestMethod,
                                "Body":  __case[x].requestBody,
                                "Headers": __case[x].headers,

                                "setGlobalVars":  __case[x].setGlobalVars,

                                "checkoptions": __case[x].checkoptions,
                                "checkSpendSeconds": __case[x].checkSpendSeconds,
                                "checkResponseCode": __case[x].checkResponseCode,
                                "checkResponseBody": __case[x].checkResponseBody,
                                "checkResponseNumber": __case[x].checkResponseNumber,
                            }
                            _CASE.append(reqs)

                else:
                    return None

        elif Tcase != None and Tcase != []:

            id_list = []
            for case in Tcase:
                _obj_id = case
                if _obj_id in id_list:
                    Tcase.remove(case)

                else:
                    # 判断 Id 是否有效
                    _temp = get_model(TestCase, object_id=_obj_id)
                    if _temp != None:
                        reqs = {
                            "EnvId": _EnvList[0],
                            "EnvName": _EnvList[1],
                            "route": _EnvList[2] + _temp.route,

                            "redis": _EnvList[3],
                            "mysql": _EnvList[4],


                            "name": _temp.name,
                            "Project_id": _temp.pid,
                            "Interface_id": _temp.Iid,
                            "object_id": _temp.object_id,
                            "Method": _temp.requestMethod,
                            "Body": _temp.requestBody,
                            "Headers": _temp.headers,

                            "setGlobalVars": _temp.setGlobalVars,

                            "checkoptions": _temp.checkoptions,
                            "checkSpendSeconds": _temp.checkSpendSeconds,
                            "checkResponseCode": _temp.checkResponseCode,
                            "checkResponseBody": _temp.checkResponseBody,
                            "checkResponseNumber": _temp.checkResponseNumber,
                        }
                        _CASE.append(reqs)
                    else:
                        pass

        # print(7777777777777777777777777777)
        # print(_CASE)

        return _CASE
    else:
        return None


def single_Save_response(_response, object_id):
    from app import app
    with app.app_context():
        _model = get_model(TestCase, object_id)
        _model.responseBody = str(_response)
        update_models(_model)
        print("异步保存数据")


def save_TestReport(_response):
    from app import app
    with app.app_context():
        _model = create_model(TestReport, **_response)
        return {"object_id": _model.object_id}


def get_TestReport(_model):
    if _model != None:
        return {
            "object_id": _model.object_id,
            "uid": _model.uid,
            "EnvId":_model.EnvId,
            "EnvName":_model.EnvName,
            "executionMode ":_model.executionMode ,
            "cronJobId":_model.cronJobId,
            "Project_id":_model.Project_id,
            "StartTime":_model.StartTime,
            "interfaces_Suites_CaseDetail":_model.interfaces_Suites_CaseDetail,
            "totalCount":_model.totalCount,
            "passCount":_model.passCount,
            "failCount":_model.failCount,
            "errorCount":_model.errorCount,
            "spendTimeInSec":_model.spendTimeInSec,
            "create_at": _model.created_at,
            "updated_at": _model.updated_at,
        }
    else:
        return {"message": "报告不存在或已被删除!"}



# ------------------------------
# ------------------------------
# ------------------------------

def get_task_Job(table_class, **params):
    _moble = db.session.query(table_class).filter_by(**params).first()
    return _moble.object_id


def get_first_one_model(table_class):
    return db.session.query(table_class).order_by(table_class.updated_at.desc()).first()


def get_like(table_class, params):
    return db.session.query(table_class).filter(table_class.name.like("%"+params+"%")).all()


def safe_check(value):
    return True


def get_query_data(request, key, default=None, throwable=False):
    value = request.args.get(key, None)
    if value is not None and safe_check(value):
        return value
    value = request.headers.get(key, None)
    if value is not None and safe_check(value):
        return value
    if not throwable:
        return default


def get_model(table_class, object_id):
    return db.session.query(table_class).get(object_id)


def get_models(table_class, **params):
    if params is not None and len(params) > 0:
        return db.session.query(table_class).filter_by(**params, state=0).all()
    else:
        return db.session.query(table_class).all()


def get_post_data(request, key, throwable=False):
    try:
        value = request.form.get(key, None)
        if value is not None:
            return value
        json = request.get_json(force=True)
        if json is not None:
            value = json.get(key, None)
            if value is not None and safe_check(value):
                return value
        if not throwable:
            return None
        print("[ 缺少提交的参数 ] -> ", key)
    except BaseException:
        raise DBError("Error: post value no contains {0}".format(key))


def get_post_items(request, item_names, throwable=False):
    items = {}
    for name in item_names:
        data = get_post_data(request, name, throwable)
        if data is not None:
            items[name] = data
    return items


from sqlalchemy.exc import IntegrityError
def create_model(table_class, **items):
    model = table_class()
    for key, value in items.items():
        setattr(model, key, value)
    try:
        model.update()
        db.session.add(model)
        db.session.commit()
        return model
    except IntegrityError as ie:
        db.session.rollback()
        raise DBError
    except Exception as e:
        db.session.rollback()
        raise DBError

def update_models(*models, auto_commit=True):
    try:
        for model in models:
            model.update()
            db.session.add(model)
        if auto_commit:
            db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        raise DBError
    except Exception as e:
        db.session.rollback()
        raise DBError


def get_models_timestamp(table_class, *params):
    try:
        return db.session.query(table_class).filter(_BaseModel.created_at <= params).all()
    except Exception as e:
        raise DBError


def get_models_filter(table_class, *params):
    try:
        return db.session.query(table_class).filter(*params).all()
    except Exception as e:
        raise DBError(e)


def get_page_value(request):
    page = int(get_query_data(request, 'page', 1))
    if page <= 0:
        return 1
    return page


def get_pages(total, per_page):
    pages = (total + per_page - 1) // per_page
    if pages <= 0:
        pages = 1
    return pages


def get_per_page_value(request, default, max_value):
    per_page = int(get_query_data(request, 'per_page', default))
    if per_page > max_value or per_page <= 0:
        return max_value
    return per_page


def get_models_filter_with_pagination(table_class, order_name, page, per_page, order_func, *params):
    # order_name 暂时废弃
    try:
        offset = (page - 1) * per_page
        query = table_class.query.filter(*params)
        total = query.count()
        models = query.order_by(order_func(_BaseModel.updated_at)).offset(offset).limit(per_page).all()
        return {
            'total': total,
            'models': models
        }
    except Exception as e:
        raise DBError(e)


def get_model_by(table_class, **params):
    try:
        return db.session.query(table_class).filter_by(**params).first()
    except Exception as e:
        raise DBError(e)


def delete_model(table_class, object_id, real_delete=False, auto_commit=True):
    try:
        model = db.session.query(table_class).get(object_id)
        delete_model_with_model(model, real_delete, auto_commit=auto_commit)
    except Exception as e:
        raise DBError(e)


def delete_model_with_model(model, real_delete=False, state=_BaseModel.STATE_DELETE, auto_commit=True):
    try:
        if real_delete:
            db.session.delete(model)
        else:
            model.update()
            model.state = state
            db.session.add(model)
        if auto_commit:
            db.session.commit()
    except Exception as e:
        if auto_commit:
            db.session.rollback()
        raise DBError(e)