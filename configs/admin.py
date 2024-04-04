# -*- coding: utf-8 -*-
#
#Date: 2021-09-18 16:29:59
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai

#batch_send_deduplication
batch_send_deduplication_mode = 'consumer' #skip same track_id ,distinct_id , lib , all_json['time'] data insert into event table in max_timeout. default
        # 'none' is disable.
        # 'ram' mode keep cache in flask_app and not share cache in multi instance .
        # 'consumer' mode do nothing in flask_app. comsumer.py will do deduplication job . It is the most safety way.
        # 'redis' mode use redis to share cache with multi instance , it support both speed and scale.
        # 'tidb6.5+' mode require tidb version >=6.5.  use db to share cache with multi instance , it support big scale.
        # 'tidb6.4-' mode support almost mysql protocol db. use db to share cache with multi instance , it support big scale.
        # 'mysql' mode support mysql 5.7+ . use inno-db engine to share cache with multi instance , it support big scale.
        # 'mysql-memory' mode support mysql 5.7+ . use mysql memory engine to share cache with multi instance , it support big scale.
batch_send_deduplication_insert = 'remark' #'skip' or 'remark' duplication data.
        # 'remark' is default setting, both normal and duplication date will insert into database . duplication data will be add aa "du-" chart before original remark. for example, normal data will insert as remark = 'normal', duplication date will insert as remark = 'du-normal' . 'remark' mode provide one more chance to verify data. 
        # 'skip' will skip duplication data and no record left.
# batch_send_deduplication_at = 'consumer' #consumer
batch_send_max_memory_limit  = 20000000 #unit byte。default is 20000000(200M), if thread use memory exceed setting , delete oldest catch.
batch_send_max_memory_gap = 60 #unit seconds. frequency what memory occupied chech. default is 30 seconds , tiny value provide accurate but cost more interrupt , huge value have better performace but lead more risk on OOM. Data lost is annoying even it can be recovery by event table. this value should be smaller then batch_send_max_window.
batch_send_max_batch_key_limit = 200000 #unit item. batch_key = distinct_id+lib . cache clean will apply when size of batch_key meet limit nomatter max memory limit.
batch_send_max_window = 60 #unit minutes. batch cache expired window. affect on ram and redis. default is 60 minutes. batch_key in cache that not update in window will be delete when batch_send_max_memory_limit or batch_send_max batch_key_limit reached.
batch_send_redis_db_number = 1 # redis database number .


#Database
database_type = 'redis' # type for database. 'tidb' support from tidb(https://docs.pingcap.com/zh/tidb/stable/?utm_source=ghost_sa),tested from tidb v3.0.0 to v5.1.1 and newer. 'mysql' support mysql from v5.7 to v8 and newer.'tidb-serverless' support tidb_serverless #! WARNING: Do not use Ghost_sa with mysql in a production deployment , it runs very slow.

serverless_system = 'RedHat' # this setting only effect 'tidb-serverless' mode,it can support 'MacOS','Debian','RedHat','Alpine','OpenSUSE'，'Windows'.'Debian' include Debian / Ubuntu / Arch and 'RedHat' include RedHat / Fedora / CentOS / Mageia.

ca_local = {'MacOS':'/etc/ssl/cert.pem','Debian':'/etc/ssl/certs/ca-certificates.crt','RedHat':'/etc/pki/tls/certs/ca-bundle.crt','Alpine':'/etc/ssl/cert.pem','OpenSUSE':'/etc/ssl/ca-bundle.pem','Windows':'cacert.pem'} 

#pic_tools
font = './fonts/NotoSerifCJKsc-Regular.otf' #Font file path for pic_tools.

#Bot Identify
bot_list = ['spider','googlebot','adsbot-google','baiduboxapp','bingpreview','bingbot'] # If there any string in User_Agent,the request will be set remark as 'spider' ,no matter what the original remark is . Maintain bot list in lower case.
<<<<<<< HEAD

#Info skip
unrecognized_info_skip = ['url的domain解析失败','取值异常','未取到值,直接打开','未取到值','未取到值_非http的url','取值异常_referrer异常_','hostname解析异常','未知搜索引擎', 'url_host取值异常','获取url异常','url解析失败'] #unrecognized utm and other info list. Utm and info will update to {project}_device if they not in this list.

