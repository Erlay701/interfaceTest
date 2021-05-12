# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import datetime
import os, sys
import base64

import getpathInfo
import readConfig

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

read_conf = readConfig.ReadConfig()
subject = read_conf.get_email('SUBJECT')  # 从配置文件中读取，邮件主题
SUBJECT = str(datetime.datetime.now())[0:19] + '%s' % subject  # 邮件主题
RECEIVER = read_conf.get_email('TO')  # 从配置文件中读取，邮件收件人
SENDER = read_conf.get_email('FROM')  # 从配置文件中读取，邮件抄送人
USER = read_conf.get_email('user')
PWD = read_conf.get_email('password')
HOST = read_conf.get_email('HOST_SERVER')
mail_path = os.path.join(getpathInfo.get_Path(), 'result')


class SendEmail(object):

    def send_email(self,resultPath):
        """
        定义发送邮件
        :param file_new:
        :return: 成功：打印发送邮箱成功；失败：返回失败信息
        """
        file = resultPath
        msg = MIMEMultipart()
        if file:
            file_name = os.path.split(file)[-1]
            try:
                f = open(file, 'rb')
                mail_body = f.read()
            except Exception as e:
                raise Exception('附件打不开！！！！')
            else:
                att = MIMEText(mail_body, "base64", "utf-8")
                att["Content-Type"] = 'application/octet-stream'
                # base64.b64encode(file_name.encode()).decode()
                new_file_name = '=?utf-8?b?' + base64.b64encode(file_name.encode()).decode() + '?='
                # 这里是处理文件名为中文名的，必须这么写
                att["Content-Disposition"] = 'attachment; filename="%s"' % new_file_name
                msg.attach(att)

        msgtext = MIMEText(mail_body, 'html', 'utf-8')
        msg.attach(msgtext)
        msg['Subject'] = SUBJECT
        msg['from'] = SENDER
        msg['to'] = RECEIVER

        try:
            server = smtplib.SMTP_SSL(HOST, port=465)
            server.set_debuglevel(1)
            server.login(USER, PWD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())
            print("邮件发送成功！")
            server.quit()
        except Exception as e:
            print("失败: " + str(e))
