import smtplib
import requests
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.common.decorator import async_test
from settings import Config


@async_test
def send_email(to_list, subject, content, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = Header("K.B_itest", 'utf-8')
        msg['To'] = ";".join(to_list)
        msg['Subject'] = Header(subject, 'utf-8')
        txt = MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)
        if attachment:
            # 添加附件
            part = MIMEApplication(open(attachment, 'rb').read())
            part.add_header('Content-Disposition',
                            'attachment',
                            filename=attachment)
            msg.attach(part)
        s = smtplib.SMTP_SSL(Config.MAIL_SERVER, int(Config.MAIL_PORT))
        s.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        s.send_message(msg, Config.MAIL_USERNAME, to_list)
        s.quit()
        return True, 'email send successfully'
    except smtplib.SMTPException as e:
        return False, 'SMTPException : %s' % str(e)
    except BaseException as e:
        return False, 'Exception : %s' % str(e)


@async_test
def send_wxwork_notify(content,
                        mentioned_mobile_list=["@all"],
                        headers=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    if not mentioned_mobile_list or not isinstance(mentioned_mobile_list,
                                                   list):
        raise TypeError("mentioned_mobile_list should be a list!")
    hook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + Config.WEBHOOK
    data = {
        "msgtype": "text",
        "text": {
            "content": "{}".format(content),
            "mentioned_mobile_list": mentioned_mobile_list
        }
    }
    notify_res = requests.post(url=hook_url, json=data, headers=headers)
    return notify_res
