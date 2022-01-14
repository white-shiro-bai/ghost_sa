# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)

from flask import request,jsonify,Response,redirect
import traceback
import time
import urllib.parse
import base64
import json
import pprint
import os
from component.db_func import insert_event,get_long_url_from_short, insert_noti_temple,insert_shortcut_history,check_long_url,insert_shortcut,show_shortcut,count_shortcut,show_check,insert_properties,insert_user_db,show_project,read_mobile_ad_list,count_mobile_ad_list,read_mobile_ad_src_list,check_mobile_ad_url,insert_mobile_ad_list,distinct_id_query,insert_shortcut_read,query_access_control,query_access_control_exclude,get_access_control_event,get_access_control_detail,get_access_control_detail_count,update_access_control,get_status_codes
from geoip.geo import get_addr,get_asn
import gzip
from component.api_tools import insert_device,encode_urlutm,insert_user,recall_dsp,return_dsp_utm,gen_token,tag_name,user_info
from configs.export import write_to_log
from component.shorturl import get_suoim_short_url
from configs import admin
import time
if admin.use_kafka is True:
    from component.kafka_op import insert_message_to_kafka
import re
from trigger import trigger
from component.qrcode import gen_qrcode
from component.url_tools import get_url_params
import hashlib
if admin.access_control_commit_mode =='none_kafka':
    from component.access_control import access_control
    ac_none_kafka = access_control()


def insert_data(project,data_decode,User_Agent,Host,Connection,Pragma,Cache_Control,Accept,Accept_Encoding,Accept_Language,ip,ip_city,ip_asn,url,referrer,remark,ua_platform,ua_browser,ua_version,ua_language,ip_is_good,ip_asn_is_good,created_at=None,updated_at=None,use_kafka=admin.use_kafka):
    start_time = time.time()
    jsondump = json.dumps(data_decode,ensure_ascii=False)
    if '_track_id' in data_decode:
        track_id = data_decode['_track_id']
    else:
        track_id = 0
    distinct_id = data_decode['distinct_id']
    if 'event' in data_decode:
        event = data_decode['event']
    else:
        event = None
    if remark :
        remark = remark
    else:
        remark = ''
    type_1 = data_decode['type'] if 'type' in data_decode else None
    # lib = data_decode['lib']['$lib'] if '$lib' in data_decode['lib'] else None
    lib = None
    if 'lib' in data_decode:
        if '$lib' in data_decode['lib']:
            lib = data_decode['lib']['$lib']
    if lib is None and 'properties' in data_decode:
        if '$lib' in data_decode['properties']:
            lib = data_decode['properties']['$lib']
    # else:
    #     lib = None
    if use_kafka is False:
        try:
            if event != 'cdn_mode' or event != 'cdn_mode2' or admin.access_control_cdn_mode_write == 'event' or admin.access_control_cdn_mode_write == 'device' :
                count = insert_event(table=project,alljson=jsondump,track_id=track_id,distinct_id=distinct_id,lib=lib,event=event,type_1=type_1,User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=created_at)
            if event != 'cdn_mode' or event != 'cdn_mode2' or admin.access_control_cdn_mode_write == 'device':
                insert_device(project=project,data_decode=data_decode,user_agent=User_Agent,accept_language=Accept_Language,ip=ip,ip_city=ip_city,ip_is_good=ip_is_good,ip_asn=ip_asn,ip_asn_is_good=ip_asn_is_good,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=created_at)
            properties_key = []
            for keys in data_decode['properties'].keys():
                properties_key.append(keys)
            if event and admin.use_properties is True and event != 'cdn_mode' and event != 'cdn_mode2':
                insert_properties(project=project,lib=lib,remark=remark,event=event,properties=json.dumps(properties_key),properties_len=len(data_decode['properties'].keys()),created_at=created_at,updated_at=updated_at)
            if type_1 == 'profile_set' or type_1 == 'track_signup' or type_1 =='profile_set_once':
                insert_user(project=project,data_decode=data_decode,created_at=created_at)
            if event == admin.aso_dsp_callback_event:
                ids = []
                if "anonymous_id" in data_decode and data_decode["anonymous_id"] not in ids:
                    ids.append(data_decode["anonymous_id"])
                if "$device_id" in data_decode["properties"] and data_decode["properties"]["$device_id"] not in ids:
                    ids.append(data_decode["properties"]["$device_id"])
                if "imei" in data_decode["properties"] and data_decode["properties"]["imei"] not in ids:
                    ids.append(data_decode["properties"]["imei"])
                if "idfa" in data_decode["properties"] and data_decode["properties"]["idfa"] not in ids:
                    ids.append(data_decode["properties"]["idfa"])
                for did in ids:
                    insert_device_count = return_dsp_utm(project=project,distinct_id=distinct_id,device_id=did,created_at=created_at)
                    print('更新地址来源',insert_device_count)
                if admin.aso_dsp_callback == True:
                    if data_decode['properties']['$is_first_day'] is True or admin.aso_dsp_callback_history is True:
                        for did in ids:
                            dsp_count = recall_dsp(project=project,device_id=did,created_at=created_at,ids=ids)
                            print('回调DSP',dsp_count)
            if admin.independent_listener == False:
                tr = trigger(project=project,data_decode=data_decode)
                tr.play_all()
            if admin.access_control_commit_mode =='none_kafka':
                ac_none_kafka.traffic(project=project,event=event,ip_commit=ip,distinct_id_commit=distinct_id,add_on_key_commit=data_decode['properties'][admin.access_control_add_on_key] if admin.access_control_add_on_key in data_decode['properties'] else None)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api',defname='insert_data',result=error)
    elif use_kafka is True:
        timenow = int(time.time())
        timenow13 = int(round(time.time() * 1000))
        msg = {"group":"event_track","timestamp":timenow13,"data":{"project":project,"data_decode":data_decode,"User_Agent":User_Agent,"Host":Host,"Connection":Connection,"Pragma":Pragma,"Cache_Control":Cache_Control,"Accept":Accept,"Accept_Encoding":Accept_Encoding,"Accept_Language":Accept_Language,"ip":ip,"ip_city":ip_city,"ip_asn":ip_asn,"url":url,"referrer":referrer,"remark":remark,"ua_platform":ua_platform,"ua_browser":ua_browser,"ua_version":ua_version,"ua_language":ua_language,"ip_is_good":ip_is_good,"ip_asn_is_good":ip_asn_is_good,"created_at":timenow,"updated_at":timenow}}
        insert_message_to_kafka(key=distinct_id ,msg=msg)
    print(time.time()-start_time)

