# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.db_op import do_tidb_exe,do_tidb_select
from component.db_func import insert_mobile_ad_src
import time
import csv
import os

def update_table_history(project_name):
  #升级user表支持多个设备绑定。2019-12-11
  sql="""CREATE TABLE `{project_name}_user2` (
  `distinct_id` varchar(255) NOT NULL,
  `lib` varchar(255) NOT NULL,
  `map_id` varchar(255) NOT NULL,
  `original_id` varchar(255) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `all_user_profile` json DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`distinct_id`,`lib`,`map_id`,`original_id`),
  KEY `distinct_id` (`distinct_id`),
  KEY `map_id` (`map_id`),
  KEY `original_id` (`original_id`),
  KEY `distinct_id_lib` (`distinct_id`,`lib`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
set @@session.tidb_batch_insert = 1;
INSERT into {project_name}_user2 (
SELECT * FROM `{project_name}_user`);
set @@session.tidb_batch_insert = 0;
ALTER table {project_name}_user RENAME to {project_name}_user3;
ALTER table {project_name}_user2 RENAME to {project_name}_user;""".format(project_name=project_name)
  result,count=do_tidb_exe(sql)
  print(result)


def create_project(project_name,expired=None):
  #创建新项目，project_name是项目名，expired是过期时间，字串输入 2019-01-01 格式
  create_project_list = """CREATE TABLE if not EXISTS `project_list` (
  `project_name` varchar(255) DEFAULT NULL COMMENT '项目名称',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  `expired_at` int(11) DEFAULT NULL COMMENT '过期时间',
  `event_count` bigint(20) DEFAULT NULL COMMENT '事件量',
  `device_count` bigint(20) DEFAULT NULL COMMENT '设备数',
  `user_count` bigint(20) DEFAULT NULL COMMENT '用户数'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
CREATE TABLE if not EXISTS `shortcut` (
  `project` varchar(255) DEFAULT NULL COMMENT '项目名',
  `short_url` varchar(255) DEFAULT NULL COMMENT '短链地址',
  `long_url` varchar(3072) DEFAULT NULL COMMENT '长链地址',
  `expired_at` int(11) DEFAULT NULL COMMENT '过期时间',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  `src` varchar(10) DEFAULT NULL COMMENT '使用的第三方创建源',
  `src_short_url` varchar(255) DEFAULT NULL COMMENT '创建源返回的短地址',
  `submitter` varchar(255) DEFAULT NULL COMMENT '由谁提交',
  `utm_source` varchar(2048) DEFAULT NULL COMMENT 'utm_source',
  `utm_medium` varchar(2048) DEFAULT NULL COMMENT 'utm_medium',
  `utm_campaign` varchar(2048) DEFAULT NULL COMMENT 'utm_campaign',
  `utm_content` varchar(2048) DEFAULT NULL COMMENT 'utm_content',
  `utm_term` varchar(2048) DEFAULT NULL COMMENT 'utm_term',
  KEY `short_url` (`short_url`),
  KEY `long_url` (`long_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
CREATE TABLE if not EXISTS `shortcut_history` (
  `short_url` varchar(255) DEFAULT NULL COMMENT '解析短链',
  `result` varchar(255) DEFAULT NULL COMMENT '解析的结果',
  `cost_time` int(11) DEFAULT NULL COMMENT '耗费时间',
  `ip` varchar(255) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL COMMENT '解析时间',
  `user_agent` text DEFAULT NULL,
  `accept_language` text DEFAULT NULL,
  `ua_platform` varchar(255) DEFAULT NULL,
  `ua_browser` varchar(255) DEFAULT NULL,
  `ua_version` varchar(255) DEFAULT NULL,
  `ua_language` varchar(255) DEFAULT NULL,
  KEY `created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
CREATE TABLE if not EXISTS `mobile_ad_src` (
  `src` varchar(255) NOT NULL COMMENT '创建源名称',
  `src_name` varchar(255) DEFAULT NULL COMMENT '创建源的中文名字',
  `src_args` varchar(1024) DEFAULT NULL COMMENT '创建源自带参数',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  `updated_at` int(11) DEFAULT NULL COMMENT '维护时间',
  `utm_source` varchar(255) DEFAULT NULL COMMENT '预制的utm_source',
  `utm_medium` varchar(255) DEFAULT NULL COMMENT '预制的utm_medium',
  `utm_campaign` varchar(255) DEFAULT NULL COMMENT '预制的utm_campaign',
  `utm_content` varchar(255) DEFAULT NULL COMMENT '预制的utm_content',
  `utm_term` varchar(255) DEFAULT NULL COMMENT '预制的utm_term',
  PRIMARY KEY (`src`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
CREATE TABLE if not EXISTS `mobile_ad_list` (
  `project` varchar(255) DEFAULT NULL COMMENT '项目名',
  `url` varchar(2048) NOT NULL COMMENT '监测地址',
  `expired_at` int(11) DEFAULT NULL COMMENT '过期时间',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  `src` varchar(255) DEFAULT NULL COMMENT '使用的检测原id',
  `src_url` varchar(1024) DEFAULT NULL COMMENT '使用的检测模板',
  `submitter` varchar(255) DEFAULT NULL COMMENT '由谁提交',
  `utm_source` varchar(2048) DEFAULT NULL COMMENT 'utm_source',
  `utm_medium` varchar(2048) DEFAULT NULL COMMENT 'utm_medium',
  `utm_campaign` varchar(2048) DEFAULT NULL COMMENT 'utm_campaign',
  `utm_content` varchar(2048) DEFAULT NULL COMMENT 'utm_content',
  `utm_term` varchar(2048) DEFAULT NULL COMMENT 'utm_term',
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
  do_tidb_exe(create_project_list)
  # print('project_list已生成')
  check_sql = "show tables"
  check_result,check_count = do_tidb_select(check_sql)
  tables_name = []
  for line in check_result:
    tables_name.append(line[0])
  # print(tables_name)
  check_project_list_sql = """SELECT count(*) FROM `project_list` where project_name='{project_name}'""".format(project_name=project_name)
  check_project_list_result,check_project_list_count = do_tidb_select(check_project_list_sql)
  # print(check_project_list_result[0][0])
  if project_name in tables_name or check_project_list_result[0][0]>0:
    print(project_name+'项目表单已存在')
  else:
    table_sql="""CREATE TABLE `{project_name}` (
  `track_id` bigint(17) DEFAULT NULL,
  `distinct_id` varchar(64) DEFAULT NULL,
  `lib` varchar(255) DEFAULT NULL,
  `event` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `all_json` json DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `user_agent` varchar(2048) DEFAULT NULL,
  `ua_platform` varchar(1024) DEFAULT NULL,
  `ua_browser` varchar(1024) DEFAULT NULL,
  `ua_version` varchar(1024) DEFAULT NULL,
  `ua_language` varchar(1024) DEFAULT NULL,
  `connection` varchar(255) DEFAULT NULL,
  `pragma` varchar(255) DEFAULT NULL,
  `cache_control` varchar(255) DEFAULT NULL,
  `accept` varchar(255) DEFAULT NULL,
  `accept_encoding` varchar(255) DEFAULT NULL,
  `accept_language` varchar(255) DEFAULT NULL,
  `ip` varchar(512) DEFAULT NULL,
  `ip_city` json DEFAULT NULL,
  `ip_asn` json DEFAULT NULL,
  `url` text DEFAULT NULL,
  `referrer` varchar(2048) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `hour` int(2) DEFAULT NULL,
  KEY `date` (`date`),
  KEY `distinct_id` (`distinct_id`),
  KEY `event` (`event`),
  KEY `date_hour` (`date`,`hour`),
  KEY `event_date` (`event`,`date`),
  KEY `event_remark_date` (`event`,`remark`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;""".format(project_name=project_name)
    table_device_sql ="""CREATE TABLE `{project_name}_device` (
  `distinct_id` varchar(255) NOT NULL,
  `lib` varchar(255) DEFAULT NULL,
  `device_id` varchar(255) DEFAULT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `os` varchar(255) DEFAULT NULL,
  `os_version` varchar(255) DEFAULT NULL,
  `ua_platform` varchar(1024) DEFAULT NULL,
  `ua_browser` varchar(1024) DEFAULT NULL,
  `ua_version` varchar(1024) DEFAULT NULL,
  `ua_language` varchar(1024) DEFAULT NULL,
  `screen_width` int(11) DEFAULT NULL,
  `screen_height` int(11) DEFAULT NULL,
  `network_type` varchar(255) DEFAULT NULL,
  `user_agent` varchar(2048) DEFAULT NULL,
  `accept_language` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `ip_city` json DEFAULT NULL,
  `ip_asn` json DEFAULT NULL,
  `wifi` varchar(20) DEFAULT NULL,
  `app_version` varchar(255) DEFAULT NULL,
  `carrier` varchar(255) DEFAULT NULL,
  `referrer` text DEFAULT NULL,
  `referrer_host` varchar(2048) DEFAULT NULL,
  `bot_name` varchar(255) DEFAULT NULL,
  `browser` varchar(255) DEFAULT NULL,
  `browser_version` varchar(255) DEFAULT NULL,
  `is_login_id` varchar(255) DEFAULT NULL,
  `screen_orientation` varchar(255) DEFAULT NULL,
  `gps_latitude` decimal(11,7) DEFAULT NULL,
  `gps_longitude` decimal(11,7) DEFAULT NULL,
  `first_visit_time` datetime DEFAULT NULL,
  `first_referrer` text DEFAULT NULL,
  `first_referrer_host` varchar(1024) DEFAULT NULL,
  `first_browser_language` varchar(1024) DEFAULT NULL,
  `first_browser_charset` varchar(1024) DEFAULT NULL,
  `first_search_keyword` varchar(1024) DEFAULT NULL,
  `first_traffic_source_type` varchar(1024) DEFAULT NULL,
  `utm_content` varchar(2048) DEFAULT NULL,
  `utm_campaign` varchar(2048) DEFAULT NULL,
  `utm_medium` varchar(2048) DEFAULT NULL,
  `utm_term` varchar(2048) DEFAULT NULL,
  `utm_source` varchar(2048) DEFAULT NULL,
  `latest_utm_content` varchar(2048) DEFAULT NULL,
  `latest_utm_campaign` varchar(2048) DEFAULT NULL,
  `latest_utm_medium` varchar(2048) DEFAULT NULL,
  `latest_utm_term` varchar(2048) DEFAULT NULL,
  `latest_utm_source` varchar(2048) DEFAULT NULL,
  `latest_referrer` varchar(2048) DEFAULT NULL,
  `latest_referrer_host` varchar(2048) DEFAULT NULL,
  `latest_search_keyword` varchar(2048) DEFAULT NULL,
  `latest_traffic_source_type` varchar(255) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`distinct_id`),
  KEY `utm_campaign` (`utm_campaign`),
  KEY `utm_source` (`utm_source`),
  KEY `utm_medium` (`utm_medium`),
  KEY `utm_term` (`utm_term`),
  KEY `utm_content` (`utm_content`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;""".format(project_name=project_name)
    table_user_sql = """CREATE TABLE `{project_name}_user` (
  `distinct_id` varchar(255) NOT NULL,
  `lib` varchar(255) NOT NULL,
  `map_id` varchar(255) NOT NULL,
  `original_id` varchar(255) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `all_user_profile` json DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`distinct_id`,`lib`,`map_id`,`original_id`),
  KEY `distinct_id` (`distinct_id`),
  KEY `map_id` (`map_id`),
  KEY `original_id` (`original_id`),
  KEY `distinct_id_lib` (`distinct_id`,`lib`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;""".format(project_name=project_name)
    table_properties_sql = """CREATE TABLE `{project_name}_properties` (
  `lib` varchar(255) NOT NULL,
  `remark` varchar(255) NOT NULL,
  `event` varchar(255) NOT NULL,
  `properties` json DEFAULT NULL,
  `properties_len` int(10) DEFAULT NULL,
  `created_at` int(10) DEFAULT NULL,
  `updated_at` int(10) DEFAULT NULL,
  `lastinsert_at` int(10) DEFAULT NULL,
  `total_count` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`lib`,`remark`,`event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;;""".format(project_name=project_name)
    result_table,count_table = do_tidb_exe(table_sql)
    print(project_name+'table表单已插入')
    result_device,count_device = do_tidb_exe(table_device_sql)
    print(project_name+'device表单已插入')
    result_user,count_user = do_tidb_exe(table_user_sql)
    print(project_name+'user表单已插入')
    result_properties,count_properties = do_tidb_exe(table_properties_sql)
    print(project_name+'properties表单已插入')
    if expired == None:
      expired_at = 2147483647
    else:
      expired_at = int(time.mktime(time.strptime(expired, "%Y-%m-%d")))
    timenow = int(time.time())
    insert_project_list = """insert project_list (`project_name`,`created_at`,`expired_at`) values ('{project_name}',{created_at},{expired_at})""".format(project_name=project_name,created_at=timenow,expired_at=expired_at)
    insert_project_list_result,insert_project_list_count = do_tidb_exe(insert_project_list)
    print(project_name+'project列表已插入')

def update_mobile_ad_src():
  with open(os.path.join(os.path.dirname(__file__).replace('component',''),'configs','mobile_ad_src_list.csv'),encoding='utf-8') as f:
    row = csv.reader(f, delimiter = ',')
    next(row)  #跳过首行
    total_count= 0
    for r in row:
      result,count =insert_mobile_ad_src(src=r[0],src_name=r[1],src_args=r[2],utm_source=r[3],utm_medium=r[4],utm_campaign=r[5],utm_content=r[6],utm_term=r[7])
      total_count = total_count+count
  print(str(total_count)+'条移动广告来源插入或更新完成（更新会记2次）')


if __name__ == "__main__":
    # create_project(project_name='test_app_with_date',expired='2020-01-01')
    create_project(project_name='test_app')
    update_mobile_ad_src()