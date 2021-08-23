# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import logging
import sys
import os
import time

from flask_cors import CORS
from flask import Flask, Response, request, g
from flask_login import login_manager
from flask_wtf import csrf
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.configs.code import ResponseCode
from app.my_extensions import NonASCIIJsonEncoder
from app.utils.response import res

sys.path.append("..")
sys.setrecursionlimit(10000000)

from app.component.api import get_datas, get_long, shortit, show_short_cut_list, ghost_check, installation_track, \
    show_project_list, show_mobile_ad_list, show_mobile_src_list, create_mobile_ad_link, check_exist_distinct_id, \
    who_am_i, shortcut_read, show_qrcode, show_long_qrcode, show_all_logos, show_logo, access_permit, \
    get_access_control_token, get_check_token
from app.component.api_noti import show_usergroup_plan, show_usergroup_list, duplicate_scheduler_jobs, \
    show_usergroup_data, disable_usergroup_data, show_temples, apply_temples_list, show_noti_group, show_noti_detial, \
    manual_send, disable_single, show_scheduler_jobs, create_scheduler_jobs_manual, create_manual_temple_noti, \
    create_manual_non_temple_noti, show_temple_args, query_msg_type, query_blacklist_single
from app.configs import admin
from app.configs.admin import recall_blacklist_commit


def create_app(config=None):
    app = Flask(__name__)

    # 使用默认配置
    app.config.from_object('app.configs.default.DefaultConfig')
    # 更新配置
    app.config.from_object(config)
    # 尝试直接通过环境进行配置
    app.config.from_envvar("GHOST_SA_SETTINGS", silent=True)

    # 配置蓝图
    configure_blueprints(app)
    # # 配置扩展
    # configure_extensions(app)
    # # 配置应用程序上下文
    # configure_context_processors(app)
    # 配置路由转发之前回调函数
    # configure_before_handlers(app)
    # 配置路由转发之后回调函数
    # configure_after_handlers(app)
    # 应用上下文的钩子,应用关闭执行
    configure_teardown_handlers(app)
    # 配置异常处理
    configure_errorhandlers(app)
    # 配置日志
    configure_logging(app)

    return app


CORS(app)


def return_error(code=0):
    page_name = str(code) + '  ' + admin.bbhj_keyword
    if admin.use_bbhj is False:
        return page_name
    if admin.use_bbhj is True:
        return f"""<html><script type="text/javascript" src="//qzonestyle.gtimg.cn/qzone/hybrid/app/404/search_children.js" charset="utf-8" homePageUrl="{admin.bbhj_url}" homePageName="{page_name}"></script></html>"""


@app.route('/')
def index():
    return return_error()


@app.route('/favicon.ico')
def favicon():
    bitimage1 = os.path.join('image', '43byte.gif')
    with open(bitimage1, 'rb') as f:
        returnimage = f.read()
    return Response(returnimage, mimetype="image/gif")


# 项目管理
app.add_url_rule('/show_project_list', view_func=show_project_list, methods=['POST'])  # 查询已有项目信息
# 数据收集
app.add_url_rule('/sa', view_func=get_datas, methods=['GET', 'POST'])  # 神策SDK上报接口
app.add_url_rule('/sa.gif', view_func=get_datas, methods=['GET', 'POST'])  # 神策SDK上报接口
# 短连接
app.add_url_rule('/t/<short_url>', view_func=get_long, methods=['GET', 'POST'])  # 解析接口
app.add_url_rule('/<short_url>.gif', view_func=shortcut_read, methods=['GET'])  # 站外跟踪
app.add_url_rule('/shortit', view_func=shortit, methods=['POST'])  # 短链创建接口
app.add_url_rule('/shortlist', view_func=show_short_cut_list, methods=['GET', 'POST'])  # 短链列表
app.add_url_rule('/qr/<short_url>', view_func=show_qrcode, methods=['GET', 'POST'])  # 显示短连接二维码
app.add_url_rule('/qrcode', view_func=show_long_qrcode, methods=['GET', 'POST'])  # 显示长链接二维码
app.add_url_rule('/image/<filename>', view_func=show_logo, methods=['GET'])  # 显示LOGO预览
app.add_url_rule('/logo_list', view_func=show_all_logos, methods=['GET'])  # 显示LOGO预览
# 埋点管理
app.add_url_rule('/ghost_check', view_func=ghost_check, methods=['POST'])  # 埋点校验接口
# 移动广告跟踪
app.add_url_rule('/cb/installation_track', view_func=installation_track, methods=['GET'])  # DSP上报接口
app.add_url_rule('/show_mobile_ad_list', view_func=show_mobile_ad_list, methods=['GET'])  # 移动跟踪列表
app.add_url_rule('/create_mobile_ad_link', view_func=create_mobile_ad_link, methods=['POST'])  # 创建移动广告跟踪链接
app.add_url_rule('/show_mobile_src_list', view_func=show_mobile_src_list, methods=['GET', 'POST'])  # 获取支持的跟踪列表
app.add_url_rule('/check_exist', view_func=check_exist_distinct_id, methods=['GET'])  # 查询idfa或其他id是否已存在
# 辅助功能
app.add_url_rule('/who_am_i', view_func=who_am_i, methods=['GET'])  # 获取自身ip