def get_data():
    bitimage1 = os.path.join('image','43byte.gif')
    with open(bitimage1, 'rb') as f:
        returnimage = f.read()
    remark = request.args.get('remark') if 'remark' in request.args else 'normal'
    project = request.args.get('project')
    if project:
        User_Agent = request.headers.get('User-Agent')[0:2047] if request.headers.get('User-Agent') else None#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
        if User_Agent and User_Agent !='' and ('spider' in User_Agent.lower() or 'googlebot' in User_Agent.lower() or 'adsbot-google' in User_Agent.lower() ):
            remark = 'spider'
        Host = request.headers.get('Host') #: 10.16.5.241:5000
        Connection = request.headers.get('Connection')#: keep-alive
        Pragma = request.headers.get('Pragma')#: no-cache
        Cache_Control = request.headers.get('Cache-Control')#: no-cache
        Accept = request.headers.get('Accept')[0:254] if request.headers.get('Accept') else None#: image/webp,image/apng,image/*,*/*;q=0.8
        Accept_Encoding = request.headers.get('Accept-Encoding')[0:254] if request.headers.get('Accept-Encoding') else None#: gzip, deflate
        Accept_Language = request.headers.get('Accept-Language')[0:254] if request.headers.get('Accept-Language') else None#: zh-CN,zh;q=0.9
        ua_platform = request.user_agent.platform #客户端操作系统
        ua_browser = request.user_agent.browser #客户端的浏览器
        ua_version = request.user_agent.version #客户端浏览器的版本
        ua_language = request.user_agent.language #客户端浏览器的语言
        ext = request.args.get('ext')
        url = request.url
        # ip = '124.115.214.179' #测试西安bug
        # ip = '36.5.99.68' #测试安徽bug
        if request.headers.get('X-Forwarded-For') is None:
            ip = request.remote_addr#服务器直接暴露
        else:
            ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
        ip_city,ip_is_good = get_addr(ip)
        ip_asn,ip_asn_is_good = get_asn(ip)
        referrer = request.referrer[0:2047] if request.referrer else None
        pending_data_list_all = []
        # data_list_all.append( get_url_params('data') )
        if get_url_params('data'):
            de64 = base64.b64decode(urllib.parse.unquote(get_url_params('data')).encode('utf-8'))
            try:
                pending_data_list_all.append(json.loads(gzip.decompress(de64)))
            except:
                pending_data_list_all.append(json.loads(de64))
        if get_url_params('data_list'):
            de64_list = base64.b64decode(urllib.parse.unquote(get_url_params('data_list')).encode('utf-8'))
            try:
                data_decodes = json.loads(gzip.decompress(de64_list))
            except:
                data_decodes = json.loads(de64_list)
            for data_decode in data_decodes:
                pending_data_list_all.append(data_decode)
        for pending_data in pending_data_list_all:
            if admin.user_ip_first is True:
                if 'properties' in pending_data and admin.user_ip_key in pending_data['properties'] and pending_data['properties'][admin.user_ip_key]:
                    user_ip = pending_data['properties'][admin.user_ip_key]
                    if len(user_ip) - len(user_ip.replace('.','')) == 3:
                        ip = user_ip
                        ip_city,ip_is_good = get_addr(user_ip)
                        ip_asn,ip_asn_is_good = get_asn(user_ip)
            insert_data(project=project,data_decode=pending_data,User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good)
    return Response(returnimage, mimetype="image/gif")

def get_datas():
    try:
        return get_data()
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='api',defname='get_datas',result=error)
        return error

def get_long(short_url):
    time1 = int(time.time()*1000)
    long_url,status = get_long_url_from_short(short_url=short_url)
    User_Agent = request.headers.get('User-Agent') 
    Accept_Language = request.headers.get('Accept-Language')#: zh-CN,zh;q=0.9
    ua_platform = request.user_agent.platform #客户端操作系统
    ua_browser = request.user_agent.browser #客户端的浏览器
    ua_version = request.user_agent.version #客户端浏览器的版本
    ua_language = request.user_agent.language #客户端浏览器的语言
    url = request.url
    ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    if request.headers.get('X-Forwarded-For') is None:
        ip = request.remote_addr                            #服务器直接暴露
    time2 = int(time.time()*1000) - time1
    if admin.use_kafka is False:
        insert_shortcut_history(short_url=short_url,result=status,cost_time=time2,ip=ip,user_agent=User_Agent,accept_language=Accept_Language,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=time1/1000)
    elif admin.use_kafka is True:
        msg = {"group":"shortcut_history","data":{"short_url":short_url,"status":status,"time2":time2,"ip":ip,"user_agent":User_Agent,"accept_language":Accept_Language,"ua_platform":ua_platform,"ua_browser":ua_browser,"ua_version":ua_version,"ua_language":ua_language,"created_at":time1/1000}}
        insert_message_to_kafka(key=ip, msg=msg)
    if status == 'success':
        return redirect(long_url.replace(' ',''))
    elif status == 'expired':
        return '您查询的地址已过期'
    elif status == 'fail':
        return '您查询的解析不存在'

def shortit():
    if 'org_url' in request.form:
        org_url = request.form.get('org_url').replace(' ','')
        expired_at = int(time.mktime(time.strptime(request.form.get('expired_at','2038-01-19'), "%Y-%m-%d")))
        project = request.form.get('project',None)
        src = request.form.get('src','suoim')
        submitter = request.form.get('submitter',None)
        utm_source = request.form.get('utm_source',None)
        utm_medium = request.form.get('utm_medium',None)
        utm_campaign = request.form.get('utm_campaign',None)
        utm_content = request.form.get('utm_content',None)
        utm_term = request.form.get('utm_term',None)
        url_addon = encode_urlutm(utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term)
        if '?' in org_url:
            longurl = org_url+'&'+url_addon
        else:
            longurl = org_url+'?'+url_addon
        urllist,urlstatus = check_long_url(long_url=longurl)
        if urlstatus == 'exist':
            returnjson = {'result':urlstatus,'urllist':urllist}
            return jsonify(returnjson)
        else:
            check_short_status = 'success'
            while check_short_status == 'success':
                if src =='suoim':
                    src_short_url,status = get_suoim_short_url(long_url=longurl)
                else:
                    return jsonify({'result':'error','urllist':'src:'+src+'不存在'})
                if status == 'ok':
                    check_short_result,check_short_status = get_long_url_from_short(src_short_url)
                    if check_short_status == 'success':
                        continue
                    break
            short_url = src_short_url.split('/')[-1]
            insert_count = insert_shortcut(project=project,short_url=short_url,long_url=longurl,expired_at=expired_at,src=src,src_short_url=src_short_url,submitter=submitter,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term)
            print('已插入短连接解析地址'+str(insert_count))
            urllist,urlstatus = check_long_url(long_url=longurl)
            returnjson = {'result':'created_success','urllist':urllist}
            return jsonify(returnjson)
    else:
        returnjson = {'result':'error','error':'参数不全'}
        return jsonify(returnjson)

def show_short_cut_list():
    page = int(request.args.get('page')) if 'page' in request.args else 1
    length = int(request.args.get('length')) if 'length' in request.args else 50
    sort = '`shortcut`.created_at'
    if 'sort' in request.args:
        sort_org = request.args.get('sort')
        sort = '`shortcut`.'+sort_org
        if sort_org in ['visit_times','read_times']:
            sort = sort_org
    way = request.args.get('way') if 'way' in request.args else 'desc'
    add_on_parames = []
    if 'create_date_start' in request.args:
        add_on_parames.append('`shortcut`.created_at>={crstart}'.format(crstart=request.args.get('create_date_start')))
    if 'create_date_end' in request.args:
        add_on_parames.append('`shortcut`.created_at<={crend}'.format(crend=request.args.get('create_date_end')))
    if 'expired_date_start' in request.args:
        add_on_parames.append('`shortcut`.expired_at>={epstart}'.format(epstart=request.args.get('expired_date_start')))
    if 'expired_date_end' in request.args:
        add_on_parames.append('`shortcut`.expired_at<={epend}'.format(epend=request.args.get('expired_date_end')))
    if 'short_url' in request.args:
        add_on_parames.append('`shortcut`.short_url=\'{short_url}\''.format(short_url=request.args.get('short_url')))
    if 'long_url' in request.args:
        add_on_parames.append('`shortcut`.long_url like \'{long_url}%\''.format(long_url=request.args.get('long_url')))
    if 'utm_source' in request.args:
        add_on_parames.append('`shortcut`.utm_source like \'%{utm_source}%\''.format(utm_source=request.args.get('utm_source')))
    if 'utm_medium' in request.args:
        add_on_parames.append('`shortcut`.utm_medium like \'%{utm_medium}%\''.format(utm_medium=request.args.get('utm_medium')))
    if 'utm_campaign' in request.args:
        add_on_parames.append('`shortcut`.utm_campaign like \'%{utm_campaign}%\''.format(utm_campaign=request.args.get('utm_campaign')))
    if 'utm_content' in request.args:
        add_on_parames.append('`shortcut`.utm_content like \'%{utm_content}%\''.format(utm_content=request.args.get('utm_content')))
    if 'utm_term' in request.args:
        add_on_parames.append('`shortcut`.utm_term like \'%{utm_term}%\''.format(utm_term=request.args.get('utm_term')))
    if 'project' in request.args:
        add_on_parames.append('`shortcut`.project=\'{project}\''.format(project=request.args.get('project')))
    if 'submitter' in request.args:
        add_on_parames.append('`shortcut`.submitter=\'{submitter}\''.format(submitter=request.args.get('submitter')))
    if 'src' in request.args:
        add_on_parames.append('`shortcut`.src=\'{src}\''.format(src=request.args.get('src')))
    if 'src_short_url' in request.args:
        add_on_parames.append('`shortcut`.src_short_url=\'{src_short_url}\''.format(src_short_url=request.args.get('src_short_url')))
    if 'everywhere' in request.args:
        add_on_parames.append('concat(`shortcut`.project,`shortcut`.short_url,`shortcut`.long_url,`shortcut`.src,`shortcut`.src_short_url,`shortcut`.submitter,`shortcut`.utm_source,`shortcut`.utm_medium,`shortcut`.utm_campaign,`shortcut`.utm_content,`shortcut`.utm_term) like \'%{everywhere}%\''.format(everywhere=request.args.get('everywhere')))
    add_on_params=''
    if add_on_parames:
        add_on_params = " where " + " and ".join(add_on_parames)
    total_count = count_shortcut(filters=add_on_params)
    if total_count[0][0] > 0:
        result,count = show_shortcut(page=page,length=length,filters=add_on_params,sort=sort,way=way)
        if count >0:
            result_name = ['project','short_url','long_url','expired_at_str','created_at_str','src','src_short_url','submitter','utm_source','utm_medium','utm_campaign','utm_content','utm_term','created_at','expired_at','visit_times','read_times']
            return_data = []
            for item in result:
                zipped = dict(zip(result_name,item))
                return_data.append(zipped)
            returnjson = {'result':'success','sort':sort,'way':way,'count':count,'total_count':total_count[0][0],'page':page,'length':length,'data':return_data}
            return jsonify(returnjson)
        returnjson = {'result':'fail','error':'参数不正确'}
        return jsonify(returnjson)
    returnjson = {'result':'fail','error':'未找到对应的短链'}
    return jsonify(returnjson)

