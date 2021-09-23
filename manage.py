# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/07/25 21:49:07
# @File     : main
# @Author   : K.B.Lam
# @Version  : 1.0


"""
使用如下命令降级；
pip install "Flask==1.1.4"
pip install "werkzeug==1.0.1"
或者

不使用Flask-Script，使用flask命令如下：
初始化数据库：flask db init
迁移新更改：flask db migrate
升级：flask db upgrade

还有其它命令...
或者
不降级则可以尝试修改一下flask_script/__init__.py中

# from flask._compat import text_type 改成
from flask_script._compat import text_type
"""


from app import create_app
from flask_script import Shell, Manager
from flask_migrate import MigrateCommand

from app.extensions import db

def make_shell_context():
    return dict(app=app, db=db)


app = create_app("test")

manager = Manager(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()


