# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2021/08/09 11:50:26
# @File     : Users.py
# @Author   : K.B.Lam
# @Version  : 1.0


from app.extensions import db
from .base import _BaseModel, timestamp
from werkzeug.security import generate_password_hash, check_password_hash



class Users(_BaseModel):
    __tablename__ = "Users"
    __bind_key__ = "default"

    REQUIRE_ITEMS = _BaseModel.REQUIRE_ITEMS + ["user", "password", "email", "role_id", "confirm"]
    OPTIONAL_ITEMS = _BaseModel.OPTIONAL_ITEMS + ["nickname", "token", "login_at"]

    user = db.Column('user', db.String(128), nullable=False, unique=True)
    _password = db.Column('password', db.String(256), nullable=False)
    email = db.Column('email', db.String(256), nullable=False)
    nickname = db.Column('nickname', db.String(64), nullable=True)
    token = db.Column('token', db.String(4096), nullable=True)
    login_at = db.Column('login_at', db.BigInteger, nullable=True)

    # 加入权限组
    role_id = db.Column(db.Integer(), default=False)

    #当期账户激活状态
    confirm = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update(self):
        self.login_at = timestamp()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def get_json(self):
        return {
            'object_id': self.object_id,
            'username': self.user,
            'nickname': self.nickname,
            'email': self.email,
            'login_at': self.login_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'role_id': self.role_id,
            'confirm': self.confirm,
            'state': self.state
        }

    @staticmethod
    def get_type():
        res = []
        return {"res": res}