def ghost_check():
    start_time = time.time()
    password = request.form.get('password')
    project = request.form.get('project',None)
    if password == admin.admin_password and project:#只有正确的密码才能触发动作
        remark = request.form.get('remark',None)
        event = request.form.get('event',None)
        date = request.form.get('date',time.strftime("%Y-%m-%d", time.localtime()))
        hour = int(request.form.get('hour',time.strftime("%H", time.localtime())))
        order = request.form.get('order','desc')
        distinct_id = request.form.get('distinct_id',None)
        start = int(request.form.get('start','0'))
        limit = int(request.form.get('limit','10'))
        add_on_where = ''
        if distinct_id:
            add_on_where = add_on_where+' and distinct_id = \''+distinct_id+'\''
        if event:
            add_on_where = add_on_where+' and event = \''+event+'\''
        if remark:
            add_on_where = add_on_where+' and remark = \''+remark+'\''
        try:
            results,results_count= show_check(project=project,date=date,hour=hour,order=order,start=start,limit=limit,add_on_where=add_on_where)
            pending_result = []
            for item in results:
                row = {'distinct_id':item[0],'event':item[1],'type':item[2],'all_json':json.loads(item[3]),'host':item[4],'user_agent':item[5],'ip':item[6],'url':item[7],'remark':item[8],'created_at':item[9],}
                # pending_result.append(dict(zip(key,item)))
                pending_result.append(row)
            time_cost = time.time() - start_time
            returnjson = {'result':'success','order':order,'results_count':results_count,'timecost':time_cost,'data':pending_result}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api',defname='ghost_check',result=error)
    # return jsonify('少参数')        # return 


def installation_track():
    start_time = time.time()
    project = request.args.get('project')
    if project:
        User_Agent = request.headers.get('User-Agent') #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
        Host = request.headers.get('Host') #: 10.16.5.241:5000
        Connection = request.headers.get('Connection')#: keep-alive
        Pragma = request.headers.get('Pragma')#: no-cache
        Cache_Control = request.headers.get('Cache-Control')#: no-cache
        Accept = request.headers.get('Accept')[0:254] if request.headers.get('Accept') else None#: image/webp,image/apng,image/*,*/*;q=0.8
        Accept_Encoding = request.headers.get('Accept-Encoding')[0:254] if request.headers.get('Accept-Encoding') else None #: gzip, deflate
        remark = request.args.get('remark') if 'remark' in request.args else 'normal'
        Accept_Language = request.headers.get('Accept-Language')[0:254] if request.headers.get('Accept-Language') else None#: zh-CN,zh;q=0.9
        ua_platform = request.user_agent.platform #客户端操作系统
        ua_browser = request.user_agent.browser #客户端的浏览器
        ua_version = request.user_agent.version #客户端浏览器的版本
        ua_language = request.user_agent.language #客户端浏览器的语言
        ext = request.args.get('ext')
        url = request.url
        args = request.args.to_dict(request.args)
        data = {"properties":args}
        # ip = '124.115.214.179' #测试西安bug
        # ip = '36.5.99.68' #测试安徽bug
        if    'ip' in args and len(args['ip']) - len( args['ip'].replace('.','') ) == 3:#判断IP里是否存在IP地址
            ip = args['ip']
        elif request.headers.get('X-Forwarded-For') is not None:
            ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
        else:
            ip = request.remote_addr#服务器直接暴露
        ip_city,ip_is_good = get_addr(ip)
        ip_asn,ip_asn_is_good = get_asn(ip)
        if ip_is_good ==0:
            ip_city = '{}'
        if ip_asn_is_good ==0:
            ip_asn = '{}'
        referrer = request.referrer[0:2047] if request.referrer else None
        try:
            if 'properties' in data and 'is_offerwall' in    data['properties'] and data['properties']['is_offerwall']=='1':
                count_event,count_user,time_cost = insert_installation_track(project=project,data_decode=data,User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma, Cache_Control=Cache_Control, Accept=Accept, Accept_Encoding=Accept_Encoding, Accept_Language=Accept_Language, ip=ip, ip_city=ip_city,ip_asn=ip_asn, url=url, referrer=referrer, remark=remark, ua_platform=ua_platform, ua_browser=ua_browser, ua_version=ua_version, ua_language=ua_language, ip_is_good=ip_is_good, ip_asn_is_good=ip_asn_is_good)
                if count_event and count_event>0 or count_user and count_user>0:
                    code = 0 #有米标准
                    msg = "success" #有米标准
                    result = 1 #七麦标准
                    error = '成功' #七麦标准
                else:
                    code = -1 #有米标准
                    msg = 'failed' #有米标准
                    result = 0 #七麦标准
                    error = '没有记录插入' #七麦标准
                returnjson = {'count_event':count_event,'count_user':count_user,'timecost':round(time_cost,4),'code':code,'msg':msg,'args':args,'result':result,'error':error}
                return jsonify(returnjson)
            else:
                insert_installation_track(project=project,data_decode=data,User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma, Cache_Control=Cache_Control, Accept=Accept, Accept_Encoding=Accept_Encoding, Accept_Language=Accept_Language, ip=ip, ip_city=ip_city,ip_asn=ip_asn, url=url, referrer=referrer, remark=remark, ua_platform=ua_platform, ua_browser=ua_browser, ua_version=ua_version, ua_language=ua_language, ip_is_good=ip_is_good, ip_asn_is_good=ip_asn_is_good)
                bitimage1 = os.path.join('image','43byte.gif')
                with open(bitimage1, 'rb') as f:
                    returnimage = f.read()
                return Response(returnimage, mimetype="image/gif")
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api',defname='installation_track',result=error)
    else:
        bitimage1 = os.path.join('image','43byte.gif')
        with open(bitimage1, 'rb') as f:
            returnimage = f.read()
        return Response(returnimage, mimetype="image/gif")

