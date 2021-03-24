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

use_kafka = True #True时，数据写入kafka。False时，直接插入数据库

# 是否开启properties表

use_properties = True #True时，会插入properties表，这个表不是必须的，只是方便提取数据时快速找到埋点里包含的变量。

# 移动广告回调支持

aso_dsp_callback_event = '$AppStart' #触发广告回调和UTM更新的事件，默认为APP启动后触发。注意，无论下一行是否开启回调，都会触发UTM更新。
aso_dsp_callback = True #Ture时，开启移动广告回调，False时，下面的配置都不会生效
aso_dsp_callback_interval_days = 3 #回调追溯期，单位为3天，会查找对应设备3天内是否有广告记录，如果有则会回调最近的一条记录。
aso_dsp_callback_repeat = False #是否允许重复回调，默认为不允许。有的触发事件可能会重复出现，如果该值为True，则每次触发都会发生回调，如果为False，则只有在第一次触发该事件时回调。
aso_dsp_callback_history = False #是否允许回调非首日用户。记是否判断['properties']['$is_first_day']这个值。默认为False,即用户只有在第一天安装并启动APP的时候，才会进行回调。如果这个值改为True，那无论是否首日，用户启动APP都会取寻找追溯期内的地址进行回调，对数据库压力较大。

# 自定义动作触发器

independent_listener = False #True时需要独立进程订阅kafka消息执行触发器（trigger.py）。False时会在进行入库操作时执行触发器。如果不需要触发器功能，选择True，然后不运行触发器进程就行了。
independent_listener_kafka_client_group_id='trigger_listener' #独立的订阅组名字

# 宝贝回家公益项目

use_bbhj = True #默认启用宝贝回家公益项目功能，启用后，程序报错时会显示宝贝回家公益页面。并在链接处显示您的项目名和错误代码。不启用该功能时，则直接显示您的留言。

bbhj_keyword = '你的请求不合法哟。有兴趣的话，点击查看源码哟'
bbhj_url = 'https://github.com/white-shiro-bai/ghost_sa/'

#黑名单

recall_blacklist_commit = True #开启黑名单增删改查
recall_blacklist_query= True #开启黑名单过滤
