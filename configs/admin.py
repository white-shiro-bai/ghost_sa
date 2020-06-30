# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")

# 身份识别
who_am_i = 'ghost_sa' #向外发送回调请求时的UA识别


# 数据查询接口的验证密码

admin_password = 'admin'

# 是否使用Kafka

use_kafka = False #True时，数据写入kafka。False时，直接插入数据库

# 是否开启properties表

use_properties = True #True时，会插入properties表，这个表不是必须的，只是方便提取数据时快速找到埋点里包含的变量。

# 移动广告回调支持

aso_dsp_callback = True #Ture时，开启移动广告回调，False时，下面的配置都不会生效
aso_dsp_callback_event = '$AppStart' #触发广告的事件，默认为APP启动后触发
aso_dsp_callback_interval_days = 3 #回调追溯期，单位为3天，会查找对应设备3天内是否有广告记录，如果有则会回调最近的一条记录。
aso_dsp_callback_repeat = False #是否允许重复回调，默认为不允许。有的触发事件可能会重复出现，如果该值为True，则每次触发都会发生回调，如果为False，则只有在第一次触发该事件时回调。