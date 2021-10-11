from .base import _BaseModel
from app.extensions import db
from app.models.tools import get_username

# {"a":[{"接口A":[1,2,3,4,5]},{"接口B":[1,2,3,4,5]}]}
class Scenes(_BaseModel):
    __tablename__ = "Scenes"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + [
                    "name", "TCase_ids",
                    "run_state", "uid"
                    ]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS + ["description"]
    name = db.Column('name', db.String(256), nullable=False, comment="场景名")
    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")

    # EnvId = db.Column('EnvId', db.String(32), nullable=False, comment="项目列表")
    # Project_ids = db.Column('Project_ids', db.JSON, nullable=True, comment="项目列表")
    # Inter_ids = db.Column('Inter_ids', db.JSON, nullable=True, comment="接口列表")

    TCase_ids = db.Column('TCase_ids', db.JSON, nullable=False, comment="用例列表")
    run_state = db.Column('run_state', db.SmallInteger, nullable=False, default=0)
    description = db.Column('description', db.String(256), nullable=True)


    def get_json(self):
        return {
            "object_id": self.object_id,
            "state": self.state,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
            "uid": self.uid,
            "uid_name": get_username("UID", self.uid),
            "TCase_ids": self.TCase_ids,
            "run_state": self.run_state,
            "description": self.description,
        }

    @staticmethod
    def get_type():
        res = []
        return {
            "res": res
        }