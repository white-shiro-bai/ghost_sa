# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")

# 数据查询接口的验证密码

admin_password = 'admin'

# 是否使用Kafka

use_kafka = False #True时，数据写入kafka。False时，直接插入数据库
use_properties = True #True时，会插入properties表，这个表不是必须的，只是方便提取数据时快速找到埋点里包含的变量。