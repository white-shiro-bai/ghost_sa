# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")

# 身份识别
who_am_i = 'ghost_sa' #向外发送回调请求时的UA识别


# 数据查询接口的验证密码

admin_password = 'admin' #普通查询密码
admin_override_code = 'override' #越权密码
admin_do_not_track_code = 'dntmode' #cdn模式不参与记录密码

# 是否使用Kafka

use_kafka = True #True时，数据写入kafka。False时，直接插入数据库

# 是否开启properties表
use_properties = True # True时，会插入properties表，这个表不是必须的，只是方便提取数据时快速找到埋点里包含的变量。

# 移动广告回调支持

aso_dsp_callback_event = '$AppStart' #触发广告回调和UTM更新的事件，默认为APP启动后触发。注意，无论下一行是否开启回调，都会触发UTM更新。
aso_dsp_callback = True #Ture时，开启移动广告回调，False时，下面的配置都不会生效
aso_dsp_callback_interval_days = 3 #回调追溯期，单位为3天，会查找对应设备3天内是否有广告记录，如果有则会回调最近的一条记录。
aso_dsp_callback_repeat = False #是否允许重复回调，默认为不允许。有的触发事件可能会重复出现，如果该值为True，则每次触发都会发生回调，如果为False，则只有在第一次触发该事件时回调。
aso_dsp_callback_history = False #是否允许回调非首日用户。记是否判断['properties']['$is_first_day']这个值。默认为False,即用户只有在第一天安装并启动APP的时候，才会进行回调。如果这个值改为True，那无论是否首日，用户启动APP都会取寻找追溯期内的地址进行回调，对数据库压力较大。

# 自定义动作触发器

independent_listener = False #True时需要独立进程订阅kafka消息执行触发器。False时会在进行入库操作时执行触发器。如果不需要触发器功能，选择True，然后不运行触发器进程就行了。
# independent_listener_kafka_client_group_id='trigger_listener' #独立的订阅组名字
independent_listener_kafka_client_group_id='trigger_listener2' #trigger独立的订阅组名字(会拼在kafka.py的group_id后面)
independent_listener_kafka_client_client_id = 'trigger_listener2'#trigger独立的订阅组名字(会拼在kafka.py的client_id后面)

# 宝贝回家公益项目

# 默认启用宝贝回家公益项目功能，启用后，程序报错时会显示宝贝回家公益页面。并在链接处显示您的项目名和错误代码。不启用该功能时，则直接显示您的留言。
use_bbhj = True
bbhj_keyword = '你的请求不合法哟。有兴趣的话，点击查看源码哟'
bbhj_url = 'https://github.com/white-shiro-bai/ghost_sa/'

# 黑名单
# 开启黑名单增删改查
recall_blacklist_commit = True
# 开启黑名单过滤
recall_blacklist_query = True

#ip透传
user_ip_first = True    # user_ip_key字段优先作为用户ip。当检测到埋点里有 user_ip字段时，优先使用。使后端的埋点ip显示为用户ip，而非服务器ip。
user_ip_key = '$ip'     # 后端上报埋点时传递ip用的key。

# 接入控制
access_control_commit_mode = 'access_control'                       # 接入控制数据的提交模式，默认 'trigger' 为使用trigger.py进程（建议）。'kafka_consumer'为使用kafka_consumer.py方式提交。'access_control'为独立进程方式提交，该方法可以用来独立控制内存消耗，不过会多消耗一份kafka订阅。'none_kafka'该方法仅在use_kafka是False时有效，不建议在没有kafka的环境下使用。'false'为关闭接入控制提交信息
access_control_kafka_client_group_id = 'access_control_group'       # 接入控制使用独立的kafka订阅时，会在kafka_op的group_id后面拼上的名字(会拼在kafka.py的group_id后面)
access_control_kafka_client_client_id = 'access_control_client'     # 接入控制使用独立的kafka订阅时，会在kafka_op的group_id后面拼上的名字(会拼在kafka.py的client_id后面)
access_control_query = True                             # 开启登录控制查询，当状态为False时，统一返回通过状态
access_control_cdn_mode_write = 'event'                 # cdn_mode的数据进入后的处理方式。'none'为直接抛掉不写入数据库，但不影响接入控制工作，主要是减少数据库数据量。'event'模式为只插入event表，不插入device表，这样会保留所有的cdn_mode的请求记录，没有update动作，所以性能不受影响。'device'则跟普通埋点一样进库。
access_control_query_hour = 1                           # 黑名单生效时间，0为只有当前时间生效，1-23小时数为向前封禁的时间，如2时，则除当前小时生效外，向前2小时内的黑名单也生效。最大不超过23
access_control_max_memory = 100000000                   # 单位byte。默认是100000000(1G)。控制模块缓存最大允许使用的内存，达量即写入access_control表
access_control_max_memory_gap = 30                      # 查询内存使用量的间隔，默认是30秒。间隔越小，越精准，但是每次查询需要浪费1秒时间。间隔越大，越容易控制不住爆内存。该值续小于access_control_max_window，否则没意义。
access_control_max_window = 300                         # 单位是秒。默认是300(5分钟)。如果一直没触发内存上限，则每10分钟写一次access_control表
access_control_add_on_key = 'coupon_id'                 # 辅助key。默认是coupon_id，即除了distinct_id,ip之外，另一个独立用来判断数量的key。该key也需要埋点，如果为空，即''的时候，则不提取辅助key。
access_control_sum_count = 500                          # 默认是500，分片时间内，所有埋点的触发阈值和。
access_control_event_default = 100                      # 默认是100，分片时间内，如果没有在properties表里查到进入接入控制清单的数量，也没在project_list表里查到该项目的缺省值，则使用全局缺省数量
access_control_force_result_record = False              # 记录所有的查询结果，如果该值为False，则只记录返回命中的记录（普通模式，记录命中的。CDN模式，记录不通过的）。该值为True时，记录所有的查询结果。不论True还是False。数据返回格式按照模式指定的返回，不会强制使用CDN模式。该记录通常用来处理用户投诉和核算节约费用，放行的记录没太大意义，还浪费资源。
access_control_force_cdn_record = False                 # 该记录值为True时，无论是否采用CDN模式的查询，都会在进一份CDN埋点进CDN事件。意义是无论什么接口进数据，都会对CDN查询造成影响，进一步限制CDN消费。当该记录值为False时，只有CDN模式的请求，会被记录到埋点，其他的请求，埋点由请求端上报，以获得更正确更清晰的数据。\
access_control_cdn_mode_distinct_id_check = True        # CDN模式是否查验distinct_id。
access_control_cdn_mode_distinct_id_token_check = True  # CDN模式是否查验distinct_id与token的匹配度。默认关。
access_control_cdn_mode_mega_match = False              # CDN模式是否参考其他event作为封禁依据。当False时，CDN模式只核对event是cdn_mode的事件。
access_control_distinct_id_per_ip = 4                   # ip触发进入黑名单的量是distinct_id的阈值的倍数
access_control_ip_per_ip_group = 3                      # ip组触发进入黑名单的量是ip的阈值的倍数
