# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    业务逻辑模块
"""
from app.component.url_tools import get_post_datas
from app.configs.code import ResponseCode
from app.flaskr.sa.vo import RequestData
from app.utils.geo import get_address, get_asn
from app.utils.kafka_op import insert_message_to_kafka
from app.flaskr.sa.dao import insert_event, insert_or_update_device, insert_properties, insert_user
from app.utils.response import res, default_return_img

try:
    import simplejson as json
except ImportError:
    import json
import time

from flask import current_app, request, Response


def get_data():
    remark = request.args.get('remark', None)
    project = request.args.get('project', None)

    # 不合法情况，直接过滤，避免造成后续处理负担
    if not remark or not project:
        return res(code=ResponseCode.SYSTEM_ERROR, msg='project或remark为空，此2项参数必填!')

    # eg: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100
    # Safari/537.36
    user_agent = request.headers.get('User-Agent', '')
    if len(user_agent) > 2048:
        return res(code=ResponseCode.SYSTEM_ERROR, msg='User-Agent参数不合法!')

    # 若是爬虫，则将remark置成爬虫标识
    user_agent_lower = user_agent.lower()
    if user_agent_lower and any([pt in user_agent_lower for pt in ['spider', 'googlebot', 'adsbot-google']]):
        remark = 'spider'

    # eg: 10.16.5.241:5000
    host = request.headers.get('Host', '')
    # eg: keep-alive
    connection = request.headers.get('Connection', '')
    # eg: no-cache
    pragma = request.headers.get('Pragma', '')
    # no-cache
    cache_control = request.headers.get('Cache-Control', '')
    # image/webp,image/apng,image/*,*/*;q=0.8
    accept = request.headers.get('Accept', '')
    if len(accept) > 255:
        return res(code=ResponseCode.SYSTEM_ERROR, msg='Accept参数不合法!')

    # image/webp,image/apng,image/*,*/*;q=0.8
    accept_encoding = request.headers.get('Accept-Encoding', '')
    if len(accept_encoding) > 255:
        return res(code=ResponseCode.SYSTEM_ERROR, msg='Accept-Encoding参数不合法!')

    #: zh-CN,zh;q=0.9
    accept_language = request.headers.get('Accept-Language', '')
    if len(accept_language) > 255:
        return res(code=ResponseCode.SYSTEM_ERROR, msg='Accept-Language参数不合法!')

    # 客户端操作系统
    ua_platform = request.user_agent.platform
    # 客户端的浏览器
    ua_browser = request.user_agent.browser
    # 客户端浏览器的版本
    ua_version = request.user_agent.version
    # 客户端浏览器的语言
    ua_language = request.user_agent.language

    ext = request.args.get('ext')
    url = request.url
    # 获取SLB真实地址
    ip = request.headers.get('X-Forwarded-For')
    if not ip:
        # 服务器直接暴露
        ip = request.remote_addr

    # 只获取第一条IP为ip_city信息，其它忽略
    first_ip = ip.split(', ')[0]
    ip_city, ip_is_good = get_address(first_ip)
    ip_asn, ip_asn_is_good = get_asn(first_ip)
    #: zh-CN,zh;q=0.9
    referrer = request.headers.get('Referer', '')
    datas = get_post_datas()
    request_data = RequestData(project=project, remark=remark)

    # ip透传
    # user_ip_key字段优先作为用户ip。当检测到埋点里有 user_ip字段时，优先使用。使后端的埋点ip显示为用户ip，而非服务器ip。
    for data in datas:
        if current_app.config['USER_IP_FIRST']:
            if 'properties' in data \
                    and current_app.config['USER_IP_KEY'] in data.get('properties', {}) \
                    and data.get('properties', {}).get(current_app.config['USER_IP_KEY']):
                user_ip = data.get('properties', {}).get(current_app.config['USER_IP_KEY'])
                # 若存在$IP，则取其中第一个
                if user_ip:
                    user_ip = user_ip.split(', ')[0]
                # user_ip为ipv4，则中间.为3个字符，若存在多个ip，则
                if len(user_ip) - len(user_ip.replace('.', '')) == 3:
                    ip = user_ip
                    ip_city, ip_is_good = get_address(user_ip)
                    ip_asn, ip_asn_is_good = get_asn(user_ip)
        request_data.data = data
        request_data.set_connect_properties(connection, pragma, cache_control, accept, accept_encoding, accept_language=accept_language)
        request_data.set_url_properties(host, url, referrer=referrer)
        request_data.set_ua_properties(user_agent, ua_platform, ua_browser, ua_version, ua_language)
        request_data.set_ip_properties(ip, ip_city, ip_asn, ip_is_good, ip_asn_is_good)

        insert_data(request_data)
    return Response(default_return_img, mimetype="image/gif")


def insert_data(request_data):
    """保存数据.
    """
    start_time = time.time()

    data_decode = request_data.data
    json_data_str = json.dumps(data_decode, ensure_ascii=False)
    track_id = data_decode.get('_track_id', 0)

    distinct_id = data_decode.get('distinct_id', '')
    event = data_decode.get('event', '')
    # event类型
    type_ = data_decode.get('type')

    lib = data_decode.get('lib', {}).get('$lib')
    if not lib:
        lib = data_decode.get('properties', {}).get('$lib')
    request_data.set_common_properties(track_id=track_id, distinct_id=distinct_id, event=event, lib=lib, type_=type_)

    access_control_cdn_mode_write = current_app.config['ACCESS_CONTROL_CDN_MODE_WRITE']
    if not current_app.config['USE_KAFKA']:
        if event not in ('cdn_mode', 'cdn_mode2') or access_control_cdn_mode_write in ('event', 'device'):
            count = insert_event(request_data)

        if event not in ('cdn_mode', 'cdn_mode2') and access_control_cdn_mode_write == 'device':
            count = insert_or_update_device(request_data)

        use_properties = current_app.config['USE_PROPERTIES']
        if event not in ('', 'cdn_mode', 'cdn_mode2') and use_properties:
            insert_properties(request_data)

        use_user = current_app.config['USE_USER']
        if type_ in ('profile_set', 'track_signup', 'profile_set_once') and use_user:
            insert_user(request_data)

        # TODO 改造后续代码
        # if event == admin.aso_dsp_callback_event:
        #     ids = []
        #     if "anonymous_id" in data_decode and data_decode["anonymous_id"] not in ids:
        #         ids.append(data_decode["anonymous_id"])
        #     if "$device_id" in data_decode["properties"] and data_decode["properties"]["$device_id"] not in ids:
        #         ids.append(data_decode["properties"]["$device_id"])
        #     if "imei" in data_decode["properties"] and data_decode["properties"]["imei"] not in ids:
        #         ids.append(data_decode["properties"]["imei"])
        #     if "idfa" in data_decode["properties"] and data_decode["properties"]["idfa"] not in ids:
        #         ids.append(data_decode["properties"]["idfa"])
        #     for did in ids:
        #         insert_device_count = return_dsp_utm(project=project,distinct_id=distinct_id,device_id=did,created_at=created_at)
        #         print('更新地址来源',insert_device_count)
        #     if admin.aso_dsp_callback == True:
        #         if data_decode['properties']['$is_first_day'] is True or admin.aso_dsp_callback_history is True:
        #             for did in ids:
        #                 dsp_count = recall_dsp(project=project,device_id=did,created_at=created_at,ids=ids)
        #                 print('回调DSP',dsp_count)
        # if admin.independent_listener == False:
        #     tr = trigger(project=project, data_decode=data_decode)
        #     tr.play_all()
        # if admin.access_control_commit_mode =='none_kafka':
        #     ac_none_kafka.traffic(project=project,event=event,ip_commit=ip,distinct_id_commit=distinct_id,add_on_key_commit=data_decode['properties'][admin.access_control_add_on_key] if admin.access_control_add_on_key in data_decode['properties'] else None)
    else:
        msg = request_data.to_kafka_msg()
        insert_message_to_kafka(msg=msg, key=distinct_id)

    cost_millisecond_time = time.time() - start_time
    current_app.logger.info(f'耗时{cost_millisecond_time}毫秒')

