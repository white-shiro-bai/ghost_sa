#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from configparser import ConfigParser

from app.flask_main import create_app

# 部署环境配置, testing 测试环境, production 生产环境, development 开发环境
ini_config = ConfigParser()
ini_config.read_file(open('uwsgi.ini'))
system_environments = ini_config.get("uwsgi", "system_environments")
print(f'获取环境变量配置成功, 环境为{system_environments}')
if system_environments == "development":
    from app.configs.development import DevelopmentConfig as Config
elif system_environments == "production":
    from app.configs.production import ProductionConfig as Config
elif system_environments == "testing":
    from app.configs.testing import TestingConfig as Config

try:
    app = create_app(Config)
except Exception as e:
    print(f"启动错误，请检查uwsgi.ini配置, {e}")

if __name__ == '__main__':
    app.logger.info(f'启动环境为: {system_environments}...')
    app.run(host=app.config['HOST'], port=app.config['PORT'], threaded=True, passthrough_errors=True)
