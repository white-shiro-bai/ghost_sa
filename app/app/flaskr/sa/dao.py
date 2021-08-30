# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    持久层逻辑模块
"""
from flask import current_app

from app.flaskr.sa.models import ProjectDeviceModel, ProjectPropertiesModel, ProjectUserModel
from app.my_extensions import db
from app.utils.database import model_to_dict


def insert_event(request_data):
    project_model = request_data.to_project_model()

    db.session.add(project_model)
    # 事务
    db.session.commit()
    current_app.logger.debug(f'插入事件数据成功， 数据为: {model_to_dict(project_model)}')
    return 1


def insert_or_update_device(request_data):
    request_data.set_other_properties()
    count = insert_device_db(request_data)
    current_app.logger.debug(f'插入或更新device={count}条')


def insert_device_db(request_data):
    table = request_data.project
    distinct_id = request_data.distinct_id
    ProjectDeviceModel.__table__.name = f'{table}_device'
    project_device_model_db = ProjectDeviceModel.query.filter_by(distinct_id=distinct_id).first()
    if project_device_model_db is None:
        project_device_model_db = request_data.to_project_device_model()
        db.session.add(project_device_model_db)
    else:   # 更新非空字段信息
        request_data.update_project_device_model(project_device_model_db)

    db.session.commit()
    return 1


def insert_properties(request_data):
    table = request_data.project
    lib = request_data.lib
    remark = request_data.remark
    event = request_data.event

    ProjectPropertiesModel.__table__.name = f'{table}_properties'
    project_properties_model_db = ProjectPropertiesModel.query.filter_by(event=event, lib=lib, remark=remark).first()
    if project_properties_model_db is None:
        project_properties_model_db = request_data.to_project_device_model()
        db.session.add(project_properties_model_db)
    else:   # 更新非空字段信息
        request_data.update_project_properties_model(project_properties_model_db)

    db.session.commit()
    current_app.logger.debug(f'插入或更新事件属性数据成功， 数据为: {model_to_dict(project_properties_model_db)}')
    return 1


def insert_user(request_data):
    table = request_data.project
    distinct_id = request_data.distinct_id
    lib = request_data.lib
    map_id = request_data.map_id
    original_id = request_data.original_id

    ProjectUserModel.__table__.name = f'{table}_user'
    project_user_model_db = ProjectUserModel.query.filter_by(distinct_id=distinct_id, lib=lib, map_id=map_id, original_id=original_id).first()
    if project_user_model_db is None:
        project_user_model_db = request_data.to_project_user_model()
        db.session.add(project_user_model_db)
    else:  # 更新非空字段信息
        request_data.update_project_properties_model(project_user_model_db)

    db.session.commit()
    current_app.logger.debug(f'插入或更新用户属性数据成功， 数据为: {model_to_dict(project_user_model_db)}')
    return 1