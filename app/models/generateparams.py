# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/08/09 11:50:26
# @File     : TestCase.py
# @Author   : K.B.Lam
# @Version  : 1.0



from .base import _BaseModel
from app.extensions import db


class GenerateParams(_BaseModel):
    __tablename__ = "GenerateParams"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + ["iid", "caseid", "BODY", "RESPONSE", "VERIFY", "RESULT", "uid", "description"]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS
    Iid = db.Column('iid', db.String(32), nullable=False, comment="归属接口")
    caseid = db.Column('caseid', db.String(32), nullable=False, comment="归属用例")
    BODY = db.Column('BODY', db.String(256), nullable=False)
    RESPONSE = db.Column('RESPONSE', db.String(256), nullable=False)
    VERIFY = db.Column('VERIFY', db.String(256), nullable=False)
    RESULT = db.Column('RESULT', db.String(256), nullable=False)
    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")
    description = db.Column('description', db.String(256), nullable=True)


    def get_json(self):
        return {
            "object_id": self.object_id,
            "uid": self.uid,
            "Iid": self.Iid,
            "caseid":self.caseid,
            "BODY":self.BODY,
            "RESPONSE":self.RESPONSE,
            "VERIFY":self.VERIFY,
            "RESULT":self.RESULT,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
            "description": self.description
        }

    @staticmethod
    def get_type():
        res = []
        return {"res": res}