def insert_installation_track(project, data_decode, User_Agent, Host, Connection, Pragma, Cache_Control, Accept, Accept_Encoding, Accept_Language, ip, ip_city,
                                        ip_asn, url, referrer, remark, ua_platform, ua_browser, ua_version, ua_language, ip_is_good, ip_asn_is_good, created_at=None, updated_at=None,use_kafka=admin.use_kafka):
    start_time = time.time()
    timenow13 = int(round(time.time() * 1000))
    distinct_id = 'undefined'
    track_id    = 0
    dist_id_name = ['IDFA','androidid','android_id','IMEI','Idfa','Imei','imei','idfa']
    distinct_id = 'undefined'
    for i in dist_id_name:
        if i in data_decode['properties'].keys() and data_decode['properties'][i] and data_decode['properties'][i]!='' and data_decode['properties'][i]!='undefined':
            distinct_id = data_decode['properties'][i]
    if 'ts' in    data_decode['properties']:
        track_id = re.sub("\D","",data_decode['properties']['ts'])
        if track_id == '':
            track_id    = 0
    if 'properties' in data_decode and 'is_offerwall' in    data_decode['properties'] and data_decode['properties']['is_offerwall']=='1':
        count_event = insert_event(table=project,alljson=json.dumps(data_decode),track_id=track_id,distinct_id=distinct_id,lib='ghost_sa',event='$AppChannelMatching',type_1='installation_track',User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=created_at if created_at else start_time)
        count_user = insert_user_db(project=project,distinct_id=distinct_id,lib='ghost_sa',map_id='',original_id='',user_id='',all_user_profile=json.dumps(data_decode),update_params='',created_at=created_at if created_at else start_time,updated_at=created_at if created_at else start_time)
        time_cost = time.time()-start_time
        if admin.use_properties is True:
            properties_key = []
            for keys in data_decode['properties'].keys():
                properties_key.append(keys)
            insert_properties(project=project,lib='ghost_sa',remark=remark,event='$AppChannelMatching',properties=json.dumps(properties_key),properties_len=len(data_decode['properties'].keys()),created_at=created_at if created_at else start_time,updated_at=created_at if created_at else start_time)
        return count_event,count_user,time_cost
    elif use_kafka is False:
        insert_event(table=project,alljson=json.dumps(data_decode),track_id=track_id,distinct_id=distinct_id,lib='ghost_sa',event='$AppChannelMatching',type_1='installation_track',User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=created_at if created_at else start_time)
        insert_user_db(project=project,distinct_id=distinct_id,lib='ghost_sa',map_id='',original_id='',user_id='',all_user_profile=json.dumps(data_decode),update_params='',created_at=created_at if created_at else start_time,updated_at=created_at if created_at else start_time)
        if admin.use_properties is True:
            properties_key = []
            for keys in data_decode['properties'].keys():
                properties_key.append(keys)
            insert_properties(project=project,lib='ghost_sa',remark=remark,event='$AppChannelMatching',properties=json.dumps(properties_key),properties_len=len(data_decode['properties'].keys()),created_at=created_at if created_at else start_time,updated_at=created_at if created_at else start_time)
        print(time.time()-start_time)
    elif use_kafka is True:
        msg = {"group":"installation_track","timestamp":timenow13,"data":{"project":project,"data_decode":data_decode,"User_Agent":User_Agent,"Host":Host,"Connection":Connection,"Pragma":Pragma,"Cache_Control":Cache_Control,"Accept":Accept,"Accept_Encoding":Accept_Encoding,"Accept_Language":Accept_Language,"ip":ip,"ip_city":ip_city,"ip_asn":ip_asn,"url":url,"referrer":referrer,"remark":remark,"ua_platform":ua_platform,"ua_browser":ua_browser,"ua_version":ua_version,"ua_language":ua_language,"ip_is_good":ip_is_good,"ip_asn_is_good":ip_asn_is_good,"created_at":created_at if created_at else start_time,"updated_at":created_at if created_at else start_time}}
        insert_message_to_kafka(key=distinct_id, msg=msg)
        print(time.time()-start_time)


def check_exist_distinct_id():
    start_time = time.time()
    password = request.args.get('password')
    project = request.args.get('project')
    distinct_id = request.args.get('distinct_id')
    query_from = request.args.get('query_from')

    User_Agent = request.headers.get('User-Agent')[0:2047] if request.headers.get('User-Agent') else None #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
    Host = request.headers.get('Host') #: 10.16.5.241:5000
    Connection = request.headers.get('Connection')#: keep-alive
    Pragma = request.headers.get('Pragma')#: no-cache
    Cache_Control = request.headers.get('Cache-Control')#: no-cache
    Accept = request.headers.get('Accept')[0:254] if request.headers.get('Accept') else None#: image/webp,image/apng,image/*,*/*;q=0.8
    Accept_Encoding = request.headers.get('Accept-Encoding')[0:254] if request.headers.get('Accept-Encoding') else None #: gzip, deflate
    remark = request.args.get('remark') if 'remark' in request.args else 'normal'
    Accept_Language = request.headers.get('Accept-Language')[0:254] if request.headers.get('Accept-Language') else None#: zh-CN,zh;q=0.9
    ua_platform = request.user_agent.platform #客户端操作系统
    ua_browser = request.user_agent.browser #客户端的浏览器
    ua_version = request.user_agent.version #客户端浏览器的版本
    ua_language = request.user_agent.language #客户端浏览器的语言
    ext = request.args.get('ext')
    url = request.url
    args = request.args.to_dict(request.args)
    data = {"properties":args}
    # ip = '124.115.214.179' #测试西安bug
    # ip = '36.5.99.68' #测试安徽bug
    if    'ip' in args and len(args['ip']) - len( args['ip'].replace('.','') ) == 3:#判断IP里是否存在IP地址
        ip = args['ip']
    elif request.headers.get('X-Forwarded-For') is not None:
        ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    else:
        ip = request.remote_addr#服务器直接暴露
    ip_city,ip_is_good = get_addr(ip)
    ip_asn,ip_asn_is_good = get_asn(ip)
    if ip_is_good ==0:
        ip_city = '{}'
    if ip_asn_is_good ==0:
        ip_asn = '{}'
    referrer = request.referrer[0:2047] if request.referrer else None

    if password == admin.admin_password and project and distinct_id and query_from:#只有正确的密码才能触发动作
        try:
            if ',' in distinct_id:
                #兼容七麦多个id一次性递入，返回格式兼容七麦
                distinct_id_list = distinct_id.split(',')
                returnjson = {'result':'success','results_count':len(distinct_id_list),'query_from':query_from}
                for distinct_id in distinct_id_list:
                    results_count= distinct_id_query(distinct_id=distinct_id,project=project)
                    returnjson[distinct_id] = results_count
                time_cost = time.time() - start_time
                returnjson['timecost'] = round(time_cost,4)
                data['returnjson'] = returnjson
                insert_event(table=project,alljson=json.dumps(data),track_id=0,distinct_id=query_from,lib='ghost_sa',event='check_exist',type_1='ghost_sa_func',User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=start_time)
                if admin.use_properties is True:
                    properties_key = []
                    for keys in data.keys():
                        properties_key.append(keys)
                    insert_properties(project=project,lib='ghost_sa',remark=remark,event='check_exist',properties=json.dumps(properties_key),properties_len=len(data.keys()),created_at=start_time,updated_at=start_time)
                return jsonify(returnjson)
            else:
                #正常一条一递，兼容有米和七麦的标准
                results_count= distinct_id_query(distinct_id=distinct_id,project=project)
                # key=['distinct_id','event','type','all_json','host','user_agent','ip','url','remark','created_at']
                if results_count== 0 :
                    row = {}
                    # pending_result.append(dict(zip(key,item)))
                    time_cost = time.time() - start_time
                    # returnjson = {'result':'success','results_count':results_count,'code':0,'msg':'not_exists'}
                    returnjson = {'result':'success','results_count':results_count,'timecost':round(time_cost,4),'code':0,'msg':'not_exists','query_from':query_from}
                    returnjson[distinct_id] = results_count
                    data['returnjson'] = returnjson
                    insert_event(table=project,alljson=json.dumps(data),track_id=0,distinct_id=query_from,lib='ghost_sa',event='check_exist',type_1='ghost_sa_func',User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=start_time)
                    if admin.use_properties is True:
                        properties_key = []
                        for keys in data.keys():
                            properties_key.append(keys)
                        insert_properties(project=project,lib='ghost_sa',remark=remark,event='check_exist',properties=json.dumps(properties_key),properties_len=len(data.keys()),created_at=start_time,updated_at=start_time)
                    return jsonify(returnjson)
                time_cost = time.time() - start_time
                returnjson = {'result':'success','results_count':results_count,'timecost':round(time_cost,4),'code':-1,'msg':'exists','query_from':query_from}
                returnjson[distinct_id] = results_count
                # returnjson = {'result':'success','results_count':results_count,'code':-1,'msg':'exists'}
                data['returnjson'] = returnjson
                insert_event(table=project,alljson=json.dumps(data),track_id=0,distinct_id=query_from,lib='ghost_sa',event='check_exist',type_1='ghost_sa_func',User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,created_at=start_time)
                if admin.use_properties is True:
                    properties_key = []
                    for keys in data.keys():
                        properties_key.append(keys)
                    insert_properties(project=project,lib='ghost_sa',remark=remark,event='check_exist',properties=json.dumps(properties_key),properties_len=len(data.keys()),created_at=start_time,updated_at=start_time)
                return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api',defname='check_exist_distinct_id',result=error)
    else:
        return jsonify('参数不正确')

