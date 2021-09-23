# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/08/09 11:50:26
# @File     : Interfaces.py
# @Author   : K.B.Lam
# @Version  : 1.0



from .base import _BaseModel
from app.extensions import db


class Interfaces(_BaseModel):
    __tablename__ = "Interfaces"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + ["name", "pid", "i_type", "route",
                    "requestMethod", "headers", "uid", "description"]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS + ["delay"]

    name = db.Column('name', db.String(128), nullable=False, comment="项目名称")
    pid = db.Column('pid', db.String(32), nullable=False, comment="归属项目")
    i_type = db.Column('i_type', db.String(64), nullable=False, comment="接口类型")
    route = db.Column('route', db.String(1024), nullable=False, comment="接口地址")
    headers = db.Column('headers', db.String(64), nullable=False, comment="请求头")
    requestMethod = db.Column('requestMethod', db.String(64), nullable=False, comment="请求方式")
    delay = db.Column('delay', db.Integer, nullable=True, comment="延时请求")
    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")
    description = db.Column('description', db.String(256), nullable=True)


    def get_json(self):
        return {
            "object_id": self.object_id,
            "pid": self.pid,
            "uid": self.uid,
            "name": self.name,
            "headers": self.headers,
            "requestMethod": self.requestMethod,
            "route": self.route,
            "delay": self.delay,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
            "description": self.description
        }

    @staticmethod
    def get_type():
        res = []
        return {
            "res": res
        }