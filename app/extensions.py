import logging
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.common.cronManager import CronManager




cron_manager = CronManager()
cron_manager.start()
cron_manager.monitor()

db = SQLAlchemy()
migrate = Migrate(db=db)


def config_extentions(app):
    db.init_app(app)
    migrate.init_app(app=app)


def setup_log(Config):
    logging.basicConfig(level=Config.LOG_LEVEL)
    file_log_hander = RotatingFileHandler('logs/running.log',
                                          maxBytes=1024 * 1024 * 100,
                                          backupCount=20)  # 100M
    # 创建日志记录的格式，日志等级 输入日志信息的文件名 行数，日志信息
    # fmt = '%(levelname)s %(filename)s:%(lineno)d %(message)s'
    fmt = "[%(asctime)s]-[文件名: %(filename)s]-[line:%(lineno)d] - %(levelname)s : %(message)s"
    formatter = logging.Formatter(fmt)
    file_log_hander.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_hander)
