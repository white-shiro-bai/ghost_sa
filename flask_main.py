# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.setrecursionlimit(10000000)
from configs import admin
if admin.access_control_commit_mode =='none_kafka':
    from component.access_control import access_control
    ac_none_kafka = access_control()
from component.api import get_datas, get_long, shortit, show_short_cut_list, ghost_check ,installation_track,show_project_list,show_mobile_ad_list,show_mobile_src_list,create_mobile_ad_link,check_exist_distinct_id,who_am_i,shortcut_read,show_qrcode,show_long_qrcode,show_all_logos,show_logo,access_permit,get_access_control_token,get_check_token,access_control_list,access_control_detail,update_access_status,status_codes,decode_sa_data,batch_cache,debug_datas
from component.api_noti import show_usergroup_plan,show_usergroup_list,duplicate_scheduler_jobs,show_usergroup_data,disable_usergroup_data,show_temples,apply_temples_list,show_noti_group,show_noti_detial,manual_send,disable_single,show_scheduler_jobs,create_scheduler_jobs_manual,create_manual_temple_noti,create_manual_non_temple_noti,show_temple_args,recall_blacklist_commit,query_msg_type,query_blacklist_single,sms_callback
from flask_cors import CORS
from flask import Flask,Response
import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
CORS(app,origins='*',supports_credentials=True,allow_headers='*')

if admin.batch_send_deduplication_mode in ('ram','tidb6.4-'):
    batch_send_scheduler = BackgroundScheduler()
    batch_send_scheduler.add_job(batch_cache.clean_expired, 'interval', seconds=admin.batch_send_max_memory_gap)
    batch_send_scheduler.start()

def return_error(code=0):
    pagename = str(code) + '  '+admin.bbhj_keyword
    if admin.use_bbhj is False:
        return  pagename
    if admin.use_bbhj is True:
        return f"""<html><script type="text/javascript" src="//qzonestyle.gtimg.cn/qzone/hybrid/app/404/search_children.js" charset="utf-8" homePageUrl="{admin.bbhj_url}" homePageName="{pagename}"></script></html>"""

# @app.before_request



# @app.teardown_appcontext
# def close_scheduler(*args):
#     print(args)
#     batch_send_scheduler.shutdown()


@app.errorhandler(404)
def miss(e):
    return return_error(code=404),404

@app.errorhandler(500)
def error(e):
    return return_error(code=500),500

@app.errorhandler(405)
def error2(e):
    return return_error(code=405),405


@app.route('/')
def index():
    return return_error()

@app.route('/favicon.ico')
def favicon():
    bitimage1 = os.path.join('image','43byte.gif')
    with open(bitimage1, 'rb') as f:
        returnimage = f.read()
    return Response(returnimage, mimetype="image/gif")


#功能测试
@app.route('/a')
def test():
    from component.api import batch_cache
    for i in range(10):
        batch_cache.query(project='test_me',distinct_id=str(i),track_id=123,time13=1698573153331)
    return str(batch_cache.cache)

#项目管理
app.add_url_rule('/show_project_list', view_func=show_project_list, methods=['POST'])#查询已有项目信息
app.add_url_rule('/status_codes', view_func=status_codes, methods=['GET','POST'])#查询状态列表
#数据收集
app.add_url_rule('/sa', view_func=get_datas, methods=['GET', 'POST'])#神策SDK上报接口
app.add_url_rule('/sa.gif', view_func=get_datas, methods=['GET', 'POST'])#神策SDK上报接口
app.add_url_rule('/debug', view_func=debug_datas, methods=['GET', 'POST' , 'OPTIONS'])#神策SDKdebug模式接口
#短连接
app.add_url_rule('/t/<short_url>', view_func=get_long, methods=['GET', 'POST'])#解析接口
app.add_url_rule('/<short_url>.gif', view_func=shortcut_read, methods=['GET'])#站外跟踪
app.add_url_rule('/shortit', view_func=shortit, methods=['POST'])#短链创建接口
app.add_url_rule('/shortlist', view_func=show_short_cut_list,methods=['GET', 'POST'])#短链列表
app.add_url_rule('/qr/<short_url>', view_func=show_qrcode,methods=['GET', 'POST'])#显示短连接二维码
app.add_url_rule('/qrcode', view_func=show_long_qrcode,methods=['GET', 'POST'])#显示长链接二维码
app.add_url_rule('/image/<filename>', view_func=show_logo, methods=['GET'])#显示LOGO预览
app.add_url_rule('/logo_list', view_func=show_all_logos, methods=['GET'])#显示LOGO预览
#埋点管理
app.add_url_rule('/ghost_check', view_func=ghost_check, methods=['POST'])#埋点校验接口
#移动广告跟踪
app.add_url_rule('/cb/installation_track', view_func=installation_track, methods=['GET'])#DSP上报接口
app.add_url_rule('/show_mobile_ad_list', view_func=show_mobile_ad_list, methods=['GET'])#移动跟踪列表
app.add_url_rule('/create_mobile_ad_link', view_func=create_mobile_ad_link, methods=['POST'])#创建移动广告跟踪链接
app.add_url_rule('/show_mobile_src_list', view_func=show_mobile_src_list, methods=['GET','POST'])#获取支持的跟踪列表
app.add_url_rule('/check_exist', view_func=check_exist_distinct_id, methods=['GET'])#查询idfa或其他id是否已存在
#辅助功能
app.add_url_rule('/who_am_i', view_func=who_am_i, methods=['GET'])#获取自身ip
app.add_url_rule('/dc', view_func=decode_sa_data, methods=['GET'])#通用解码

