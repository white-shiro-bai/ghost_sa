# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from configs.export import write_to_log
from configs import email

def send_email(to_addr='unknowwhite@outlook.com',from_addr=None,subject='鬼策测试邮件标题',html="""<p>鬼策测试邮件正文</p><p><a href="https://github.com/white-shiro-bai/ghost_sa/">这是一个测试链接</a></p>"""):
    #使用Python发送HTML格式的邮件
    message = MIMEText(html, 'html', 'utf-8')
    message['From'] = Header(from_addr, 'utf-8') #括号里的对应发件人邮箱昵称（随便起）、发件人邮箱账号
    message['To'] = Header(to_addr, 'utf-8') #括号里的对应收件人邮箱昵称、收件人邮箱账号
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(host=email.mail_host, port=email.mail_port)
        smtpObj.login(email.mail_user, email.mail_pass)
        smtpObj.sendmail(from_addr, to_addr, message.as_string())
        return 'success'
    except smtplib.SMTPException as e:
        write_to_log(filename='email',defname='send_email',result=str(e))
        return str(e)

if __name__ == "__main__":
    print(send_email())