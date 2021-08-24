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

    # access token配置
    CLIENT_NAME = 'test'
    CLIENT_ID = '395b6cd1-64db-4de4-973b-a968288b3204'
    CLIENT_SECRET = '45a113ac-c7f2-30b0-90a5-a399ab912716'

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
