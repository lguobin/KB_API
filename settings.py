import os
from datetime import timedelta
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


# 所有环境配置的基类
basedir = os.path.abspath(os.path.dirname(__file__))
Platform_name = "【测试】定时任务结果报表"


class Config:
    # 设置日志等级
    PER_PAGE = 20
    MAX_PER_PAGE = 20
    DEBUG = True
    LOG_LEVEL = DEBUG
    SECRET_KEY = '8~wl7K?MHiQNI23a4g<re}c*0B@"1vzu9EWkSZyCfT[b]oJt#>P(h:G^!psR5F6$'

    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时是否显示原始SQL语句
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 邮箱
    MAIL_PORT = 465
    MAIL_SERVER = "smtp.exmail.qq.com"
    MAIL_USERNAME = "aaaa"
    MAIL_PASSWORD = "bbbbb"
    USER_REGISTER_SENDEMAIL = False
    REGISTER_SUBJECT = "用户激活邮件"
    REGISTER_CONTENT = "用户激活邮件! 点击下方链接即可完成激活!"


    # 原文链接：https://blog.csdn.net/weixin_43262264/article/details/108628334
    JWT_SECRET_KEY = SECRET_KEY
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600 * 24)
    JWT_VERIFY_CLAIMS = ['signature', 'exp', 'iat', 'refresh_token']
    JWT_REQUIRED_CLAIMS = ['exp', 'iat']
    JWT_ALGORITHM = 'HS256'
    JWT_AUTH_ENDPOINT = 'jwt'
    JWT_LEEWAY = timedelta(seconds=10)
    JWT_AUTH_HEADER_PREFIX = 'JWT'
    JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)

    MYSQL_HOSTS = {
        "host": "192.168.2.41",
        "user": "root",
        "password": "a123456",
        "db": "t_kb",
        "port": 3306,
        "charset": "utf8",
    }

    JOBSTORE = 'mysql'
    APS_JOBSTORES = {
        JOBSTORE:
        SQLAlchemyJobStore(
            url=
            'mysql+pymysql://root:a123456@192.168.2.41:3306/t_kb?charset=utf8',
            tablename='CronJob_list',
        )
    }
    APS_EXECUTORS = {
        'default': ThreadPoolExecutor(20),     # 默认线程数
        'processpool': ProcessPoolExecutor(4)  # 默认进程
    }

    # 企微_机器人
    WEBHOOK = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    RESET_Password = "123456"


class TestingConfig(Config):
    # json 显示中文
    JSON_AS_ASCII = False
    # 连接池
    SQLALCHEMY_POOL_SIZE = 10
    # 测试配置
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:a123456@192.168.2.41:3306/t_kb?charset=utf8"
    SQLALCHEMY_BINDS = {
        'default': SQLALCHEMY_DATABASE_URI,
    }


class ProductionConfig(Config):
    # 生产配置
    DEBUG = False
    # 连接池
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/blog?charset=utf8"
    SQLALCHEMY_BINDS = {
        'default': SQLALCHEMY_DATABASE_URI,
    }


config = {
    "test": TestingConfig,
    "production": ProductionConfig,
}
