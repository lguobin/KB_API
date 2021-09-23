from flask import jsonify, Blueprint, request
from app.common.decorator import jwt_role
from app.models import *
from app.common.helper import *
from app.common.helper import get_post_items
from app.common.helper import create_model
from sqlalchemy import desc
from settings import Config


proj = Blueprint("proj", __name__)


@proj.route('/addProject', methods=['POST'])
@jwt_role()
def addproject():
    try:
        require_items = get_post_items(request, Project.REQUIRE_ITEMS, throwable=True)
        option_items = get_post_items(request, Project.OPTIONAL_ITEMS)
        _model = get_models_filter(Project, Project.name == require_items["name"])
        if _model != []:
            return jsonify({'status': 'failed', 'msg': '名字已存在'})

        require_items.update(option_items)
        project_model = create_model(Project, **require_items)
        return jsonify({'status': 'ok', 'object_id':project_model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '新建失败 %s' % e})


@proj.route('/putProject/<object_id>', methods=['PUT'])
@jwt_role()
def putproject(object_id):
    """
    {
        "name":"test",
        "version":"test",
        "uid":"1@1.cn",
        "description":"descriptionasdasdaasasd",
        "projectTestType":"apiTest",
        "state":1
    }
    """
    try:
        project_model = get_model(Project, object_id)

        name = get_post_data(request, "name", throwable=True)
        uid = get_post_data(request, "uid", throwable=True)
        version = get_post_data(request, "version", throwable=True)
        projectTestType = get_post_data(request, "projectTestType", throwable=True)
        description = get_post_data(request, "description", throwable=True)
        project_model.name = name
        project_model.uid = uid
        project_model.version = version
        project_model.projectTestType = projectTestType
        project_model.description = description
        update_models(project_model)
        return {
            "object_id": object_id,
        }
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '修改错误%s' % e})


@proj.route('/deleteProject/<object_id>', methods=['DELETE'])
@jwt_role()
def deleteProject(object_id):
    """
    {}
    """
    try:
        project_model = get_model_by(Project, object_id=object_id)
        if project_model is None:
            return jsonify({'status': 'failed', 'data': '删除不存在的对象'})
        delete_model(Project, object_id, real_delete=False)
        return {}
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '删除错误%s' % e})


@proj.route('/checkinterface/<object_id>', methods=['GET'])
@jwt_role()
def checkinterface(object_id):
    """
    {}
    """
    try:
        page = get_page_value(request)
        per_page = get_per_page_value(request, Config.PER_PAGE, Config.MAX_PER_PAGE)
        paging = get_query_data(request, "paging", 1)
        filter_params = [Interfaces.state == Interfaces.STATE_NORMAL, Interfaces.pid == object_id]
        if bool(int(paging)):
            pagination = get_models_filter_with_pagination(Interfaces, "", page, per_page, desc, *filter_params)

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
