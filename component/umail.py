# -*- coding: utf-8 -*-
#
#Date: 2022-01-24 16:35:57
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2022-02-24 15:44:01
#FilePath: \ghost_sa_github\component\umail.py
#
import sys
sys.path.append('./')
import requests, base64
from configs import umail
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from configs.export import write_to_log
from component.public_value import getdate
from component.recall_blacklist import blacklist_commit
import time
import xmltodict

def send_umail(to_addr='unknowwhite@outlook.com',from_addr=umail.umail_user,subject='鬼策测试邮件标题',html="""<p>鬼策测试邮件正文</p><p><a href="https://github.com/white-shiro-bai/ghost_sa">这是一个测试链接</a></p>""",sender_alias = umail.umail_alias):
    message = MIMEText(html, 'html', 'utf-8')
    message['From'] = formataddr([sender_alias,from_addr]) #括号里的对应发件人邮箱昵称（随便起）、发件人邮箱账号
    message['To'] = Header(to_addr, 'utf-8') #括号里的对应收件人邮箱昵称、收件人邮箱账号
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP(host=umail.umail_host, port=umail.umail_port)
        smtpObj.login(umail.umail_user, umail.umail_pass)
        smtpObj.sendmail(from_addr, to_addr, message.as_string())
        return 'success'
    except smtplib.SMTPException as e:
        write_to_log(filename='email',defname='send_email',result=str(e))
        return str(e)

def check_fail(date='2022-01-24'):
    api_url = f'http://www.bestedm.net/mm-ms/apinew/failexport.php?date={date}&date_end={date}&type=all&out_type=xml'
    print(api_url)
    auth = str(base64.b64encode(f'{umail.web_username}:{umail.web_password}'.encode('utf-8')), 'utf-8')
    header = {'Authorization': f'Basic {auth}'}
    result = requests.get(url=api_url,headers=header)
    xml_parse = xmltodict.parse(result.text)
    # return json.loads(json.dumps(xml_parse['fail_recipient_list']['recipient'],indent=1))
    return xml_parse['fail_recipient_list']['recipient']

def update_blacklist(target='yesterday'):
    date = getdate(target)
    result = check_fail(date=date)
    if not isinstance(result ,list):
        result = [result]
    for i in result:
        timenow = int(time.time())
        if str(i['error_type'])  in ("4","2"):
            status = 54
        else:
            status = 40
        commit = blacklist_commit(data={'project':umail.default_project,'distinct_id':None,'owner':'umail','key':i['email'],'type':81,'comment':i['error_type_dec'],'status':status,'timenow':timenow})
        commit.add_by_import()
    
if __name__ == '__main__':
    # print(send_umail())
    # check_fail(date='2022-01-24')
    # check_reason()
    update_blacklist(sys.argv[1])