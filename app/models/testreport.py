# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/08/09 11:50:26
# @File     : TestCase.py
# @Author   : K.B.Lam
# @Version  : 1.0



from .base import _BaseModel
from app.extensions import db
from app.models.tools import get_username


class TestReport(_BaseModel):
    __tablename__ = "TestReport"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + [
                    "uid", "EnvId", "EnvName",
                    "executionMode", "cronJobId",
                    "StartTime", "Project_id", "interfaces_Suites_CaseDetail",
                    "totalCount", "passCount", "failCount", "errorCount", "spendTimeInSec",
                    ]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS
    EnvId = db.Column('EnvId', db.String(32), nullable=False)
    EnvName = db.Column('EnvName', db.String(32), nullable=False)
    executionMode = db.Column('executionMode', db.String(32), nullable=False)
    cronJobId = db.Column('cronJobId', db.String(32), nullable=True)
    Project_id = db.Column('Project_id', db.String(32), nullable=False)
    StartTime = db.Column('StartTime', db.Integer, nullable=False)

    interfaces_Suites_CaseDetail = db.Column('interfaces_Suites_CaseDetail', db.JSON, nullable=False)

    totalCount = db.Column('totalCount', db.Integer, nullable=False)
    passCount = db.Column('passCount', db.Integer, nullable=False)
    failCount = db.Column('failCount', db.Integer, nullable=False)
    errorCount = db.Column('errorCount', db.Integer, nullable=False)
    spendTimeInSec = db.Column('spendTimeInSec', db.Float, nullable=False)

    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")


    def get_json(self):
        return {
            "report_object_id": self.object_id,
            "uid": self.uid,
            "Project_id": self.Project_id,
            "uid_name": get_username("UID", self.uid),
            "Project_id_name": get_username("PID", self.Project_id),
            "EnvId":self.EnvId,
            "EnvName":self.EnvName,
            "executionMode":self.executionMode ,
            "cronJobId":self.cronJobId,
            "StartTime":self.StartTime,

            # "interfaces_Suites_CaseDetail":self.interfaces_Suites_CaseDetail,

            "totalCount":self.totalCount,
            "passCount":self.passCount,
            "failCount":self.failCount,
            "errorCount":self.errorCount,
            "spendTimeInSec":self.spendTimeInSec,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def get_type():
        res = []
        return {"res": res}