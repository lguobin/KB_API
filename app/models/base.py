import time
import uuid
from app.extensions import db


def timestamp():
    return int(time.time())


def get_object_id():
    return uuid.uuid4().hex


class _BaseModel(db.Model):
    __abstract__ = True
    REQUIRE_ITEMS = []
    OPTIONAL_ITEMS = []
    object_id = db.Column('object_id',
                          db.String(32),
                          primary_key=True,
                          nullable=False)
    created_at = db.Column('created_at', db.BigInteger, nullable=False)
    updated_at = db.Column('updated_at', db.BigInteger, nullable=False)
    STATE_NORMAL = 0
    STATE_DELETE = 1
    state = db.Column('state', db.SmallInteger, nullable=False, default=0)

    def __init__(self, oid=None):
        if oid is None:
            self.object_id = get_object_id()
        else:
            self.object_id = oid
        self.created_at = timestamp()
        self.updated_at = timestamp()
        self.uid = get_object_id()

    def update(self):
        self.updated_at = timestamp()
        return True

    def get_json(self):
        return {
            'object_id': self.object_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "state": self.state,
        }

    @classmethod
    def create(cls, object_id=None, **items):
        model = cls(object_id)
        for key, value in items.items():
            setattr(model, key, value)
        model.update()
        return model

    @staticmethod
    def update_model(model, **items):
        for key, value in items.items():
            setattr(model, key, value)
        model.update()
        return model
