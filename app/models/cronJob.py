
from .base import _BaseModel
from app.extensions import db


class CronJob(_BaseModel):
    __tablename__ = "CronJob"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + [
                    "mission_name",
                    "uid", "EnvId", 
                    "triggerType", 
                    ]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS + [
                    "pid", "SuiteIdList",
                    "interval", "runDate",
                    "lastUpdateTime", "description",
                    "alwaysSendMail", "alarmMailGroupList",
                    "alwaysWXWorkNotify",
                    ]

    # 任务
    mission_name = db.Column('mission_name', db.String(2048), nullable=False)
    uid = db.Column('uid', db.String(32), nullable=False)
    EnvId = db.Column('EnvId', db.String(32), nullable=True)
    triggerType = db.Column('triggerType', db.String(256), nullable=False)
    pid = db.Column('pid', db.String(32), nullable=True)
    SuiteIdList = db.Column('SuiteIdList', db.JSON, nullable=True)
    interval = db.Column('interval', db.BigInteger, nullable=True)
    runDate = db.Column('runDate', db.BigInteger, nullable=True)
    lastUpdateTime = db.Column('lastUpdateTime', db.BigInteger(), nullable=True)

    # 邮件
    alwaysSendMail = db.Column('alwaysSendMail', db.SmallInteger, nullable=True, default=False)
    alarmMailGroupList = db.Column('alarmMailGroupList', db.String(4096), nullable=True)
    alwaysWXWorkNotify = db.Column('alwaysWXWorkNotify', db.SmallInteger, nullable=True, default=False)
    description = db.Column('description', db.String(256), nullable=True)

    def get_json(self):
        return {
            "mission_name": self.mission_name,
            "interval":self.interval,
            "runDate":self.runDate,

            "object_id": self.object_id,
            "uid": self.uid,
            "pid":self.pid,
            "EnvId":self.EnvId,
            "SuiteIdList":self.SuiteIdList,
            "alarmMailGroupList":self.alarmMailGroupList,
            "alwaysSendMail":self.alwaysSendMail,
            "alwaysWXWorkNotify":self.alwaysWXWorkNotify,
            "lastUpdateTime":self.lastUpdateTime,
            "triggerType":self.triggerType,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
            "description": self.description
        }

    @staticmethod
    def get_type():
        res = []
        return {"res": res}

