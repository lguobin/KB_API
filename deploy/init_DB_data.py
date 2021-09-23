# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/07/21 16:38:50
# @File     : Create_info.py
# @Author   : K.B.Lam
# @Version  : 1.0

import os
import shutil
from settings import basedir

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config
from app.models import *

app = Flask(__name__)
app.Config.from_object(Config['test'])
db = SQLAlchemy(app)


# 插入信息
roles_A = Roles(name="Administrator", default=0, permissions=255)
roles_B = Roles(name="User", default=1, permissions=7)
roles_C = Roles(name="Anonymity", default=2, permissions=15)
works_A = Works(name="测试")
works_B = Works(name="开发")
works_C = Works(name="产品")
works_D = Works(name="CTO")

admin = Users(
    username = "admin",
    password_hash = "pbkdf2:sha256:260000$5NOb6roatp0vxAKR$1656ab4cc23791dc9cf6636a9d7dbac1a7fc71342482fdffa822c61d995183ce",
    email = "1@1.cn",
    status = True,
    work_id = "1",
    role_id = "1",
    confirm = True,
    about_me = "我是管理员，权限高的很哦",
)



def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

if __name__ == '__main__':
    db.session.add_all([roles_A, roles_B, works_A, works_B, works_C, works_D, admin])
    db.session.commit()
    # del_file(os.path.join(basedir, "migrations"))