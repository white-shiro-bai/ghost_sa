# -*- coding: utf-8 -*-
#
# Date: 2022-08-17 09:08:01
# Author: unknowwhite@outlook.com
# WeChat: Ben_Xiaobai
#LastEditTime: 2022-08-31 23:57:11
#FilePath: \ghost_sa_github_cgq\docs\从零开始的数据分析\python_track_demo.py
#
import sys
import traceback

sys.path.append('./')
import sensorsanalytics
import datetime
import time

# 这是SDK配置，不同的SDK请参考各自的SDK配置方法
def sa_report(properties={}, event_name='demo'):
    SA_SERVER_URL = (
        'http://192.168.193.28:8000/sa.gif?project=test_me&remark=python'  # 生产
    )
    # SA_SERVER_URL = 'http://www.dreamyou.net:7332/sa.gif?project=test_app&remark=python' #生产
    # SA_SERVER_URL = 'http://www.dreamyou.net:7333/sa.gif?project=test_app&remark=python' #测试
    # SA_REQUEST_TIMEOUT = 10000
    # DefaultConsumer 是同步发送数据，因此不要在任何线上的服务中使用此 Consumer
    consumer = sensorsanalytics.DefaultConsumer(SA_SERVER_URL)
    # 使用 Consumer 来构造 SensorsAnalytics 对象
    sa = sensorsanalytics.SensorsAnalytics(consumer)
    distinct_id = 'python_demo_user'
    properties['$time'] = datetime.datetime.now()
    properties['version'] = 20190410.01
    properties['env'] = 'linux_python_3.6'
    # properties['returnstatus'] = returnstatus
    # properties['owner'] = 'Ben'
    # print(properties)
    sa.track(distinct_id, event_name, properties)
    # 记录用户登录事件
    sa.close()

def normal_track(event_name='demo',properties={},tracking_enable=True):
    # 在标准track上封装一层，控制整体关闭和跳过的list
    skip_event_list = ['skip_demo1','skip_demo2']
    if tracking_enable == True and event_name not in skip_event_list:
        sa_report(event_name=event_name,properties=properties)


# 这是推荐的埋点封装方法，请参考各自的SDK进行
class python_track:
    def __init__(self, event='', eventdata={}, owner='undefined',event_enable=True):
        self.event = event
        self.eventdata = eventdata
        self.eventdata['owner'] = owner
        self.timestart = time.time()
        self.apitimestart = time.time()
        self.event_enable = event_enable
        self.track(action=1)

    def track(self, action=0, oncedata={}):
        if action in (100,600):
            self.apitimestart = time.time()
            self.eventdata['user_mainstory_timecost'] = int((time.time() - self.timestart) * 1000)
            # 所有的后续event带上主要进程完成时间
        self.trackdata = dict(self.eventdata)
        self.trackdata.update(oncedata)
        self.trackdata['action'] = action
        self.trackdata['event_duration'] = int((time.time() - self.timestart) * 1000)
        # 所有的action都带上相对初始化的基础时间
        if action in (200,400,700,800):
            self.trackdata['api_timecost'] = int((time.time() - self.apitimestart) * 1000)
            # api请求成功的时候自动带时间
        if self.event_enable == True:
            normal_track(properties=self.trackdata, event_name=self.event)
            # 可以独立关闭某个埋点用于测试

    def __del__(self):
        class_name = self.__class__.__name__
        print(class_name, '已销毁')


# 这是一个埋点的具体示例
def demo_app(demotype='成功'):
    # 这是手机号注册登录的埋点演示
    # 用户在这一步拉起了登录注册模块
    track_login = python_track(
        event='login', eventdata={'invite_uid': '这是示例的邀请者uid', 'invite_type': '1'}
    )
    # 用户在这一步点击手机号登陆
    track_login.track(action=101)
    # 用户焦点离开了手机号输入框
    track_login.eventdata['mobile'] = '用户输入的手机号'
    track_login.track(action=102)
    # 用户点击获取验证码
    track_login.track(action=103)
    # 用户输入验证码
    track_login.eventdata['captcha'] = '用户输入的验证码'
    # 用户点击同意协议
    track_agreement = python_track(event='agreement',eventdata={'scene':'login','agreement_url':'这是协议的url','agreement_title':'这是协议的标题','agreement_version':'这是协议的版本'})
    track_agreement.track(action=100)
    track_login.track(action=107)
    # 用户点击登录
    track_login.track(action=100)
    t1 = time.time()
    # 接口返回登录失败
    if demotype == '失败':
        time.sleep(1)
        track_login.track(
            action=106,
            oncedata={
                'reason': '后端返回的失败原因',
                'timecost': int((time.time() - t1) * 1000),
            },
        )
    # 接口返回登录成功
    elif demotype == '成功':
        track_login.track(
            action=200,
            oncedata={
                'method': '后端返回的注册方式',
                'is_sign_up': '后端返回的登录类型，1是注册并登录，2是登录',
                'timecost': int((time.time() - t1) * 1000),
            },
        )
    del track_login
    del track_agreement


if __name__ == "__main__":
    demo_app('成功')
    demo_app('失败')