from .base import _BaseModel
from app.extensions import db
from app.models.tools import get_username

class Email(_BaseModel):
    __tablename__ = "Email"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + [
                        "uid", 
                        "name", "email", "mailGroup",
                    ]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS + [
                        "sendStatus", "sendMailDate",
                        "description",
                    ]

    name = db.Column('name', db.String(128), nullable=False)
    email = db.Column('email', db.String(2048), nullable=False)
    mailGroup = db.Column('mailGroup', db.String(4096), nullable=False)

    uid = db.Column('uid', db.String(32), nullable=False, comment="创建者")

    description = db.Column('description', db.String(256), nullable=True)
    sendStatus = db.Column('sendStatus', db.SmallInteger, nullable=True)
    sendMailDate = db.Column('sendMailDate', db.BigInteger, nullable=True)

    def get_json(self):
        return {
            "object_id": self.object_id,
            "uid": self.uid,
            "uid_name": get_username("UID", self.uid),
            "name": self.name,
            "email": self.email,
            "mailGroup": self.mailGroup,

            "sendStatus": self.sendStatus,
            "sendMailDate": self.sendMailDate,

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