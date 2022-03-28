# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    鬼策埋点上报模块.
"""

from flask import Blueprint

from app.configs.code import ResponseCode
from app.flaskr.sa.bu import get_data
from app.utils.response import res

sa_bp = Blueprint('sa', __name__)


@sa_bp.route('/sa.gif', methods=('GET', 'POST'))
@sa_bp.route('/sa', methods=('GET', 'POST'))
def register():
    return get_data()


@sa_bp.route('/favicon.ico')
@sa_bp.route('/')
def index():
    return res(ResponseCode.SUCCEED)
