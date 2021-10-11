# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/08/09 11:50:26
# @File     : Users.py
# @Author   : K.B.Lam
# @Version  : 1.0


from app.models import env


def get_username(_Tables, _obj):
    from app.models import Users
    from app.models import Project
    from app.models import Interfaces
    from app.models import EnvConfig

    if _Tables == "PID":
        name = Project.query.filter(Project.object_id == _obj).first()

    elif _Tables == "IId":
        name = Interfaces.query.filter(Interfaces.object_id == _obj).first()

    elif _Tables == "ENV":
        name = EnvConfig.query.filter(EnvConfig.object_id == _obj).first()

    elif _Tables == "UID":
        name = Users.query.filter(Users.object_id == _obj).first()
        if name != None:
            return name.user
        else:
            return None
    else:
        name = None

    if name != None:
        return name.name
    else:
        return None