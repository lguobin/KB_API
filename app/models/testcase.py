# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/08/09 11:50:26
# @File     : TestCase.py
# @Author   : K.B.Lam
# @Version  : 1.0


from .base import _BaseModel
from app.extensions import db


class TestCase(_BaseModel):
    __tablename__ = "TestCase"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + ["name", "uid", "pid", "Iid", "route",
                    "headers", "requestMethod", "requestBody",
                    "description", "parameterType", "responseBody",
                    ]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS + [
                    "setGlobalVars", "tempGlobalParams",
                    "checkoptions", "checkSpendSeconds", "checkResponseCode",
                    "checkResponseBody", "checkResponseNumber",
                    "optionsValue", "generate_params",
                    "delay", "variable_1", "variable_2",
                    "filePath",
                    ]

    name = db.Column('name', db.String(128), nullable=False, comment="名称")
    pid = db.Column('pid', db.String(32), nullable=False, comment="归属项目")
    Iid = db.Column('Iid', db.String(32), nullable=False, comment="归属接口")
    route = db.Column('route', db.String(1024), nullable=False, comment="接口地址")
    headers = db.Column('headers', db.String(256), nullable=False, comment="请求头")
    requestMethod = db.Column('requestMethod', db.String(64), nullable=False, comment="请求方式")
    requestBody = db.Column('requestBody', db.String(256), nullable=True, comment="请求体")

    setGlobalVars = db.Column('setGlobalVars', db.JSON, nullable=True)
    tempGlobalParams = db.Column('tempGlobalParams', db.JSON, nullable=True)

    responseBody = db.Column('responseBody', db.Text, nullable=True)


    checkoptions = db.Column('checkoptions', db.Boolean, nullable=True, default=False)
    checkSpendSeconds = db.Column('checkSpendSeconds', db.Float, nullable=True)
    checkResponseCode = db.Column('checkResponseCode', db.Integer, nullable=True)
    checkResponseBody = db.Column('checkResponseBody', db.JSON, nullable=True)
    checkResponseNumber = db.Column('checkResponseNumber', db.JSON, nullable=True)

    optionsValue = db.Column('optionsValue', db.String(1024), nullable=True)
    generate_params = db.Column('generate_params', db.String(4096), nullable=True)

    delay = db.Column('delay', db.Integer, nullable=True, comment="延时请求")
    variable_1 = db.Column('variable_1', db.String(2048), nullable=True)
    variable_2 = db.Column('variable_2', db.String(2048), nullable=True)

    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")
    description = db.Column('description', db.String(256), nullable=True)

    parameterType = db.Column('parameterType', db.String(256), nullable=False)
    filePath = db.Column('filePath', db.String(256), nullable=True)


    def get_json(self):
        return {
            "object_id": self.object_id,
            "uid": self.uid,
            "pid": self.pid,
            "Iid": self.Iid,
            "testcase_name": self.name,
            "headers": self.headers,
            "requestMethod": self.requestMethod,
            "route": self.route,
            "parameterType": self.parameterType,
            "filePath": self.filePath,
            "requestBody": self.requestBody,
            "responseBody": self.responseBody,

            "setGlobalVars": self.setGlobalVars,
            "tempGlobalParams": self.tempGlobalParams,

            "checkoptions": self.checkoptions,
            "checkSpendSeconds": self.checkSpendSeconds,
            "checkResponseCode": self.checkResponseCode,
            "checkResponseBody": self.checkResponseBody,
            "checkResponseNumber": self.checkResponseNumber,

            "optionsValue": self.optionsValue,
            "generate_params": self.generate_params,
            "delay": self.delay,
            "variable_1": self.variable_1,
            "variable_2": self.variable_2,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
            "description": self.description
        }

    @staticmethod
    def get_type():
        res = []
        return {"res": res}