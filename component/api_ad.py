# -*- coding: utf-8 -*-
#
#Date: 2021-09-28 14:35:25
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2021-12-02 17:52:04
#FilePath: \server_gitlab\component\api_ad.py
#
import sys
import json
sys.path.append('./')
from flask import jsonify
from component.user_profile import profile_control
from component.url_tools import get_url_params
from configs import admin


def get_my_profile():
    org_profile_id = get_url_params('org_profile_id')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner', 'get_my_profile_api')
    control = profile_control(project=project, remark=remark, owner=owner)
    myprofile = control.my_profile(org_profile_id=org_profile_id)
    return jsonify({'project':project,'remark':remark,'owner':owner,'org_profile_id':org_profile_id,'profile':myprofile})

def get_my_profile_list():
    # 管理端获取配置
    # show all list for admin ui
    org_profile_id = get_url_params('org_profile_id')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner', 'get_my_profile_api')
    password = get_url_params('password')
    if password == admin.admin_password:
        control = profile_control(project=project,remark=remark,owner=owner)
        myprofile = control.show(limit=100)
        return jsonify(myprofile)

def insert_new_profile():
    password = get_url_params('password')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner')
    profile = get_url_params('profile')
    desc = get_url_params('desc')
    if password == admin.admin_password:
        if project and remark and owner and profile and desc:
            control = profile_control(project=project,remark=remark,owner=owner)
            control.json(profile=json.loads(profile))
            result  = control.create(desc=desc)
            return jsonify({'result':result[0],'code':result[1]})
        else:
            return jsonify({'result':'缺参数','code':71})
    else:
        return jsonify({'result':'密码不正确','code':71})

def update_new_profile():
    password = get_url_params('password')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner')
    pre_profile_id = get_url_params('pre_profile_id')
    gray_percent = get_url_params('gray_percent')
    profile = get_url_params('profile')
    desc = get_url_params('desc')
    override = get_url_params('override') 
    update_now = get_url_params('update_now') if override == admin.admin_override_code else 'No'
    if password == admin.admin_password:
        if project and remark and owner and profile and desc and pre_profile_id and  gray_percent is not None:
            control = profile_control(project=project,remark=remark,owner=owner)
            control.json(profile=profile)
            result  = control.update(profile_id=pre_profile_id,desc=desc,gray_percent=gray_percent,update_now=update_now)
            return jsonify({'result':result[0],'code':result[1]})
        else:
            return jsonify({'result':'缺参数','code':71})
    else:
        return jsonify({'result':'密码不正确','code':71})

def enable_profile():
    password = get_url_params('password')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner')
    profile_id = get_url_params('profile_id')
    override = get_url_params('override') 
    update_now = get_url_params('update_now') if override == admin.admin_override_code else 'No'
    if password == admin.admin_password:
        if project and remark and owner and profile_id :
            control = profile_control(project=project,remark=remark,owner=owner)
            result  = control.enable(profile_id=int(profile_id),update_now=update_now)
            return jsonify({'result':result[0],'code':result[1]})
        else:
            return jsonify({'result':'缺参数','code':71})
    else:
        return jsonify({'result':'密码不正确','code':71})

def roll_back():
    password = get_url_params('password')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner')
    profile_id = get_url_params('profile_id')
    target_profile_id = get_url_params('target_profile_id')
    override = get_url_params('override') 
    update_now = get_url_params('update_now') if override == admin.admin_override_code else 'No'
    if password == admin.admin_password:
        if project and remark and owner and profile_id:
            control = profile_control(project=project,remark=remark,owner=owner)
            result  = control.rollback(profile_id=profile_id,target_profile_id=target_profile_id,update_now=update_now)
            return jsonify({'result':result[0],'code':result[1]})
        else:
            return jsonify({'result':'缺参数','code':71})
    else:
        return jsonify({'result':'密码不正确','code':71})

def disable():
    password = get_url_params('password')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner')
    profile_id = get_url_params('profile_id')
    if password == admin.admin_password:
        if project and remark and owner and profile_id:
            control = profile_control(project=project,remark=remark,owner=owner)
            result  = control.disable(profile_id=int(profile_id))
            return jsonify({'result':result[0],'code':result[1]})
        else:
            return jsonify({'result':'缺参数','code':71})
    else:
        return jsonify({'result':'密码不正确','code':71})

def lock_version():
    password = get_url_params('password')
    project = get_url_params('project')
    remark = get_url_params('remark')
    owner = get_url_params('owner')
    profile_id = get_url_params('profile_id')
    if password == admin.admin_password:
        if project and remark and owner and profile_id:
            control = profile_control(project=project,remark=remark,owner=owner)
            result  = control.lock_version(profile_id=int(profile_id))
            return jsonify({'result':result[0],'code':result[1]})
        else:
            return jsonify({'result':'缺参数','code':71})
    else:
        return jsonify({'result':'密码不正确','code':71})

