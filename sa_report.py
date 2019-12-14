# -*- coding: utf-8 -*
import sensorsanalytics
import datetime

# 从神策分析配置页面中获取数据接收的 URL
def sa_report(properties,apiname,returnstatus):
    # print('埋点已关闭')
    # SA_SERVER_URL = 'https://t.tvcbook.com/sa?project=production' #生产
    SA_SERVER_URL = 'http://10.16.4.160:8000/sa.gif?project=test_app&remark=python' #测试

    # SA_REQUEST_TIMEOUT = 10000
    # DefaultConsumer 是同步发送数据，因此不要在任何线上的服务中使用此 Consumer
    consumer = sensorsanalytics.DefaultConsumer(SA_SERVER_URL)
    # 使用 Consumer 来构造 SensorsAnalytics 对象
    sa = sensorsanalytics.SensorsAnalytics(consumer)
    distinct_id = 'python_toplist_api'
    properties['owner'] = 'Ben'
    properties['$time'] = datetime.datetime.now()
    properties['apiname'] = apiname
    properties['apiversion'] = 20190410.01
    properties['apienv'] = 'linux_python_3.6'
    properties['returnstatus'] = returnstatus
    # properties['owner'] = 'Ben'
    # print(properties)
    sa.track(distinct_id, 'API', properties)
    # 记录用户登录事件
    sa.close()

if __name__ == "__main__":
  sa_report(properties={},apiname='test',returnstatus='ok')