def show_project_list():
    start_time = time.time()
    password = request.form.get('password')
    if password == admin.admin_password:#只有正确的密码才能触发动作
        try:
            results,results_count= show_project()
            # key=['distinct_id','event','type','all_json','host','user_agent','ip','url','remark','created_at']
            pending_result = []
            for item in results:
                row = {'project':item[0],'created_at':item[1],'expired_at':item[2],'enable_scheduler':item[3]}
                # pending_result.append(dict(zip(key,item)))
                pending_result.append(row)
            time_cost = time.time() - start_time
            returnjson = {'result':'success','results_count':results_count,'timecost':round(time_cost,4),'data':pending_result}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api',defname='show_project_list',result=error)


def show_mobile_ad_list():
    #默认跟踪参数的含义，见文档 https://github.com/white-shiro-bai/ghost_sa/blob/master/docs/admaster.md
    page = int(request.args.get('page')) if 'page' in request.args else 1
    length = int(request.args.get('length')) if 'length' in request.args else 50
    sort    = '`mobile_ad_list`.created_at'
    if 'sort' in request.args:
        sort_org = request.args.get('sort')
        sort = sort_org
    way = request.args.get('way') if 'way' in request.args else 'desc'
    add_on_parames = []
    if 'create_date_start' in request.args:
        # print('kk1')
        add_on_parames.append('mobile_ad_list.created_at>={crstart}'.format(crstart=request.args.get('create_date_start')))
        # print(add_on_params)
    if 'create_date_end' in request.args:
        add_on_parames.append('mobile_ad_list.created_at<={crend}'.format(crend=request.args.get('create_date_end')))
    if 'expired_date_start' in request.args:
        add_on_parames.append('mobile_ad_list.expired_at>={epstart}'.format(epstart=request.args.get('expired_date_start')))
    if 'expired_date_end' in request.args:
        add_on_parames.append('mobile_ad_list.expired_at<={epend}'.format(epend=request.args.get('expired_date_end')))
    if 'url' in request.args:
        add_on_parames.append('mobile_ad_list.url=\'{url}\''.format(url=request.args.get('url')))
    if 'src' in request.args:
        add_on_parames.append('mobile_ad_list.src like \'{src}%\''.format(src=request.args.get('src')))
    if 'src_name' in request.args:
        add_on_parames.append('mobile_ad_src.src_name like \'{src_name}%\''.format(src=request.args.get('src_name')))
    if 'utm_source' in request.args:
        add_on_parames.append('`mobile_ad_list`.utm_source like \'%{utm_source}%\''.format(utm_source=request.args.get('utm_source')))
    if 'utm_medium' in request.args:
        add_on_parames.append('`mobile_ad_list`.utm_medium like \'%{utm_medium}%\''.format(utm_medium=request.args.get('utm_medium')))
    if 'utm_campaign' in request.args:
        add_on_parames.append('`mobile_ad_list`.utm_campaign like \'%{utm_campaign}%\''.format(utm_campaign=request.args.get('utm_campaign')))
    if 'utm_content' in request.args:
        add_on_parames.append('`mobile_ad_list`.utm_content like \'%{utm_content}%\''.format(utm_content=request.args.get('utm_content')))
    if 'utm_term' in request.args:
        add_on_parames.append('`mobile_ad_list`.utm_term like \'%{utm_term}%\''.format(utm_term=request.args.get('utm_term')))
    if 'project' in request.args:
        add_on_parames.append('project=\'{project}\''.format(project=request.args.get('project')))
    if 'submitter' in request.args:
        add_on_parames.append('`mobile_ad_list`.submitter=\'{submitter}\''.format(submitter=request.args.get('submitter')))
    if 'everywhere' in request.args:
        add_on_parames.append('concat(`mobile_ad_list`.project,`mobile_ad_list`.src,`mobile_ad_list`.submitter,`mobile_ad_list`.utm_source,`mobile_ad_list`.utm_medium,`mobile_ad_list`.utm_campaign,`mobile_ad_list`.utm_content,`mobile_ad_list`.utm_term,`mobile_ad_src`.src_name) like \'%{everywhere}%\''.format(everywhere=request.args.get('everywhere')))
    add_on_params=''
    if add_on_parames:
        add_on_params = " where " + " and ".join(add_on_parames)
    total_count = count_mobile_ad_list(filters=add_on_params)
    if total_count[0][0] > 0:
        result,count = read_mobile_ad_list(page=page,length=length,filters=add_on_params,sort=sort,way=way)
        if count >0:
            result_name = ['project','url','src','src_name','src_url','submitter','utm_source','utm_medium','utm_campaign','utm_content','utm_term','created_at','expired_at']
            return_data = []
            for item in result:
                zipped = dict(zip(result_name,item))
                return_data.append(zipped)
            returnjson = {'result':'success','sort':sort,'way':way,'count':count,'total_count':total_count[0][0],'page':page,'length':length,'data':return_data}
            return jsonify(returnjson)
        returnjson = {'result':'fail','error':'参数不正确'}
        return jsonify(returnjson)
    returnjson = {'result':'fail','error':'未找到对应的检测链接'}
    return jsonify(returnjson)

def show_mobile_src_list():
    #默认跟踪参数的含义，见文档 https://github.com/white-shiro-bai/ghost_sa/blob/master/docs/admaster.md
    start_time = time.time()
    result,count = read_mobile_ad_src_list()
    if count > 0:
            result_name = ['src','src_name','src_args','created_at','updated_at','new_mark','utm_source','utm_medium','utm_campaign','utm_content','utm_term']
            return_data = []
            for item in result:
                zipped = dict(zip(result_name,item))
                return_data.append(zipped)
            time_cost = time.time() - start_time
            returnjson = {'result':'success','count':count,'data':return_data}
            return jsonify(returnjson)
    returnjson = {'result':'fail','error':'支持列表里无连接'}
    return jsonify(returnjson)

def create_mobile_ad_link():
    #默认跟踪参数的含义，见文档 https://github.com/white-shiro-bai/ghost_sa/blob/master/docs/admaster.md
    if 'src' in request.form and 'project' in request.form:
        src = request.form.get('src')
        expired_at = int(time.mktime(time.strptime(request.form.get('expired_at','2038-01-19'), "%Y-%m-%d"))) if 'expired_at' in request.form else 2147483647
        project = request.form.get('project',None)
        submitter = request.form.get('submitter',None)
        utm_source = request.form.get('utm_source',None)
        utm_medium = request.form.get('utm_medium',None)
        utm_campaign = request.form.get('utm_campaign',None)
        utm_content = request.form.get('utm_content',None)
        utm_term = request.form.get('utm_term',None)
        url_addon = encode_urlutm(utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term)
        result,count = read_mobile_ad_src_list(add_on_where="where `src`='"+src+"'")
        if count >0:
            src_args = result[0][2]
            url = '/cb/installation_track?'+src_args+'&project='+project+'&src='+src+'&'+url_addon
            urllist,urlstatus = check_mobile_ad_url(url=url)
            if urlstatus == 'exist':
                returnjson = {'result':urlstatus,'urllist':urllist}
                return jsonify(returnjson)
            else:
                if project:
                    insert_result,insert_count = insert_mobile_ad_list(project=project,url=url,src=src,src_url=src_args,submitter=submitter,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term,expired_at=expired_at)
                    if insert_count == 0 :
                        return jsonify({'result':'error','urllist':'url:'+url+'插入失败'})
                    else :
                        urllist,urlstatus = check_mobile_ad_url(url=url)
                        returnjson = {'result':'created_success','urllist':urllist}
                        return jsonify(returnjson)
                else:
                    returnjson = {'result':'error','error':'参数不全'}
                    return jsonify(returnjson)
        else:
            returnjson = {'result':'error','error':'暂不支持该源'}
            return jsonify(returnjson)
    else:
        returnjson = {'result':'error','error':'参数不全'}
        return jsonify(returnjson)

