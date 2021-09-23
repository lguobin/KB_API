import time
from settings import Platform_name
from app.common.notify import send_email, send_wxwork_notify
from app.common.utils import str_list
from app.common.errors import DBError


# Do something
def Test_missions(items):
    action = {
        "uid": "admin_定时服务",
        "executionMode": "cronJob",
        "cronJobId": items.get("mission_name"),
    }

    # print("----------------------------------------")
    # print(items)
    # print("----------------------------------------")

    from app import app
    with app.app_context():
        from app.models import CronJob, TestReport, Email
        from app.common.session import send_and_save_report_BySuite
        from app.common.helper import composeCaseWorkshop, get_model_by, get_first_one_model

        _model = get_model_by(CronJob, object_id=items.get("object_id"))
        EnvId, pid, SuiteIdList = _model.EnvId, _model.pid, _model.SuiteIdList

        CronJob_object_id = _model.object_id
        alwaysSendMail = _model.alwaysSendMail
        alwaysWXWorkNotify = _model.alwaysWXWorkNotify

        alarmMailGroupList = _model.alarmMailGroupList
        alarmMailGroupList = str_list(alarmMailGroupList)

        mailGroup = []
        for x in range(len(alarmMailGroupList)):
            _tt = get_model_by(Email, object_id=alarmMailGroupList[x])
            if _tt != None:
                _email = str_list(_tt.mailGroup)
                mailGroup.extend(_email)

        # print("---------------------------------")
        # print(mailGroup)
        # print("---------------------------------")

        case = composeCaseWorkshop(EnvId=EnvId, ProjectId=pid, Interface=SuiteIdList)
        if case == None:
            # TypeError
            raise DBError({'status': 'failed', 'data': '找不到可用项目\接口'})


        result = send_and_save_report_BySuite(case, action=action)
        if result:
            _report = get_first_one_model(TestReport)
            # 发送邮件通知
            if alwaysSendMail:
                subject = Platform_name
                PassRate = '{:.2%}'.format(_report.passCount / _report.totalCount)
                content_result = "<font color='green'>PASS</font>"
                if _report.totalCount > _report.passCount:
                    content_result = "<font color='red'>FAIL</font>"
                content_text = "<h2>Hi~. 印萌 Dears:</h2>" \
                    "<div style='font-size:20px'>&nbsp;&nbsp;KB_iTest API Test TaskJob executed successfully!<br/>" \
                    "&nbsp;&nbsp;Cron Job ID:&nbsp;&nbsp; <b>{}</b><br/>" \
                    "&nbsp;&nbsp;Environment:&nbsp;&nbsp; <b>{}</b><br/>" \
                    "&nbsp;&nbsp;Status:&nbsp;&nbsp; <b>{}</b><br/>" \
                    "&nbsp;&nbsp;TotalAPICount:&nbsp;&nbsp; <b>{}</b><br/>" \
                    "&nbsp;&nbsp;PassAPICount:&nbsp;&nbsp; <b>{}</b><br/>" \
                    "&nbsp;&nbsp;PassRate:&nbsp;&nbsp; <b>{}</b><br/>" \
                    "&nbsp;&nbsp;<a href=\"http://{}/testReport/{}\">Please login platform " \
                    "for details!</a><br/>" \
                    "&nbsp;&nbsp;Report ID: {}<br/>" \
                    "&nbsp;&nbsp;Generated At: {} CST</div>" \
                    .format(
                        CronJob_object_id,
                        _report.EnvName,
                        content_result,
                        _report.totalCount,
                        _report.passCount,
                        PassRate,
                        "127.0.0.1:80",
                        _report.object_id,
                        _report.object_id,
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                    )

                for index in range(len(alarmMailGroupList)):
                    _email_list = get_model_by(Email, object_id=alarmMailGroupList[index])
                    print(11111111111, _email_list)
                    if _email_list != None:
                        mailGroup = str_list(_email_list.mailGroup) # 字符串 转 list
                        res = send_email(mailGroup, subject, content_text)
                        print("邮件发送结果", res)
                    else:
                        pass

            if alwaysWXWorkNotify:
                content_result = "PASS"
                if _report.totalCount > _report.passCount:
                    content_result = "Fail"
                content_text = '''> Hi~. 印萌小伙伴们:
API Test TaskJob executed successfully!
定时任务名： {}
测试结果：   {}
用例总数：   {}
通过总数：   {}
通过比例：   {}
测试报告 ID：{}
有关详细信息:{}
                '''.format(
                    CronJob_object_id,
                    content_result,
                    _report.totalCount,
                    _report.passCount,
                    '{:.2%}'.format(_report.passCount / _report.totalCount),
                    _report.object_id,
                    "0.0.0.0",
                )
                send_wxwork_notify(content_text)


        #     elif _model.alwaysSendMail == 0:
        #         print("不发 - 邮件")

        # else:
        #     print("获取报告失败")
        #     return False