#Performance Enchance
combine_device_type = 'original' # 'original' mode is fit for tidb , every event can update device table. As the reason original mode leads a low performance in None tidb environment , but it provide a stateless compatibility. 'memcache_once' mode use memory to cache device update and combine the same info except update time,finally each distinct_id have a row.'memcache_session' mode use memory to cache device update with a session id and detect idle time,data will be insert to device table with session id which each session have a row.
combine_device_memory = 100000000 #unit byte。default is 100000000(1G), if thread use memory exceed setting , insert all cache into table first.
combine_device_max_memory_gap = 30 #frequency what memory occupied chech. default is 30 seconds , tiny value provide accurate but cost more interrupt , huge value have better performace but lead more risk on OOM. Data lost is annoying even it can be recovery by event table. this value should be smaller then combine_device_max_window.
combine_device_max_window = 300 #unit seconds。default is 300(every 5 minutes). Force insert device table after window since last insert if max_memory or gap not trigger insert.
combine_device_max_distinct_id = 1000 #unit keys. default is 1000.if cached distinct id reach the limit , insert all cache into table first.
combine_device_multiple_threads = 6 # insert treads. between 2 and 9 is good depend on your database performance.Data insert have retry times to avoid data lost when database busy or connection unstable, 1 is not a good idea at lock table , only 1 thread with retry function can jam the process on a single lock.

bot_override = True # allow insert into event table with specific remark if no_bot=admin_password otherwise remark force to spider. 

# 身份识别
who_am_i = 'ghost_sa' #向外发送回调请求时的UA识别


# 数据查询接口的验证密码

admin_password = 'admin' #普通查询密码
admin_override_code = 'override' #越权密码
admin_do_not_track_code = 'dntmode' #cdn模式不参与记录密码

# 是否使用Kafka

use_kafka = True #True时，数据写入kafka。False时，直接插入数据库
consumer_workers = 9 #使用kafka时，消费者的数量。标准部署tidb，9个效果比较好。请根据数据库压力调节。不是越大越好。

#Performance and Feature

fast_mode = 'fast' # 'original','fast','boost'。original mode is start from ghost_sa earliest version, update all data in db tables. fast mode is use memory to cache data, and update data into db tables. boost mode write data like fast mode, but close all trys to enhance performance, it fastest but may cause data lost at abnormal data collection request.

# 是否开启properties表
use_properties = False #True时，会插入properties表，这个表不是必须的，只是方便提取数据时快速找到埋点里包含的变量。

#Device Table
device_source_update_mode = 'restrict' #'restrict','first_sight','latest_sight'。this setting control device first source column update mode .
# 'restrict' mode is limit update device table only when the row insert first time no matter value , it suite for a brand new project,restrict mode will log the real first source.
# 'first_sight' mode is update device table when the column is empty and income data is valued ,it useful to patch all source , it is the default mode of 2.0 ghost_sa .
# 'latest_sight' mode is update column no matter the status when income data is valued, it the mode of 1.0 ghost_sa.

# device_latest_info_update_mode = 'restrict' #'restrict','latest_sight'。this setting control device latest info column update mode .
# # 'restrict' mode is limit update device table only when the row insert first time no matter value , it suite for a brand new project,restrict mode will log the real latest info.


#IP地址转化
#IP_Address dictionary
ip_city_mode = 'all' #mode for ip_city. 'all' for all info. 'language' for only language selected , it was designed for saving storage spaces. default value : "all"
ip_city_language = ['zh-CN', 'en'] #only work at "language" mode. ip_city will only return information in matched language.It had better to be contained more then one primary language if ghost_sa worked in an international project as the reason is not every ip address has the result in primary language. defult value : ['zh-CN', 'en']
        #   *language support:
        #   * de -- German
        #   * en -- English names may still include accented characters if that is the accepted spelling in English. In other words, English does not mean ASCII.
        #   * es -- Spanish
        #   * fr -- French
        #   * ja -- Japanese
        #   * pt-BR -- Brazilian Portuguese
        #   * ru -- Russian
        #   * zh-CN -- Simplified Chinese.

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

use_bbhj = True #默认启用宝贝回家公益项目功能，启用后，程序报错时会显示宝贝回家公益页面。并在链接处显示您的项目名和错误代码。不启用该功能时，则直接显示您的留言。

bbhj_keyword = '你的请求不合法哟。有兴趣的话，点击查看源码哟'
bbhj_url = 'https://github.com/white-shiro-bai/ghost_sa/'

#黑名单
recall_blacklist_commit = True #开启黑名单增删改查
recall_blacklist_query= True #开启黑名单过滤

#ip透传
user_ip_first = True #user_ip_key字段优先作为用户ip。当检测到埋点里有 user_ip字段时，优先使用。使后端的埋点ip显示为用户ip，而非服务器ip。
user_ip_key = '$ip' # 后端上报埋点时传递ip用的key。

