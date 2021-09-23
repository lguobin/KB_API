# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/08/09 11:32:25
# @File     : project.py
# @Author   : K.B.Lam
# @Version  : 1.0


from .base import _BaseModel
from app.extensions import db


class Project(_BaseModel):
    __tablename__ = "Project"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + ["name", "projectTestType", "version", 
                                            "uid", "description"]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS

    name = db.Column('name', db.String(128), nullable=False, comment="项目名称")
    projectTestType = db.Column('projectTestType', db.String(64), nullable=False, comment="项目测试类型")
    version = db.Column('version', db.String(32), nullable=False, comment="项目版本")
    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")
    description = db.Column('description', db.String(256), nullable=True)

    def get_json(self):
        return {
            "object_id": self.object_id,
            "name": self.name,
            "uid": self.uid,
            "projectTestType": self.projectTestType,
            "version": self.version,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
            "description": self.description
        }

    @staticmethod
    def get_type():
        res = []
        return {"res": res}
