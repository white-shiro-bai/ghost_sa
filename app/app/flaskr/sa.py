# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    鬼策埋点上报模块.
"""

from flask import Blueprint

from app.component.api import get_data

sa_bp = Blueprint('sa', __name__)


@sa_bp.route('/sa', methods=('GET', 'POST'))
def register():
    return get_data()