#接入控制
access_control_commit_mode = 'none_kafka' #接入控制数据的提交模式，默认 'trigger' 为使用trigger.py进程（建议）。'kafka_consumer'为使用kafka_consumer.py方式提交。'access_control'为独立进程方式提交，该方法可以用来独立控制内存消耗，不过会多消耗一份kafka订阅。'none_kafka'该方法仅在use_kafka是False时有效，不建议在没有kafka的环境下使用。'false'为关闭接入控制提交信息
access_control_kafka_client_group_id='access_control_group'# 接入控制使用独立的kafka订阅时，会在kafka_op的group_id后面拼上的名字(会拼在kafka.py的group_id后面)
access_control_kafka_client_client_id='access_control_client'# 接入控制使用独立的kafka订阅时，会在kafka_op的group_id后面拼上的名字(会拼在kafka.py的client_id后面)
access_control_query = True #开启登录控制查询，当状态为False时，统一返回通过状态
access_control_cdn_mode_write = 'event' #cdn_mode的数据进入后的处理方式。'none'为直接抛掉不写入数据库，但不影响接入控制工作，主要是减少数据库数据量。'event'模式为只插入event表，不插入device表，这样会保留所有的cdn_mode的请求记录，没有update动作，所以性能不受影响。'device'则跟普通埋点一样进库。
access_control_query_hour = 1 #黑名单生效时间，0为只有当前时间生效，1-23小时数为向前封禁的时间，如2时，则除当前小时生效外，向前2小时内的黑名单也生效。最大不超过23
access_control_max_memory = 100000000 #单位byte。默认是100000000(1G)。控制模块缓存最大允许使用的内存，达量即写入access_control表
access_control_max_memory_gap = 30 #查询内存使用量的间隔，默认是30秒。间隔越小，越精准，但是每次查询需要浪费1秒时间。间隔越大，越容易控制不住爆内存。该值续小于access_control_max_window，否则没意义。
access_control_max_window = 300 #单位是秒。默认是300(5分钟)。如果一直没触发内存上限，则每10分钟写一次access_control表
access_control_add_on_key = 'coupon_id' #辅助key。默认是coupon_id，即除了distinct_id,ip之外，另一个独立用来判断数量的key。该key也需要埋点，如果为空，即''的时候，则不提取辅助key。
access_control_sum_count = 500 #默认是500，分片时间内，所有埋点的触发阈值和。
access_control_event_default = 100 #默认是100，分片时间内，如果没有在properties表里查到进入接入控制清单的数量，也没在project_list表里查到该项目的缺省值，则使用全局缺省数量
access_control_force_result_record = False #记录所有的查询结果，如果该值为False，则只记录返回命中的记录（普通模式，记录命中的。CDN模式，记录不通过的）。该值为True时，记录所有的查询结果。不论True还是False。数据返回格式按照模式指定的返回，不会强制使用CDN模式。该记录通常用来处理用户投诉和核算节约费用，放行的记录没太大意义，还浪费资源。
access_control_force_cdn_record = False #该记录值为True时，无论是否采用CDN模式的查询，都会在进一份CDN埋点进CDN事件。意义是无论什么接口进数据，都会对CDN查询造成影响，进一步限制CDN消费。当该记录值为False时，只有CDN模式的请求，会被记录到埋点，其他的请求，埋点由请求端上报，以获得更正确更清晰的数据。\
access_control_cdn_mode_distinct_id_check = True #CDN模式是否查验distinct_id。
access_control_cdn_mode_distinct_id_token_check = True #CDN模式是否查验distinct_id与token的匹配度。默认关。
access_control_token_means_override = False #如果CDN模式下使用参数传递distinct_id且token被认可，则等效override密码正确。
access_control_cdn_mode_mega_match = False #CDN模式是否参考其他event作为封禁依据。当False时，CDN模式只核对event是cdn_mode的事件。
access_control_distinct_id_per_ip = 4 # ip触发进入黑名单的量是distinct_id的阈值的倍数
access_control_ip_per_ip_group = 3 # ip组触发进入黑名单的量是ip的阈值的倍数
access_control_ip_group_per_ip_group_extend = 5 # 超大IP组触发进入黑名单的量是ip组的倍数
access_control_check_ip_group_extend = True # 是否拦截进入超大IP组的IP
access_control_per_add_on_key = 50 # add_on_key触发进入黑名单的量是distinct_id的阈值的倍数