# 查询开启了用户分群与召回的项目列表
# 用户分群与召回 app.add_url_rule('/usergroups/check_enable_project', view_func=create_mobile_ad_link, methods=['POST'])
app.add_url_rule('/usergroups/show_usergroup_plan', view_func=show_usergroup_plan, methods=['POST'])  # 查询用户分群计划列表
app.add_url_rule('/usergroups/show_usergroup_list', view_func=show_usergroup_list, methods=['POST'])  # 查询计划下的用户分群列表
app.add_url_rule('/usergroups/duplicate_scheduler_jobs', view_func=duplicate_scheduler_jobs,
                 methods=['POST'])  # 重新执行该分群
app.add_url_rule('/usergroups/show_usergroup_data', view_func=show_usergroup_data, methods=['POST'])  # 查询计划下的用户分群列表的详情
app.add_url_rule('/usergroups/disable_usergroup_data', view_func=disable_usergroup_data, methods=['POST'])  # 禁用单条分群结果
app.add_url_rule('/usergroups/show_temples', view_func=show_temples, methods=['POST'])  # 查询可用的模板列表
app.add_url_rule('/usergroups/apply_temples_list', view_func=apply_temples_list, methods=['POST'])  # 对单个分群列表应用模板
app.add_url_rule('/usergroups/show_noti_group', view_func=show_noti_group, methods=['POST'])  # 查询消息群组
app.add_url_rule('/usergroups/show_noti_detial', view_func=show_noti_detial, methods=['POST'])  # 查询消息群组详情
app.add_url_rule('/usergroups/manual_send', view_func=manual_send, methods=['POST'])  # 手动推送消息群组
# app.add_url_rule('/create_mobile_ad_link', view_func=create_mobile_ad_link, methods=['POST'])         # 手动推送单条消息
app.add_url_rule('/usergroups/disable_single_noti', view_func=disable_single, methods=['POST'])  # 禁用单条消息
app.add_url_rule('/usergroups/show_scheduler_jobs', view_func=show_scheduler_jobs, methods=['POST'])  # 查询分群任务列表
# app.add_url_rule('/create_mobile_ad_link', view_func=create_mobile_ad_link, methods=['POST'])         # 手动插入推送消息
app.add_url_rule('/usergroups/create_scheduler_jobs_manual', view_func=create_scheduler_jobs_manual,
                 methods=['POST'])  # 手动开始执行分群
app.add_url_rule('/usergroups/create_manual_temple_noti', view_func=create_manual_temple_noti,
                 methods=['POST'])  # 手动创建模板消息
app.add_url_rule('/usergroups/create_manual_non_temple_noti', view_func=create_manual_non_temple_noti,
                 methods=['POST'])  # 手动创建非模板消息
app.add_url_rule('/usergroups/show_temple_args', view_func=show_temple_args, methods=['POST'])  # 查询模板需要的参数
app.add_url_rule('/usergroups/recall_blacklist_commit', view_func=recall_blacklist_commit,
                 methods=['POST'])  # 手工添加和修改黑名单
