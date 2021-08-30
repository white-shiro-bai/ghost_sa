# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    app.configs.default

    This is the default configuration for app that every site should have.
    You can override these configuration variables in another class.
"""
import os
import sys
import datetime

_VERSION_STR = '{0.major}{0.minor}'.format(sys.version_info)


class DefaultConfig(object):
    # Get the app root path
    #            <_basedir>
    # ../../ -->  TOSC/app/configs/default.py
    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
        os.path.dirname(__file__)))))

    # 设置监听网段
    HOST = "0.0.0.0"

    # 设置运行端口号
    PORT = 8000

    # 启动进程数
    PROCESSES = 4

    # 启动线程数
    THREADS = 2

    # 项目名
    CALLABLE = "ghost_sa"

    # 项目启动文件
    MODULE = "wsgi"

    ENV = 'production'

    DEBUG = False
    TESTING = False

    # 开启支持debug模式下teardown_request捕获异常，默认不捕获
    # 默认情况下，如果应用工作在调试模式，请求上下文不会在异常时出栈来允许调试器内省。
    # 这可以通过这个键来禁用。你同样可以用这个设定来强制启用它，即使没有调试执行，
    # 这对调试生产应用很有用（但风险也很大）
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # Logs
    # If SEND_LOGS is set to True, the admins (see the mail configuration) will
    # recieve the error logs per email.
    SEND_LOGS = True

    # Set logging app name
    LOGGER_NAME = 'ghost_sa'

    # The filename for the info and error logs. The logfiles are stored at
    # app/logs
    INFO_LOG = "info"
    ERROR_LOG = "error"

    # 是否开启模版错误消息
    EXPLAIN_TEMPLATE_LOADING = True

    # 按照文件大小分割参数配置
    MAX_BYTES = 100000
    BACKUP_COUNT = 10

    # 按照时间分割参数配置
    BACKUP_WHEN = "midnight"
    BACKUP_COUNT = 62
    # 备份配置文件后缀名
    BACKUP_SUFFIX = "%Y%m%d-%H%M.log"

    # 日志格式化参数配置
    DEBUG_FORMATTER = "%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)s %(message)s"
    INFO_FORMATTER = "%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)s %(message)s"
    ERROR_FORMATTER = "%(asctime)s %(levelname)s %(pathname)s %(funcName)s lineNo=%(lineno)s processId=6%(process)d " \
                      "thread=%(thread)d  %(message)s"

    LOGSTASH_FORMATTER = "%(asctime)s %(levelname)s %(pathname)s %(funcName)s lineNo=%(lineno)s processId=6%(process)d " \
                         "thread=%(thread)d  %(message)s"

    # Default Database
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
    #                           'flaskbb.sqlite'
    # SQLALCHEMY_DATABASE_URI = "postgresql://app@localhost:5432/app"
    SQLALCHEMY_DATABASE_URI = 'mysql://tosc:w8Jr3RGy@localhost/tosc?charset=utf8'

    # 如果设置成True(默认情况)，Flask - SQLAlchemy
    # 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    # 指定数据库连接池的超时时间。默认是 10s
    SQLALCHEMY_POOL_TIMEOUT = 2

    # Security
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # Protection against form post fraud
    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    # Searching
    WHOOSH_BASE = os.path.join(_basedir, "whoosh_index", _VERSION_STR)

    # Auth
    LOGIN_VIEW = "auth.login"
    REAUTH_VIEW = "auth.reauth"
    LOGIN_MESSAGE_CATEGORY = "info"
    REFRESH_MESSAGE_CATEGORY = "info"

    # The name of the cookie to store the “remember me” information in.
    # Default: remember_token
    REMEMBER_COOKIE_NAME = "remember_token"
    # The amount of time before the cookie expires, as a datetime.timedelta object.
    # Default: 365 days (1 non-leap Gregorian year)
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=365)
    # If the “Remember Me” cookie should cross domains,
    # set the domain value here (i.e. .example.com would allow the cookie
    # to be used on all subdomains of example.com).
    # Default: None
    # REMEMBER_COOKIE_DOMAIN = None
    # Limits the “Remember Me” cookie to a certain path.
    # Default: /
    # REMEMBER_COOKIE_PATH = "/"
    # Restricts the “Remember Me” cookie’s scope to secure channels (typically HTTPS).
    # Default: None
    # REMEMBER_COOKIE_SECURE = None
    # Prevents the “Remember Me” cookie from being accessed by client-side scripts.
    # Default: False
    # REMEMBER_COOKIE_HTTPONLY = False

    # token session 时长，单位为秒，默认为30分钟
    SESSION_EXPIRE = 1800
    # 默认的生成token有效期，单位为秒，默认为30天
    TOKEN_EXPIRE = 30 * 24 * 60 * 60
    # 生成的app_token有效期，单位为秒，默认为7天
    APP_TOKEN_EXPIRE = 7 * 24 * 60 * 60
    # 生成的api_token有效期，单位为秒，默认为30分钟
    API_TOKEN_EXPIRE = 30 * 60

    # # Mail
    # MAIL_SERVER = "localhost"
    # MAIL_PORT = 25
    # MAIL_USE_SSL = False
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = "noreply@example.org"
    # MAIL_PASSWORD = ""
    # MAIL_DEFAULT_SENDER = ("Default Sender", "noreply@example.org")
    # # Where to logger should send the emails to
    # ADMINS = ["admin@example.org"]

    # # Google Mail Example
    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = "your_username@gmail.com"
    # MAIL_PASSWORD = "your_password"
    # MAIL_DEFAULT_SENDER = ("Your Name", "your_username@gmail.com")
    #
    # # The user who should recieve the error logs
    # ADMINS = ["your_admin_user@gmail.com"]

    # # Mail 163 开启SSL保护，关闭TLS，使用994端口，也可以使用465，不支持TLS协议
    # MAIL_SERVER = "smtp.163.com"
    # MAIL_PORT = 994
    # MAIL_USE_SSL = True
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = "xxxxx@163.com"
    # MAIL_PASSWORD = "xxxxx"
    # MAIL_DEFAULT_SENDER = ("Default Sender", "xxxxx@163.com")
    # # Where to logger should send the emails to
    # ADMINS = ["songxiaowei@travelsky.com"]

    # # Mail qq 开启SSL保护，关闭TLS，使用994端口
    # MAIL_SERVER = "smtp.qq.com"
    # MAIL_PORT = 465
    # MAIL_USE_SSL = False
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = "xxx@qq.com"
    # MAIL_PASSWORD = "xxxx"
    # MAIL_DEFAULT_SENDER = ("Default Sender", "xxxx@qq.com")
    # # Where to logger should send the emails to
    # ADMINS = ["songxiaowei@travelsky.com"]

    # # Mail qq 开启TLS保护，关闭SSL，使用587端口
    # MAIL_SERVER = "smtp.qq.com"
    # MAIL_PORT = 587
    # MAIL_USE_SSL = False
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = "xxxx@qq.com"
    # MAIL_PASSWORD = "xxxx"
    # MAIL_DEFAULT_SENDER = ("Default Sender", "xxxx@qq.com")
    # # Where to logger should send the emails to
    # ADMINS = ["songxiaowei@travelsky.com"]

    # TravelSky 开启SSL保护，关闭TLS，使用465端口
    MAIL_SERVER = "10.6.168.207"
    MAIL_PORT = 25
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "teamwork@travelsky.com"
    MAIL_PASSWORD = "12345abc"
    MAIL_DEFAULT_SENDER = ("Default Sender", "teamwork@travelsky.com")
    # 系统管理员，接收相关系统错误日志邮件
    ADMINS = ["teamwork@travelsky.com"]

    # Flask-Redis
    REDIS_ENABLED = False
    REDIS_URL = "redis://:travelskyopenstackcloud@10.237.43.105:6379/0"
    REDIS_DATABASE = 0

    # Celery
    CELERY_BROKER_URL = 'redis://:travelskycloud@localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://:travelskycloud@localhost:6379'
    # CELERY_TASK_SERIALIZER = 'msgpack'
    # CELERY_TASK_SERIALIZER = 'json'
    # CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True
    # CELERY_IMPORTS = ("tasks",)
    # # 定义任务队列
    # CELERY_QUEUES = (
    #     # 路由键以"task."开头的消息都进行default队列
    #     Queue('default', routing_key='task.#'),
    #     # 路由键以"web."开头的消息都进web_tasks队列
    #     Queue('web_task', routing_key='web.#')
    # )
    # # 默认的交互机名字为tasks
    # CELERY_DEFAULT_EXCHANGE = 'tasks'
    # # 默认的交换类型是topic
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # # 默认的路由键是task.default，这个路由键符合上面的default队列
    # CELERY_DEFAULT_ROUTING_KEY = 'task.default'
    #
    # CELERY_ROUTES = {
    #     # tasks.add的消息会进入web_tasks队列
    #     'app.tasks.add': {
    #         'queue': 'web_tasks',
    #         'routing_key': 'web.add'
    #     }
    # }

    # 是否启用应用
    APP_ENABLE = True
    # 应用前缀
    APP_URL_PREFIX = "/app"
    # 是否启用接口
    API_ENABLE = True
    # 接口前缀
    API_URL_PREFIX = "/api"

    # 分页参数
    PER_PAGE_NUM = 10

    # 设置数据库中字符串编码格式（针对mysql数据库）
    SQLALCHEMY_DATABASE_CHAR_CODE = u'utf8_general_ci'

    # 设置用户操作日志开关
    SERVICE_LOG_ENABLED = False

    # 向外发送回调请求时的UA标识
    WHO_AM_I = 'ghost_sa'

    # 是否开启寻找失踪孩子公益页面
    IS_OPEN_SEARCH_CHILDREN = True
    SEARCH_CHILDREN_KEYWORD = '你的请求不合法哟。有兴趣的话，点击查看源码哟'
    SEARCH_CHILDREN_URL = 'https://github.com/white-shiro-bai/ghost_sa/'

    # 获取ip的位置信息
    # 这个文件在去这里下载对应的mmdb文件 https://dev.maxmind.com/geoip/geoip2/geolite2/
    GEO_LITE2CITY_FILE = 'app/resources/GeoLite2-City.mmdb'
    GEO_LITE2ASN_FILE = 'app/resources/GeoLite2-ASN.mmdb'

    # ip透传
    # user_ip_key字段优先作为用户ip。当检测到埋点里有 user_ip字段时，优先使用。使后端的埋点ip显示为用户ip，而非服务器ip。
    USER_IP_FIRST = True
    # 后端上报埋点时传递ip用的key。
    USER_IP_KEY = '$ip'

    # 是否使用Kafka
    # True时，数据写入kafka, 反之，直接插入数据库
    USE_KAFKA = False

    # 开启登录控制查询，当状态为False时，统一返回通过状态
    ACCESS_CONTROL_QUERY = True

    # cdn_mode的数据进入后的处理方式。 可选值none、event、device
    # 'none'为直接抛掉不写入数据库，但不影响接入控制工作，主要是减少数据库数据量。
    # 'event'模式为只插入event表，不插入device表，这样会保留所有的cdn_mode的请求记录，没有update动作，所以性能不受影响。
    # 'device' 则跟普通埋点一样进库。
    ACCESS_CONTROL_CDN_MODE_WRITE = 'event'
    # 黑名单生效时间，
    # 0为只有当前时间生效，
    # 1-23小时数为向前封禁的时间，如2时，则除当前小时生效外，向前2小时内的黑名单也生效。最大不超过23
    ACCESS_CONTROL_QUERY_HOUR = 1
    # 单位byte。默认是100000000(1G)。控制模块缓存最大允许使用的内存，达量即写入access_control表
    ACCESS_CONTROL_MAX_MEMORY = 100000000
    # 查询内存使用量的间隔，默认是30秒。间隔越小，越精准，但是每次查询需要浪费1秒时间。间隔越大，越容易控制不住爆内存。该值续小于access_control_max_window，否则没意义。
    ACCESS_CONTROL_MAX_MEMORY_GAP = 30
    # 单位是秒。默认是300(5分钟)。如果一直没触发内存上限，则每10分钟写一次access_control表
    ACCESS_CONTROL_MAX_WINDOW = 300
    # 辅助key。
    # 默认是coupon_id，即除了distinct_id,ip之外，另一个独立用来判断数量的key。该key也需要埋点，
    # 如果为空，即''的时候，则不提取辅助key。
    ACCESS_CONTROL_ADD_ON_KEY = 'coupon_id'
    # 默认是500，分片时间内，所有埋点的触发阈值和。
    ACCESS_CONTROL_SUM_COUNT = 500
    # 默认是100，分片时间内，如果没有在properties表里查到进入接入控制清单的数量，也没在project_list表里查到该项目的缺省值，则使用全局缺省数量
    ACCESS_CONTROL_EVENT_DEFAULT = 100
    # 记录所有的查询结果，
    # 如果该值为False，则只记录返回命中的记录（普通模式，记录命中的。CDN模式，记录不通过的）。
    # 该值为True时，记录所有的查询结果。
    # 不论True还是False。数据返回格式按照模式指定的返回，不会强制使用CDN模式。该记录通常用来处理用户投诉和核算节约费用，放行的记录没太大意义，还浪费资源。
    ACCESS_CONTROL_FORCE_RESULT_RECORD = False
    # 该记录值为True时，无论是否采用CDN模式的查询，都会在进一份CDN埋点进CDN事件。意义是无论什么接口进数据，都会对CDN查询造成影响，进一步限制CDN消费。
    # 当该记录值为False时，只有CDN模式的请求，会被记录到埋点，其他的请求，埋点由请求端上报，以获得更正确更清晰的数据。\
    ACCESS_CONTROL_FORCE_CDN_RECORD = False
    # CDN模式是否查验distinct_id。
    ACCESS_CONTROL_CDN_MODE_DISTINCT_ID_CHECK = True
    # CDN模式是否查验distinct_id与token的匹配度。默认关。
    ACCESS_CONTROL_CDN_MODE_DISTINCT_ID_TOKEN_CHECK = True
    # CDN模式是否参考其他event作为封禁依据。当False时，CDN模式只核对event是cdn_mode的事件。
    ACCESS_CONTROL_CDN_MODE_MEGA_MATCH = False
    # ip触发进入黑名单的量是distinct_id的阈值的倍数
    ACCESS_CONTROL_DISTINCT_ID_PER_IP = 4
    # ip组触发进入黑名单的量是ip的阈值的倍数
    ACCESS_CONTROL_IP_PER_IP_GROUP = 3

    USE_PROPERTIES = False  # True时，会插入properties表，这个表不是必须的，只是方便提取数据时快速找到埋点里包含的变量。
    USE_USER = False  # True时，会插入properties表，这个表不是必须的，只是方便提取数据时快速找到埋点里包含的变量。

    # Kafka服务器的地址
    BOOTSTRAP_SERVERS = ['172.18.5.17:9092', '172.18.5.15:9092', '172.18.5.16:9092']

    # Kafka群组地址，同一群组共享一个Offset，不会重复，也不会漏。
    CLIENT_GROUP_ID = 'your_group_id_here'
    # Kafka的Topic
    KAFKA_TOPIC = 'events-tracking_test_cero'
    CLIENT_ID = 'get_message_from_kafka'
    # latest,earliest,none
    KAFKA_OFFSET_RESET = 'latest'

    # 日志是否输出到ELK
    LOG2ELK = False
    ELK_HOST = '172.18.3.110'
    ELK_PORT = 23037

    # 默认情况下Flask使用ascii编码来序列化对象。如果这个值被设置为False ， Flask不会将其编码为ASCII，并且按原样输出，返回它的unicode字符串。
    # 比如jsonfiy会自动地采用utf-8来编码它然后才进行传输。
    JSON_AS_ASCII = False
