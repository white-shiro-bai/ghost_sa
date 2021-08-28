# -*- coding: utf-8 -*-
"""
    xiaowei.song 2016-7-7

    返回关键字和返回代码
"""


class ResponseKey(object):
    """返回关键字."""
    STATUS = "code"
    MESSAGE = "msg"
    LEVEL = "level"


class ResponseCode(object):
    """返回代码"""
    # 数据库异常错误代码
    FLASK_SQLALCHEMY_EXCEPT = 3306

    # 异常请求错误代码
    URL_NOT_FOUND = 404             # 该请求不存在
    BAD_REQUEST = 400               # 错误的请求，请求格式不规范，不符合API要求
    METHOD_NOT_ALLOWED = 405        # 请求的方式错误
    CSRF_TOKEN_MISSING = 40000      # CSRF token missing or incorrect

    # 全局错误代码块
    SUCCEED = 0                     # 成功
    ERROR = 1                       # 失败
    VALIDATE_FAIL = 10002           # 数据校验失败
    GET_BY_PARAM_ERROR = 10003      # 根据参数获取结果失败，数据不存在
    SYSTEM_ERROR = 500


class ResponseLevel(object):
    """
    xiaowei.song 2016-7-7

    定义错误等级
    """
    INFO = "info"
    DANGER = "danger"