app.add_url_rule('/usergroups/noti_type', view_func=query_msg_type, methods=['POST'])  # 查询开启的消息类型
app.add_url_rule('/usergroups/blacklist_single', view_func=query_blacklist_single, methods=['POST'])  # 查询开启的消息类型

# 接入控制
app.add_url_rule('/access_control/access_permit', view_func=access_permit, methods=['POST', 'GET'])  # 查询接入控制
app.add_url_rule('/access_control/token', view_func=get_access_control_token,
                 methods=['POST', 'GET'])  # 生成cdn_mode的token
app.add_url_rule('/access_control/get_check_token', view_func=get_check_token, methods=['POST', 'GET'])  # 查询正确的token


def configure_blueprints(app):
    """
    上下文注册蓝图

    :param app: app
    """
    # 注册sa模块
    from app.flaskr.sa import sa_bp
    app.register_blueprint(sa_bp)


def configure_extensions(app):
    """
    上下文插件扩展初始化配置

    :param app: app
    """
    # 设置flask-json支持中文
    app.json_encoder = NonASCIIJsonEncoder

    # Flask-WTF CSRF
    # csrf.init_app(app)

    # Flask-Plugins
    # plugin_manager.init_app(app)

    # Flask-SQLAlchemy
    # db.init_app(app)

    # Flask-Migrate
    # migrate.init_app(app, db)

    # Flask-Mail
    # mail.init_app(app)

    # Flask-And-Redis
    # redis_store.init_app(app)

    # Flask-Login
    # login_manager.login_view = app.config["LOGIN_VIEW"]
    # login_manager.refresh_view = app.config["REAUTH_VIEW"]
    # login_manager.login_message_category = app.config["LOGIN_MESSAGE_CATEGORY"]
    # login_manager.needs_refresh_message_category = \
    #     app.config["REFRESH_MESSAGE_CATEGORY"]
    #
    # @login_manager.user_loader
    # def load_user(user_id):
    #     """
    #     user_id存储在flask的session环境中
    #     需要Flask-Login扩展，载入用户
    #
    #     :param user_id:
    #     :return None:
    #     """
    #     return None
    #
    # @login_manager.token_loader
    # def token_loader(token):
    #     """
    #     xiaowei.song 2016-6-24
    #
    #     需要Flask-Login扩展，从cookie中获取令牌（token），进行解码分析，载入用户
    #
    #     :param token:
    #     :return None:
    #     """
    #     return None
    #
    # @login_manager.request_loader
    # def load_user_from_request(req):
    #     """
    #     xiaowei.song 2016-6-24
    #
    #     需要Flask-Login扩展，可以从request-header中获取token，进行解码分析，载入用户
    #
    #     :param req:
    #     :return None:
    #     """
    #     return None
    #
    # @login_manager.unauthorized_handler
    # def unauthorized():
    #     """
    #     xiaowei.song 2016-6-24
    #
    #     定制已经配置@login_required，但未登录的url请求错误
    #
    #     :return json string:
    #     """
    #     return res(ResponseCode.NO_AUTHENTICATED)
    #
    # login_manager.init_app(app)

    # # 开启支持OAuth2支持
    # app.oauth = MyOAuthCredentials(None, app.config['CLIENT_NAME'], app.config['CLIENT_ID'],
    #                                app.config['CLIENT_SECRET'], None, None,
    #                                token_uri=app.config['GET_ACCESS_TOKEN_URI'])


def configure_context_processors(app):
    """
    配置应用上下文
    """
    pass


def configure_before_handlers(app):
    """
    请求之前处理器

    :param app:
    """

    @app.before_request
    def token_authentication():
        pass

    @app.before_request
    def update_lastseen():
        """
        更新已认证用户的最后交互时间
        """
        pass
        # if current_user.is_authenticated:
        #     current_user.lastseen = datetime.datetime.now()
        #     db.session.add(current_user)
        #     db.session.commit()

    if app.config['REDIS_ENABLED']:
        @app.before_request
        def mark_current_user_online():
            pass


