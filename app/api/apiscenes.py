from flask import jsonify, Blueprint, request
from app.models import *
from app.common.helper import *
from app.common.session import send_and_save_report_BySuite
from app.common.decorator import jwt_role

scenes = Blueprint("scenes", __name__)


def tcases(_Tcase_list):
    tc = []    
    for index in range(len(_Tcase_list)):
        if _Tcase_list[index].get("EnvId") != None:
            bbb = composeCaseWorkshop(EnvId=_Tcase_list[index].get("EnvId"), Tcase=_Tcase_list[index].get("Scene"))
            tc.extend(bbb)
    return tc


@scenes.route('/scenes', methods=['POST'])
@jwt_role()
def addscenes():
    """
    {
        "name": "场景名字",
        "uid": "asdasdas",
        "TCase_ids": [{"EnvId":"AA环境", "Scene":[1,2,3,4]}, {"EnvId":"BBB环境", "Scene":[1,2,3,4]}],
        "run_state": 0,
        "description": "asdadasdasaasdasasdadadsadadadasdads"
    }

    重要的是:
        [{"EnvId":"AA环境", "Scene":[1,2,3,4]}, {"EnvId":"BBB环境", "Scene":[1,2,3,4]}]
    """
    try:
        require_items = get_post_items(request, Scenes.REQUIRE_ITEMS, throwable=True)
        option_items = get_post_items(request, Scenes.OPTIONAL_ITEMS)
        require_items.update(option_items)
        require_items.update({"uid": g.user_object_id})
        _model = get_models_filter(Scenes, Scenes.name == require_items["name"])
        if _model != []:
            return jsonify({'status': 'failed', 'data': '场景已存在'})
        _model = create_model(Scenes, **require_items)
        return jsonify({'status': 'ok', 'object_id':_model.object_id})
    except BaseException as e:
        return jsonify({'status': 'failed', 'data': '参数错误 %s' %e})


@scenes.route('/scenes/<object_id>', methods=['GET'])
@jwt_role()
def detailed(object_id):
    _model = get_model(Scenes, object_id)
    if _model != None:
        Tcase_list = tcases(_model.TCase_ids)
        return jsonify({'status': 'ok', 'object_id': Tcase_list})
    else:
        return jsonify({'status': 'ok', 'object_id': None})


@scenes.route('/scenes/activation', methods=['POST'])
@jwt_role()
def startScenes():
    """
    {
        "activation":"0c9f14e7cbcf4986bc32f1b311ad1bff",
        "uid":11111111
    }
    """
    request_data = request.get_json(force=True)
    activation = request_data.get("activation")
    if activation != None and activation != "" and len(activation) == 32:
        _model = get_model(Scenes, activation)
        if _model != None:
            Tcase_list = tcases(_model.TCase_ids)
            action = {
                    "uid": request_data.get("uid"),
                    "executionMode": "scenes",
                }
            send_and_save_report_BySuite(Tcase_list, action=action)
            return jsonify({'status': 'ok', 'data': '测试完毕, 稍后前往「测试报告」查看结果'})
        else:
            return jsonify({'status': 'failed', 'data': '场景运行失败，找不到可用场景或用例'})
    else:
        return jsonify({'status': 'failed', 'data': '场景运行失败，找不到可用场景或用例'})


@scenes.route('/scenes/<object_id>', methods=['DELETE'])
@jwt_role()
def delScenes(object_id):
    """
    {}
    """
    _model = get_model_by(Scenes, object_id=object_id)
    if _model != None:
        delete_model(Scenes, object_id)
        return {
            "status": "ok",
            "object_id": object_id,
        }
    else:
        return jsonify({'status': 'failed', 'data': '删除不存在的对象'})