def who_am_i():
    ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    if request.headers.get('X-Forwarded-For') is None:
        ip = request.remote_addr                #服务器直接暴露

    ip_city,ip_is_good = get_addr(ip)
    ip_asn,ip_asn_is_good = get_asn(ip)
    if ip_is_good ==0:
        ip_city = '{}'
    if ip_asn_is_good ==0:
        ip_asn = '{}'
    User_Agent = request.headers.get('User-Agent')[0:2047] if request.headers.get('User-Agent') else None#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
    Host = request.headers.get('Host') #: 10.16.5.241:5000
    Connection = request.headers.get('Connection')#: keep-alive
    Pragma = request.headers.get('Pragma')#: no-cache
    Cache_Control = request.headers.get('Cache-Control')#: no-cache
    Accept = request.headers.get('Accept')[0:254] if request.headers.get('Accept') else None#: image/webp,image/apng,image/*,*/*;q=0.8
    Accept_Encoding = request.headers.get('Accept-Encoding')[0:254] if request.headers.get('Accept-Encoding') else None#: gzip, deflate
    Accept_Language = request.headers.get('Accept-Language')[0:254] if request.headers.get('Accept-Language') else None#: zh-CN,zh;q=0.9
    ua_platform = request.user_agent.platform #客户端操作系统
    ua_browser = request.user_agent.browser #客户端的浏览器
    ua_version = request.user_agent.version #客户端浏览器的版本
    ua_language = request.user_agent.language #客户端浏览器的语言
    url = request.url
    referrer = request.referrer

    returnjson = {'ip':ip,'ip_city':ip_city,'ip_asn':ip_asn,'ip_is_good':ip_is_good,'ip_asn_is_good':ip_asn_is_good,'User_Agent':User_Agent,'Host':Host,'Connection':Connection,'Pragma':Pragma,'Cache_Control':Cache_Control,'Accept':Accept,'Accept_Encoding':Accept_Encoding,'Accept_Language':Accept_Language,'ua_platform':ua_platform,'ua_browser':ua_browser,'ua_version':ua_version,'ua_language':ua_language,'url':url,'referrer':referrer}
    return jsonify(returnjson)

def shortcut_read(short_url):
    time1 = int(time.time())
    User_Agent = request.headers.get('User-Agent') 
    Accept_Language = request.headers.get('Accept-Language')#: zh-CN,zh;q=0.9
    ua_platform = request.user_agent.platform #客户端操作系统
    ua_browser = request.user_agent.browser #客户端的浏览器
    ua_version = request.user_agent.version #客户端浏览器的版本
    ua_language = request.user_agent.language #客户端浏览器的语言
    url = request.url
    referrer = request.referrer
    ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    if request.headers.get('X-Forwarded-For') is None:
        ip = request.remote_addr#服务器直接暴露        
    if admin.use_kafka is False:
        insert_shortcut_read(short_url=short_url,ip=ip,user_agent=User_Agent,accept_language=Accept_Language,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,referrer=referrer,created_at=time1)
    elif admin.use_kafka is True:
        msg = {"group":"shortcut_read","data":{"short_url":short_url,"ip":ip,"user_agent":User_Agent,"accept_language":Accept_Language,"ua_platform":ua_platform,"ua_browser":ua_browser,"ua_version":ua_version,"ua_language":ua_language,"referrer":referrer,"created_at":time1}}
        insert_message_to_kafka(key=ip, msg=msg)
    bitimage1 = os.path.join('image','43byte.gif')
    with open(bitimage1, 'rb') as f:
        returnimage = f.read()
    return Response(returnimage, mimetype="image/gif")

def show_qrcode(short_url):
    short = short_url.split("_____")[0]
    logo = short_url.split("_____")[1] if len(short_url.split("_____"))>1 else None
    returnimage = gen_qrcode(args={"qrdata":request.host_url+"t/"+short,"logo":os.path.join('image',logo) if logo and logo != "" else None})
    shortcut_read(short_url=short_url.split("_____")[0])
    return Response(returnimage, mimetype="image/png")
    # return returnimage

def show_long_qrcode():
    long_url = request.url.split('/qrcode?url=')[1]
    logo = long_url.split("_____")[1] if len(urllib.parse.unquote(long_url).split("_____"))>1 else None
    returnimage = gen_qrcode(args={"qrdata":urllib.parse.unquote(long_url).split("_____")[0],"logo":os.path.join('image',logo) if logo and logo != "" else None})
    shortcut_read(short_url=urllib.parse.unquote(long_url).split("_____")[0].split("_____")[0][0:200])
    return Response(returnimage, mimetype="image/png")


def show_all_logos():
    password = get_url_params('password')
    if password == admin.admin_password:#只有正确的密码才能触发动作
        logo_list = {'logo_list':[]}
        for maindir, subdir, file_name_list in os.walk('./image'):
            for file in file_name_list:
                logo_list['logo_list'].append({'file_name':file,'image_url':request.host_url+'image/'+file})
        return jsonify(logo_list)


def show_logo(filename):
    with open(os.path.join('image',filename), 'rb') as f:
        returnimage = f.read()
    return Response(returnimage, mimetype="image")

def access_control_list():
    password = get_url_params('password')
    if password == admin.admin_password:
        event_list = get_access_control_event()
        pending_list  = {}
        for item in event_list[0]:
            if item[0] not in pending_list:
                pending_list[item[0]] = []
            if item[1] not in pending_list[item[0]]:
                pending_list[item[0]].append(item[1])
        return jsonify({'data':pending_list})

def status_codes():
    password = get_url_params('password')
    if password == admin.admin_password:
        event_list = get_status_codes()
        pending_list  = {}
        for item in event_list[0]:
            if item[2]==0:
                pending_list[item[0]] = {'name':item[1],'list':{}}
            elif item[2]!=0:
                pending_list[item[2]]['list'][item[0]] = item[1]
        return jsonify({'data':pending_list})

def access_control_detail():
    password = get_url_params('password')
    if password == admin.admin_password:
        project = get_url_params('project')
        events = get_url_params('events')
        startdate = get_url_params('startdate')
        enddate = get_url_params('enddate')
        page = get_url_params('page') if get_url_params('page') else 1
        length = get_url_params('length') if get_url_params('length') else 50
        sort = get_url_params('sort',None)
        status = get_url_params('status',None)
        way = get_url_params('way',None)
        key = get_url_params('key',None)
        hour = get_url_params('hour',None)
        type_id = get_url_params('type_id',None)
        result_list,result_count = get_access_control_detail(project=project,events=events,startdate=startdate,enddate=enddate,page=page,length=length,sort=sort,way=way,key=key,hour=hour,status=status,type_id=type_id)
        result_total = get_access_control_detail_count(project=project,events=events,startdate=startdate,enddate=enddate,page=page,length=length,sort=sort,way=way,key=key,hour=hour,status=status,type_id=type_id)
        tag = tag_name()
        user = user_info()
        for i in range(result_count):
            result_list[i]['type_name'] = tag.find(tag_id=result_list[i]['type_id'])
            result_list[i]['status_name'] = tag.find(tag_id=result_list[i]['status_id'])
            if result_list[i]['type_id'] == 62 :
                result_list[i]['key_info'] = user.find(distinct_id=result_list[i]['key'],project=project)
            elif result_list[i]['type_id'] == 60 :
                result_list[i]['key_info'] = json.loads(get_addr(result_list[i]['key'])[0])
            result_list[i]['default_hit'] = True if result_list[i]['hour']+admin.access_control_query_hour>=int(time.strftime("%H",time.localtime())) else False
        pending_list = {'total':result_total[0][0][0],'page':page,'length':length,'count':result_count,'data':result_list}
        return jsonify(pending_list)