# 配置回调方法
def configure_after_handlers(app):
    """
    xiaowei.song 2016-8-9

    请求之后处理器，非正常请求不处理

    :param app:
    """

    @app.teardown_request
    def teardown_request(exception):
        """
        xiaowei.song 2016-8-11
        针对模型query异常，回滚所有操作
        :param exception:
        :return:
        """
        pass


def configure_teardown_handlers(app):
    @app.teardown_appcontext
    def teardown(cmd=None):
        if cmd is None:
            db.session.commit()
        else:
            db.session.rollback()
        db.session.remove()


def configure_errorhandlers(app):
    """
    配置异常处理返回值

    :param app:
    """

    # @app.errorhandler(400)
    # def bad_request(error):
    #     error
    #     pass
    # if app.config['DEBUG'] is False:
    #     return res(400,)

    @app.errorhandler(404)
    def api_not_found(error):
        return res(ResponseCode.URL_NOT_FOUND)

    @app.errorhandler(405)
    def method_not_allowed(error):
        """
        xiaowei.song 2016-6-24

        定制405错误，若请求url路由存在但是未配置请求方式，则回复`请求方式错误，请重试`

        eg.
            @route('/api', method=['post'])
            get /api  则报这个错误
            post /api 则不报错

        :param error:
        :return:
        """
        return res(error.code, error.name)
        # return res(ResponseCode.METHOD_NOT_ALLOWED, u"请求方式错误，请重试!")

    @app.errorhandler(500)
    def server_error(error):
        return True

    from sqlalchemy.exc import SQLAlchemyError

    @app.errorhandler(SQLAlchemyError)
    def sql_alchemy_error(error):
        """
            xiaowei.song 2016-7-4

            处理sqlqlchemy异常错误
        """
        from _mysql_exceptions import OperationalError

        if not app.config['DEBUG'] and isinstance(error.orig, OperationalError):
            return res(ResponseCode.FLASK_SQLALCHEMY_EXCEPT, u"连接数据库操作异常，请联系管理员!")
        return res(ResponseCode.FLASK_SQLALCHEMY_EXCEPT, error.message)

    @app.errorhandler(AccessTokenCredentialsError)
    def access_token_error(error):
        """
            xiaowei.song 2017-3-9

            处理access token认证异常错误
        """
        return res(ResponseCode.TOKEN_CREDENTIALS_EXCEPT, error.message)


def configure_logging(app):
    """
    配置日志处理

    :param app:
    """
    # 根据时间分割日志文件
    logs_folder = os.path.join(app.root_path, os.pardir, "logs")
    logging.getLogger(app.config["LOGGER_NAME"])
    debug_formatter = logging.Formatter(app.config['DEBUG_FORMATTER'])
    info_formatter = logging.Formatter(app.config['INFO_FORMATTER'])
    error_formatter = logging.Formatter(app.config['ERROR_FORMATTER'])

    # 控制台文件中输出相应的日志信息
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(debug_formatter)
    app.logger.addHandler(stream_handler)

    import platform
    if "Linux" == platform.system():
        info_log = os.path.join(logs_folder, app.config['INFO_LOG'])

        info_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=info_log,
            when=app.config['BACKUP_WHEN'],
            backupCount=app.config['BACKUP_COUNT']
        )

        info_file_handler.suffix = app.config['BACKUP_SUFFIX']
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.setFormatter(info_formatter)
        app.logger.addHandler(info_file_handler)

        error_log = os.path.join(logs_folder, app.config['ERROR_LOG'])

        error_file_handler = logging.handlers.TimedRotatingFileHandler(
            error_log,
            when=app.config['BACKUP_WHEN'],
            backupCount=app.config['BACKUP_COUNT']
        )

        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.suffix = app.config['BACKUP_SUFFIX']
        error_file_handler.setFormatter(error_formatter)
        app.logger.addHandler(error_file_handler)

    # 设置系统默认日志记录等级
    app.logger.setLevel(logging.INFO)

    if app.config['SQLALCHEMY_ECHO']:
        # Ref: http://stackoverflow.com/a/842856
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement,
                                  parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement,
                                 parameters, context, executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
            app.logger.debug('Total Time: %f', total)


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8000)  # 默认不填写的话，是5000端口；
