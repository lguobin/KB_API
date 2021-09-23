from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_MISSED, EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

from pytz import timezone
from settings import Config
from datetime import datetime
from app.common.cronJobs import Test_missions


class CronManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler(
            timezone=timezone('Asia/Shanghai'),
            jobstores=Config.APS_JOBSTORES,
            executors=Config.APS_EXECUTORS,
            daemon=True)
        self.scheduler.daemonic = False
        self.jobstore = Config.JOBSTORE

    def add_cron(self, **cron_instance):
        # 参数体
        # {"mission_name": "test", "mode":"interval", "seconds": 5}
        # {"mission_name": "test", "mode":"runDate", "run_Date": 1629699809}
        mission_name = cron_instance.get("mission_name")
        if cron_instance.get("mode") == 'interval':
            seconds = cron_instance.get("seconds")
            seconds = int(seconds)
            if seconds <= 0:
                raise ValueError('please set interval > 0')
            job = self.scheduler.add_job(func=Test_missions,
                                         id=mission_name,
                                         args=(cron_instance,),
                                         trigger='interval',
                                         seconds=seconds,
                                         coalesce=True,
                                         replace_existing=True,
                                         max_instances=5,
                                         misfire_grace_time=30,
                                         jobstore=self.jobstore,
                                         )
        elif cron_instance.get("mode") == 'runDate':
            run_Date = datetime.fromtimestamp(cron_instance.get('run_Date'))
            job = self.scheduler.add_job(func=Test_missions,
                                        id=mission_name,
                                        args=(cron_instance,),
                                        trigger='date',
                                        run_date=run_Date,
                                        replace_existing=True,
                                        coalesce=True,
                                        misfire_grace_time=30,
                                        jobstore=self.jobstore,
                                        )

        elif cron_instance.get("mode") == 'cron':
            raise TypeError('暂时不支持 trigger_type 等于 \'cron\'')
        return mission_name

    def job_listener(self, _Event):
        print(333, _Event.job_id)
        job = self.scheduler.get_job(_Event.job_id)
        if job == None:
            from app import app
            with app.app_context():
                from app.models import CronJob
                from app.common.helper import get_task_Job, delete_model
                _object = get_task_Job(CronJob, mission_name=_Event.job_id)
                delete_model(CronJob, _object)

    def monitor(self):
        self.scheduler.add_listener(self.job_listener, EVENT_JOB_MISSED | EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)


    def start(self, paused=False):
        self.scheduler.start(paused=paused)

    def pause_cron(self, cron_id=None, pause_all=False):
        if pause_all:
            self.scheduler.pause()
        elif cron_id:
            self.scheduler.pause_job(job_id=cron_id)

    def resume_cron(self, cron_id=None, resume_all=False):
        if resume_all:
            self.scheduler.resume()
        elif cron_id:
            self.scheduler.resume_job(job_id=cron_id)

    def del_cron(self, cron_id=None, del_all=False):
        if del_all:
            self.scheduler.remove_all_jobs()
        elif cron_id:
            self.scheduler.remove_job(job_id=cron_id)

    def shutdown(self, force_shutdown=False):
        if force_shutdown:
            self.scheduler.shutdown(wait=False)
        else:
            self.scheduler.shutdown(wait=True)

    def get_jobs(self):
        return self.scheduler.get_jobs()