def update_access_status():
    password = get_url_params('password')
    if password == admin.admin_password:
        status_id_target = get_url_params('status_id_target')
        if str(status_id_target) == '78' or str(status_id_target) == '58':
            override = get_url_params('override')
            if override != admin.admin_override_code :
                return jsonify({'result':0,'desc':'永久解封或永久封禁需要提权'})
        project = get_url_params('project')
        event = get_url_params('event')
        type_id = get_url_params('type_id')
        date = get_url_params('date')
        key = get_url_params('key',None)
        hour = get_url_params('hour',None)
        status_id_source = get_url_params('status_id_source')
        if status_id_target and project and event and type_id and date and key and status_id_source and hour is not None:
            result = update_access_control(project=project,event=event,type_id=type_id,date=date,key=key,hour=hour,status_id_target=status_id_target,status_id_source=status_id_source)
            if result[1] > 0 :
                return jsonify({'result':result[1],'desc':'更新成功'})
            else:
                return jsonify({'result':result[1],'desc':'无更新内容'})
        else:
            return jsonify({'result':0,'desc':'缺参数'})


def access_permit():
    time1 = int(time.time()*1000)
    password = get_url_params('password')
    mode = get_url_params('mode')
    arr_mode = get_url_params('arr_mode')
    distinct_id = get_url_params('distinct_id')
    project = get_url_params('project')
    remark = request.args.get('remark') if 'remark' in request.args else 'normal'
    User_Agent = request.headers.get('User-Agent')[0:2047] if request.headers.get('User-Agent') else None#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
    if get_url_params('user_agent'):
        User_Agent = get_url_params('user_agent')
    if User_Agent and User_Agent !='' and 'spider' in User_Agent.lower() :
        remark = 'spider'
    Host = request.headers.get('Host') #: 10.16.5.241:5000
    if get_url_params('host'):
        Host = get_url_params('host')
    Connection = request.headers.get('Connection')#: keep-alive
    Pragma = request.headers.get('Pragma')#: no-cache
    Cache_Control = request.headers.get('Cache-Control')#: no-cache
    Accept = request.headers.get('Accept')[0:254] if request.headers.get('Accept') else None#: image/webp,image/apng,image/*,*/*;q=0.8
    Accept_Encoding = request.headers.get('Accept-Encoding')[0:254] if request.headers.get('Accept-Encoding') else None#: gzip, deflate
    Accept_Language = request.headers.get('Accept-Language')[0:254] if request.headers.get('Accept-Language') else None#: zh-CN,zh;q=0.9
    ua_platform = request.user_agent.platform #客户端操作系统
    ua_browser = request.user_agent.browser #客户端的浏览器
    ua_version = request.user_agent.version #客户端浏览器的版本
    ua_language = request.user_agent.language #客户端浏览器的语言
    ext = request.args.get('ext')
    url = request.url
    if get_url_params('request_uri'):
        url = get_url_params('request_uri')
    referrer = request.referrer[0:2047] if request.referrer else None
    if get_url_params('http_referrer') and get_url_params('http_referrer')!= '$http_referrer' :
        referrer = get_url_params('http_referrer')[0:2047]
    elif get_url_params('http_referer') and get_url_params('http_referer')!= '$http_referer' :
        referrer = get_url_params('http_referer')[0:2047]
    if get_url_params('http_x_forward_for') and get_url_params('http_x_forward_for') != '' and get_url_params('http_x_forward_for').count('.')==3:
        ip = get_url_params('http_x_forward_for')
    elif get_url_params('remote_addr') and get_url_params('remote_addr') != '' and get_url_params('remote_addr').count('.')==3:
        ip = get_url_params('remote_addr')
    elif get_url_params('ip') and get_url_params('ip') != '' and get_url_params('ip').count('.')==3:
        ip = get_url_params('ip')
    elif request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    else:
        ip = request.remote_addr#服务器直接暴露
    ip_city,ip_is_good = get_addr(ip)
    ip_asn,ip_asn_is_good = get_asn(ip)
    add_on_key = get_url_params('add_on_key')
    event = get_url_params('event')
    date = get_url_params('date')
    hour = get_url_params('hour')
    override = get_url_params('override')
    limit = get_url_params('limit')
    query_hour = get_url_params('query_hour')
    owner = get_url_params('owner')
    dnt = get_url_params('dnt')
    args = request.args
    forms = request.form
    req_jsons = request.json
    result_combine = []
    args_http_x_forward_for = get_url_params('http_x_forward_for')
    args_remote_addr = get_url_params('remote_addr')
    args_ip = get_url_params('ip')
    headers_x_forward_for = request.headers.get('X-Forwarded-For')
    remote_addr = request.remote_addr
    cookie_peoperties = request.cookies.get("sensorsdata2015jssdkcross")
    properties = {}
    if cookie_peoperties:
        properties = json.loads(urllib.parse.unquote(cookie_peoperties))
    device_id = properties['$device_id'] if '$device_id' in properties else None
    cdn_token = get_url_params('cdn_token')
    cdn_token_list = []
    token_checked = False
    if admin.access_control_cdn_mode_distinct_id_token_check is True:
        if distinct_id:
            for token in gen_token():
                sha1 = hashlib.sha1()
                sha1.update((distinct_id+token['token']).encode(encoding='utf-8'))
                cdn_token_list.append(sha1.hexdigest()[int(token['hour_str']):int(token['hour_str'])+int(token['length'])])
        token_checked = True if cdn_token in cdn_token_list else False
    distinct_event = distinct_id if admin.access_control_cdn_mode_distinct_id_token_check is False or token_checked is True or mode not in ('cdn','cdn2') else None
    
    if not distinct_event and 'distinct_id' in properties:
        distinct_event = properties['distinct_id']
    if project and (mode == 'cdn' or mode == 'cdn2' or admin.access_control_force_cdn_record is True) :
        if "http_referer" in args and "kitchen.tvcbook.com" in args["http_referer"]:
            dnt = admin.admin_do_not_track_code
        distinct_cdn = distinct_event
        if not distinct_cdn and 'uri' in args and args['uri'] == "/favicon.ico":
            distinct_cdn = "favicon.ico"
        if not distinct_cdn:
            distinct_cdn = 'cdn_mode_without_distinct_id'
        if dnt != admin.admin_do_not_track_code:
            insert_data(project=project,data_decode={'ip_data':{'args_http_x_forward_for':args_http_x_forward_for,'args_remote_addr':args_remote_addr,'args_ip':args_ip,'headers_x_forward_for':headers_x_forward_for,'remote_addr':remote_addr},'type':'track','distinct_id':distinct_cdn,'event':'cdn_mode' if mode == 'cdn' or admin.access_control_force_cdn_record is True else 'cdn_mode2','lib':{'$lib':'ghost_sa'},'_track_id':0,'properties':{'owner':owner,'args':args,'forms':forms,'jsons':req_jsons,'$device_id':device_id}},User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,created_at=None,updated_at=None,use_kafka=admin.use_kafka)#这里event强制指定为cdn_mode，哪怕是强制写入其他事件也是以cdnmode为准。保证其他查询正常，也保证cdn模式查询正常。
    if admin.access_control_query is True :
        if project:
            if not distinct_event:
                distinct_event = 'access_control_without_distinct_id'
            if password == admin.admin_password:#只有正确的密码才能触发动作
                if override != admin.admin_override_code or ( admin.access_control_token_means_override is True and token_checked is False and override != admin.admin_override_code):
                    if admin.access_control_cdn_mode_mega_match is False and mode == 'cdn': #不启动匹配其他参数功能时，cdn模式只匹配cdnmode的数据，其他模式则匹配实际的event或所有event。
                        event = 'cdn_mode'
                    elif admin.access_control_cdn_mode_mega_match is False and mode == 'cdn2': #不启动匹配其他参数功能时，cdn模式只匹配cdnmode的数据，其他模式则匹配实际的event或所有event。
                        event = 'cdn_mode2'
                    if ip:
                        ip_group = '.'.join(ip.split('.')[0:3])
                        ip_group_extend = '.'.join(ip.split('.')[0:2])
                        result_ip = query_access_control(project=project,key=ip,type_id=60,event=event,pv=limit,query_hour=query_hour,date=date,hour=hour,arr_mode=arr_mode)
                        if result_ip[0]:
                            result_combine.append(result_ip[0])
                        result_ip_group = query_access_control(project=project,key=ip_group,type_id=61,event=event,pv=limit,query_hour=query_hour,date=date,hour=hour,arr_mode=arr_mode)
                        if result_ip_group[0]:
                            result_combine.append(result_ip_group[0])
                        if admin.access_control_check_ip_group_extend == True :
                            result_ip_group_extend = query_access_control(project=project,key=ip_group_extend,type_id=80,event=event,pv=limit,query_hour=query_hour,date=date,hour=hour,arr_mode=arr_mode)
                            if result_ip_group_extend[0]:
                                result_combine.append(result_ip_group_extend[0])
                    if (mode == 'cdn' or mode == 'cdn2') and admin.access_control_cdn_mode_distinct_id_check is True:
                        distinct_id = distinct_cdn if not distinct_id else distinct_id #如果强制检查cdn模式的distinct_id，哪怕提交参数时不提交distinct_id，也会取header里的disntict_id用于检查
                        if admin.access_control_cdn_mode_distinct_id_token_check is True:
                            distinct_id = distinct_cdn #如果强制校验且校验失败，则检测cdn的id
                    if distinct_id:
                        result_distinct_id = query_access_control(project=project,key=distinct_id,type_id=62,event=event,pv=limit,query_hour=query_hour,date=date,hour=hour,arr_mode=arr_mode)
                        if result_distinct_id[0]:
                            result_combine.append(result_distinct_id[0])
                    if add_on_key:
                        result_add_on_key = query_access_control(project=project,key=add_on_key,type_id=63,event=event,pv=limit,query_hour=query_hour,date=date,hour=hour,arr_mode=arr_mode)
                        if result_add_on_key[0]:
                            result_combine.append(result_add_on_key[0])
                    if len(result_combine) > 0:
                        referrer_list = []
                        exclude_combine = 0
                        if exclude_combine ==0:
                            exclude_combine = exclude_combine + query_access_control_exclude(key=ip,project=project,type_id=60,event=event)[1]
                        if exclude_combine ==0:
                            if get_url_params('http_referer'):
                                referrer_list.append(get_url_params('http_referer')) 
                            if request.referrer:
                                referrer_list.append(request.referrer[0:2047]) 
                            for ref in referrer_list:
                                exclude_combine = exclude_combine + query_access_control_exclude(key=urllib.parse.urlparse(ref).netloc,project=project,type_id=74,event=event)[1]
                        if exclude_combine ==0:
                            exclude_combine = exclude_combine + query_access_control_exclude(key=ip_group,project=project,type_id=61,event=event)[1]
                        if exclude_combine ==0:
                            exclude_combine = exclude_combine + query_access_control_exclude(key=distinct_id,project=project,type_id=62,event=event)[1]
                        if exclude_combine ==0:
                            exclude_combine = exclude_combine + query_access_control_exclude(key=add_on_key,project=project,type_id=63,event=event)[1]
                        if exclude_combine ==0:
                            insert_data(project=project,data_decode={'ip_data':{'args_http_x_forward_for':args_http_x_forward_for,'args_remote_addr':args_remote_addr,'args_ip':args_ip,'headers_x_forward_for':headers_x_forward_for,'remote_addr':remote_addr},'type':'access_control','distinct_id':distinct_event,'event':'access_control','lib':{'$lib':'ghost_sa'},'_track_id':0,'properties':{'owner':owner,'args':args,'forms':forms,'jsons':req_jsons,'$device_id':device_id,'auth':'failed','return':result_combine,'return_code':403,'time_cost':int(time.time()*1000) - time1}},User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,created_at=None,updated_at=None,use_kafka=admin.use_kafka)
                            return jsonify({'auth':'failed','data':result_combine,'time_cost':int(time.time()*1000) - time1}),403
                if admin.access_control_force_result_record is True:
                    insert_data(project=project,data_decode={'ip_data':{'args_http_x_forward_for':args_http_x_forward_for,'args_remote_addr':args_remote_addr,'args_ip':args_ip,'headers_x_forward_for':headers_x_forward_for,'remote_addr':remote_addr},'type':'access_control','distinct_id':distinct_event,'event':'access_control','lib':{'$lib':'ghost_sa'},'_track_id':0,'properties':{'owner':owner,'args':args,'forms':forms,'jsons':req_jsons,'$device_id':device_id,'auth':'success','return':result_combine,'return_code':200,'time_cost':int(time.time()*1000) - time1}},User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,created_at=None,updated_at=None,use_kafka=admin.use_kafka)
                return jsonify({'auth':'success','data':result_combine,'time_cost':int(time.time()*1000) - time1}),200
        if project:
            insert_data(project=project,data_decode={'ip_data':{'args_http_x_forward_for':args_http_x_forward_for,'args_remote_addr':args_remote_addr,'args_ip':args_ip,'headers_x_forward_for':headers_x_forward_for,'remote_addr':remote_addr},'type':'access_control','distinct_id':distinct_event,'event':'access_control','lib':{'$lib':'ghost_sa'},'_track_id':0,'properties':{'owner':owner,'args':args,'forms':forms,'jsons':req_jsons,'$device_id':device_id,'auth':'wrong_password','return_code':403,'time_cost':int(time.time()*1000) - time1}},User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,created_at=None,updated_at=None,use_kafka=admin.use_kafka)
        return jsonify({'auth':'miss_info','data':result_combine,'time_cost':int(time.time()*1000) - time1}),403
    else:
        if admin.access_control_force_result_record is True and project:
            insert_data(project=project,data_decode={'ip_data':{'args_http_x_forward_for':args_http_x_forward_for,'args_remote_addr':args_remote_addr,'args_ip':args_ip,'headers_x_forward_for':headers_x_forward_for,'remote_addr':remote_addr},'type':'access_control','distinct_id':distinct_event,'event':'access_control','lib':{'$lib':'ghost_sa'},'_track_id':0,'properties':{'owner':owner,'args':args,'forms':forms,'jsons':req_jsons,'$device_id':device_id,'auth':'offload','return':result_combine,'return_code':200,'time_cost':int(time.time()*1000) - time1}},User_Agent=User_Agent,Host=Host,Connection=Connection,Pragma=Pragma,Cache_Control=Cache_Control,Accept=Accept,Accept_Encoding=Accept_Encoding,Accept_Language=Accept_Language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,url=url,referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,created_at=None,updated_at=None,use_kafka=admin.use_kafka)
        return jsonify({'auth':'offload','data':result_combine,'time_cost':int(time.time()*1000) - time1}),200


def get_access_control_token():
    time1 = int(time.time()*1000)
    tokenlist = gen_token()
    mode = get_url_params('mode')
    if mode == 'json':
        return jsonify({'data':{'token':tokenlist[1]['hour_str'] + tokenlist[1]['token'] + tokenlist[1]['length']},'code':200,'message':'success','result':'success','result_count':1,'time_cost':int(time.time()*1000) - time1})
    return tokenlist[1]['hour_str'] + tokenlist[1]['token'] + tokenlist[1]['length']

def get_check_token():
    distinct_id = get_url_params('distinct_id')
    override = get_url_params('override')
    password = get_url_params('password')
    if password == admin.admin_password and override == admin.admin_override_code:
        cdn_token_list = []
        keys = gen_token()
        for token in keys:
            sha1 = hashlib.sha1()
            sha1.update((distinct_id+token['token']).encode(encoding='utf-8'))
            cdn_token_list.append(sha1.hexdigest()[int(token['hour_str']):int(token['hour_str'])+int(token['length'])])
        return jsonify({'key':keys,'token':cdn_token_list})