from .base import _BaseModel
from app.extensions import db


class EnvConfig(_BaseModel):
    __tablename__ = "EnvConfig"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + ["name", "projectTestType", "domain",
                    "uid", "description"]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS + ["redis", "mysql"]

    name = db.Column('name', db.String(128), nullable=False, comment="环境名称")
    projectTestType = db.Column('projectTestType', db.String(128), nullable=False, comment="接口类型")
    domain = db.Column('domain', db.String(256), nullable=False, comment="域名")

    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")
    redis = db.Column('redis', db.JSON, nullable=True)
    mysql = db.Column('mysql', db.JSON, nullable=True)
    description = db.Column('description', db.String(256), nullable=True)

    def get_json(self):
        return {
            "object_id": self.object_id,
            "name": self.name,
            "projectTestType": self.projectTestType,
            "domain": self.domain,
            "redis": self.redis,
            "mysql": self.mysql,
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