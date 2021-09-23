from .users import _user
from .proj import proj
from .inter import inter
from .env import env
from .testcase import tcase
from .testapi import startAPI
from .reports import report
from .mail import email
from .cronjob import cron
from .commons import common
from .mockserver import mock
from .apiscenes import scenes

BluePrint = [
    (_user, "/user"),
    (proj, ""),
    (env, ""),
    (inter, ""),
    (tcase, ""),
    (startAPI, ""),
    (report, ""),
    (email, ""),
    (common, ""),
    (scenes, ""),
    (cron, ""),
    (mock, ""),
]


def api_blueprint(app):
    for blueprint, prefix in BluePrint:
        app.register_blueprint(blueprint, url_prefix="/api" + prefix)
