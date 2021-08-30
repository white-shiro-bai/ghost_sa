# -*- coding: utf-8 -*-
"""自定义通用返回数据格式"""
from flask import render_template, current_app
from flask.json import jsonify

from app.configs.code import ResponseCode

from app.utils.database import CRUDMixin, model_to_dict


def translate2succeed(msg):
    """
        xiaowei.song 2017-3-6

        转换程序中一些特殊返回消息，定制成统一的SUCCEED
    """
    if msg and (not isinstance(msg, str) or msg.lower() not in ("success", "succeed")):
        return msg
    return u"成功"


def res(code=ResponseCode.SUCCEED, msg=u"成功", level=None, data=None):
    """
    封装的通用返回方法

    :param code: http，返回代码，默认为 200成功
    :param msg: 返回消息，默认为'成功'
    :param level:   api请求消息等级，默认为None
    :param data:    返回的数据列表，必须是可以iterator，比如dict,list,tuple都可以
    :return json:   返回json对象
    """
    result = {"status": str(code), "message": translate2succeed(msg)}
    if code != ResponseCode.SUCCEED and (msg == u"成功" or msg is None):
        result.pop("message")
    if level:
        result['level'] = level

    if data or isinstance(data, int):
        result['data'] = data

    # 兼容ghost_sa 返回html页面
    if current_app.config['IS_OPEN_SEARCH_CHILDREN'] and code == ResponseCode.URL_NOT_FOUND:
        return render_template(f'{code}.html'), code

    current_app.logger.debug(f'返回结果为: {result}')
    return jsonify(result)


def res_page(args, data=None, total_count=0):
    """
    xiaowei.song 2016-6-28

    添加分页返回方法

    :param args: 分页相关参数
    :param data: 查询出来的list数据
    :param total_count: 总记录数
    :return json: json格式对象
    """
    result = {"status": ResponseCode.SUCCEED,
              'page': {"current_page": args["page"],
                       "total_page": 0,
                       "per_page": args["per_page"],
                       "total_count": total_count}}
    # 分页相关参数
    total_page = total_count // args["per_page"]
    if total_count % args["per_page"]:
        total_page += 1
    result["page"]["total_page"] = total_page

    if isinstance(data, list):
        if len(data):
            result['data'] = data
            if isinstance(data[0], CRUDMixin):
                result['data'] = map(lambda v: model_to_dict(v), data)
        else:
            result['page'] = {"current_page": 0, "total_page": 0, "per_page": 0,
                              "total_count": 0}
            result['data'] = None
    else:
        result['data'] = data
    return jsonify(result)
