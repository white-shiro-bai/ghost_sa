# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
from component.api import get_datas, get_long, shortit, show_short_cut_list, ghost_check ,installation_track ,show_project_list
from flask_cors import CORS
from flask import jsonify
from flask import make_response
from flask import request
from flask import Flask
import sys
sys.path.append("..")
sys.setrecursionlimit(10000000)


app = Flask(__name__)
CORS(app)

ad_words = '你的请求不合法哟。对我们那么感兴趣的话，投个简历给我吧。unknowwhite@outlook.com'


@app.errorhandler(404)
def miss(e):
    return '404.159265357 '+ad_words


@app.errorhandler(500)
def error(e):
    return '500.159265357 '+ad_words


@app.errorhandler(405)
def error2(e):
    return '405.159265357 '+ad_words


@app.route('/')
def index():
    return ad_words


#项目管理
app.add_url_rule('/show_project_list', view_func=show_project_list, methods=['POST'])#查询已有项目信息
#数据收集
app.add_url_rule('/sa.gif', view_func=get_datas, methods=['GET', 'POST'])#神策SDK上报接口
#短连接
app.add_url_rule('/t/<short_url>', view_func=get_long, methods=['GET', 'POST'])#解析接口
app.add_url_rule('/shortit', view_func=shortit, methods=['POST'])#短链创建接口
app.add_url_rule('/shortlist', view_func=show_short_cut_list,methods=['GET', 'POST'])#短链列表
#埋点管理
app.add_url_rule('/ghost_check', view_func=ghost_check, methods=['POST'])#埋点校验接口
#移动广告跟踪
app.add_url_rule('/cb/installation_track', view_func=installation_track, methods=['GET'])#DSP上报接口

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8000)  # 默认不填写的话，是5000端口；