#用户分群与召回
# app.add_url_rule('/usergroups/check_enable_project', view_func=create_mobile_ad_link, methods=['POST'])#查询开启了用户分群与召回的项目列表
app.add_url_rule('/usergroups/show_usergroup_plan', view_func=show_usergroup_plan, methods=['POST'])#查询用户分群计划列表
app.add_url_rule('/usergroups/show_usergroup_list', view_func=show_usergroup_list, methods=['POST'])#查询计划下的用户分群列表
app.add_url_rule('/usergroups/duplicate_scheduler_jobs', view_func=duplicate_scheduler_jobs, methods=['POST'])#重新执行该分群
app.add_url_rule('/usergroups/show_usergroup_data', view_func=show_usergroup_data, methods=['POST'])#查询计划下的用户分群列表的详情
app.add_url_rule('/usergroups/disable_usergroup_data', view_func=disable_usergroup_data, methods=['POST'])#禁用单条分群结果
app.add_url_rule('/usergroups/show_temples', view_func=show_temples, methods=['POST'])#查询可用的模板列表
app.add_url_rule('/usergroups/apply_temples_list', view_func=apply_temples_list, methods=['POST'])#对单个分群列表应用模板
app.add_url_rule('/usergroups/show_noti_group', view_func=show_noti_group, methods=['POST'])#查询消息群组
app.add_url_rule('/usergroups/show_noti_detial', view_func=show_noti_detial, methods=['POST'])#查询消息群组详情
app.add_url_rule('/usergroups/manual_send', view_func=manual_send, methods=['POST'])#手动推送消息群组
# app.add_url_rule('/create_mobile_ad_link', view_func=create_mobile_ad_link, methods=['POST'])#手动推送单条消息
app.add_url_rule('/usergroups/disable_single_noti', view_func=disable_single, methods=['POST'])#禁用单条消息
app.add_url_rule('/usergroups/show_scheduler_jobs', view_func=show_scheduler_jobs, methods=['POST'])#查询分群任务列表
# app.add_url_rule('/create_mobile_ad_link', view_func=create_mobile_ad_link, methods=['POST'])#手动插入推送消息
app.add_url_rule('/usergroups/create_scheduler_jobs_manual',view_func=create_scheduler_jobs_manual, methods=['POST'])#手动开始执行分群
app.add_url_rule('/usergroups/create_manual_temple_noti',view_func=create_manual_temple_noti, methods=['POST'])#手动创建模板消息
app.add_url_rule('/usergroups/create_manual_non_temple_noti',view_func=create_manual_non_temple_noti, methods=['POST'])#手动创建非模板消息
app.add_url_rule('/usergroups/show_temple_args',view_func=show_temple_args, methods=['POST'])#查询模板需要的参数
app.add_url_rule('/usergroups/recall_blacklist_commit',view_func=recall_blacklist_commit, methods=['POST'])#手工添加和修改黑名单
app.add_url_rule('/usergroups/noti_type',view_func=query_msg_type, methods=['POST'])#查询开启的消息类型
app.add_url_rule('/usergroups/blacklist_single',view_func=query_blacklist_single, methods=['POST'])#查询开启的消息类型
app.add_url_rule('/usergroups/sms_callback',view_func=sms_callback, methods=['POST'])#第三方短信平台到达情况回调

#接入控制
app.add_url_rule('/access_control/access_permit',view_func=access_permit, methods=['POST','GET'])#查询接入控制
app.add_url_rule('/access_control/token',view_func=get_access_control_token, methods=['POST','GET'])#生成cdn_mode的token
app.add_url_rule('/access_control/get_check_token',view_func=get_check_token, methods=['POST','GET'])#查询正确的token
app.add_url_rule('/access_control/access_control_list',view_func=access_control_list, methods=['POST','GET'])#查询已有的控制列表类型
app.add_url_rule('/access_control/access_control_detail',view_func=access_control_detail, methods=['POST','GET'])#查看列表详情
app.add_url_rule('/access_control/update_access_status',view_func=update_access_status, methods=['POST','GET'])#修改详情

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8000)  # 默认不填写的话，是5000端口；