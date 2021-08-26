#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.manage
    ~~~~~~~~~~~~~~~~~~~~
    这个脚本提供一些简单的命令创建数据库包含一些简单的内容，
    执行`python manage.py`执行开发环境，可以看到一列可选命令
    TODO: When Flask 1.0 is released, get rid of Flask-Script and use click.
          Then it's also possible to split the commands in "command groups"
          which would make the commands better seperated from each other
          and less confusing.

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from configparser import ConfigParser

from flask_migrate import upgrade, MigrateCommand
from flask_script import (Manager, Server, prompt_bool)
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.utils import import_string

from app.flask_main import create_app
from app.my_extensions import db

# 假如存在开发配置，则使用开发模式，否则默认模式配置
try:
    from app.configs.development import DevelopmentConfig as Config
except ImportError:
    from app.configs.default import DefaultConfig as Config

app = create_app(Config)
manager = Manager(app)

# 运行本地服务
manager.add_command("runserver", Server("localhost", port=5000))
manager.add_command("runserver", Server(app.config["HOST"], port=app.config["PORT"], passthrough_errors=True))

# 迁移数据库命令
manager.add_command('db', MigrateCommand)


@manager.option('-s', '--system_environments', dest="system_environments", default=None)
def uwsgi(system_environments):
    if system_environments not in ["development", "production", "testing"]:
        print("""请输入正确参数, testing 对应 测试环境, production 对应 生产环境, development 对应 开发环境""")
    else:
        pwd = os.popen("pwd").read().strip("\n")
        ini_config = ConfigParser.ConfigParser()
        ini_config.add_section("uwsgi")
        ini_config.set("uwsgi", "http", "{0}:{1}".format(app.config["HOST"], app.config["PORT"]))
        ini_config.set("uwsgi", "processes", app.config["PROCESSES"])
        ini_config.set("uwsgi", "threads", app.config["THREADS"])
        ini_config.set("uwsgi", "pythonpath", "{}".format(pwd))
        ini_config.set("uwsgi", "callable", app.config["CALLABLE"])
        ini_config.set("uwsgi", "module", app.config["MODULE"])
        ini_config.set("uwsgi", "daemonize", "{}/uwsgi.log".format(pwd))
        ini_config.set("uwsgi", "system_environments", system_environments)
        ini_config.write(open('uwsgi.ini', "w"))


@manager.command
def initdb():
    u"""创建数据库"""

    upgrade()


@manager.command
def dropdb():
    """删除数据库"""

    db.drop_all()


@manager.command
def populate(dropdb=False, createdb=False):
    """创建数据库包含默认的数据
    使用`-d`、`-c`参数删除或者新建数据库
    """

    if dropdb:
        print("删除数据库中...")
        db.drop_all()

    if createdb:
        print("新建数据库中...")
        upgrade()

    app.logger.info("初始化默认数据中...")
    # create_test_data()


@manager.option('-u', '--name', dest='name')
@manager.option('-p', '--passwd', dest='passwd')
@manager.option('-e', '--email', dest='email')
def install(username=None, password=None, email=None):
    """创建所有的数据"""

    print("创建默认的数据中...")
    try:
        pass
        # create_default_groups()
        # create_default_settings()
    except IntegrityError:
        print("不可以创建默认的数据，因为它已经存在!")
        if prompt_bool("找到存在的数据库"
                       "需要覆盖默认的数据库吗? (y/n)"):
            db.session.rollback()
            db.drop_all()
            upgrade()
            # create_default_groups()
            # create_default_settings()
        else:
            sys.exit(0)
    except OperationalError:
        print("数据库不存在")
        if prompt_bool("现在新建数据库? (y/n)"):
            db.session.rollback()
            upgrade()
            # create_default_groups()
            # create_default_settings()
        else:
            sys.exit(0)

    print("创建管理员...")
    if username and password and email:
        pass
        # create_admin_user(name=name, passwd=passwd, email=email)
    else:
        pass
        # create_admin()

    print("Creating welcome forum...")
    # create_welcome_forum()

    print("恭喜，安装成功！")


@manager.option('-f', '--force', dest="force", default=False)
@manager.option('-s', '--settings', dest="settings")
def update(settings=None, force=False):
    """直接通过固定设置更新配置属性，所有的固定设置已经指向了`fixture`
    Usage: python manage.py update -s your_fixture
    """
    if settings is None:
        settings = "settings"

    try:
        fixture = import_string(
            "App.fixtures.{}".format(settings)
        )
        fixture = fixture.fixture
    except ImportError:
        raise "{} fixture is not available".format(settings)

    overwrite_group = overwrite_setting = False
    if force:
        overwrite_group = overwrite_setting = True

    # count = update_settings_from_fixture(
    #     fixture=fixture,
    #     overwrite_group=overwrite_group,
    #     overwrite_setting=overwrite_setting
    # )
    # print("{} groups and {} settings updated.".format(
    #     len(count.keys()), len(count.values()))
    # )


@manager.option('-l', '--length', dest="length", default=8)
def create_password(length=8):
    """生成密码字段
    Usage: python manage.py create_password -l 8
    """
    import random
    import string
    print('password: ' + ''.join(random.sample(string.ascii_letters + string.digits, int(length))))


@manager.option('-l', '--length', dest='length', default=25)
@manager.option('-d', '--directory', dest='profile_dir', default=None)
def profile(length=25, profile_dir=None):
    """"基于代码分析器启动应用."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])


if __name__ == "__main__":
    manager.run()
