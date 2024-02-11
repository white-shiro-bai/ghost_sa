# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.db_op import do_tidb_exe,do_tidb_select
from component.db_func import insert_mobile_ad_src
from configs import admin
import time
import csv
import os

def update_table_history(project_name):
    #升级user表支持多个设备绑定。2019-12-11
    sql="""CREATE TABLE IF NOT EXISTS `{project_name}_user2` (
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
    result=do_tidb_exe(sql)
    print(result)


def create_project(project_name,expired=None):
    #创建新项目，project_name是项目名，expired是过期时间，字串输入 2019-01-01 格式
    create_project_list = """CREATE TABLE IF NOT EXISTS `project_list` (
    `project_name` varchar(255) DEFAULT NULL COMMENT '项目名称',
    `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
    `expired_at` int(11) DEFAULT NULL COMMENT '过期时间',
    `event_count` bigint(20) DEFAULT NULL COMMENT '事件量',
    `device_count` bigint(20) DEFAULT NULL COMMENT '设备数',
    `user_count` bigint(20) DEFAULT NULL COMMENT '用户数',
    `enable_scheduler` int(4) DEFAULT 1 COMMENT '是否启动定时器支持',
    `access_control_threshold_sum` int(11) DEFAULT NULL COMMENT '接入控制的全局缺省值',
    `access_control_threshold_event` int(11) DEFAULT NULL COMMENT '接入控制的单项缺省值'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""

    create_shortcut = """CREATE TABLE IF NOT EXISTS `shortcut` (
`project` varchar(255) DEFAULT NULL COMMENT '项目名',
`short_url` varchar(255) DEFAULT NULL COMMENT '短链地址',
`short_url_dec` bigint(18) NOT NULL DEFAULT '0' COMMENT '短链地址十进制表达。正数是自身创建的。0是网站外带进来的需要参与排序的。-1是手动创建或修改不参与排序的。',
`long_url` varchar(768) DEFAULT NULL COMMENT '长链地址',
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
KEY `long_url` (`long_url`),
KEY `short_url_dec`(`short_url_dec`),
UNIQUE KEY `short_url` (`short_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    create_shortcut_history = """CREATE TABLE IF NOT EXISTS `shortcut_history` (
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
    KEY `created_at` (`created_at`),
    KEY `short_url` (`short_url`),
    KEY `short_url_result` (`short_url`,`result`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""

    create_mobile_ad_src ="""CREATE TABLE if not EXISTS `mobile_ad_src` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    create_mobile_ad_list ="""CREATE TABLE if not EXISTS `mobile_ad_list` (
    `project` varchar(255) DEFAULT NULL COMMENT '项目名',
    `url` varchar(768) NOT NULL COMMENT '监测地址',
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
    created_shortcut_read="""CREATE TABLE if not EXISTS `shortcut_read` (
    `short_url` varchar(255) NOT NULL COMMENT '短链地址',
    `ip` varchar(20) DEFAULT NULL COMMENT 'ip',
    `created_at` int(11) DEFAULT NULL COMMENT '时间',
    `user_agent` text DEFAULT NULL COMMENT 'ua',
    `accept_language` text DEFAULT NULL COMMENT '语言',
    `ua_platform` varchar(255) DEFAULT NULL COMMENT '平台',
    `ua_browser` varchar(255) DEFAULT NULL COMMENT '浏览器',
    `ua_version` varchar(255) DEFAULT NULL COMMENT '版本号',
    `ua_language` varchar(255) DEFAULT NULL COMMENT '语言',
    `referrer` text DEFAULT NULL COMMENT '页面',
    KEY `short_url` (`short_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    blacklist_sql_1="""CREATE TABLE IF NOT EXISTS `recall_blacklist` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `project` varchar(255) NOT NULL COMMENT '项目名',
    `distinct_id` varchar(255) DEFAULT NULL,
    `key` varchar(255) NOT NULL COMMENT '渠道key',
    `type_id` int(11) NOT NULL COMMENT '渠道类型',
    `reason_id` int(11) DEFAULT NULL COMMENT '原因id',
    `owner` varchar(255) DEFAULT NULL COMMENT '第一次操作所属人',
    `latest_owner` varchar(255) DEFAULT NULL COMMENT '最后一次操作所属人',
    `status` int(11) DEFAULT NULL COMMENT '状态',
    `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
    `updated_at` int(11) DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `anti_copy` (`key`,`type_id`,`project`),
    KEY `check_blacklist` (`status`,`key`,`type_id`,`project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;"""
    blacklist_sql_2="""CREATE TABLE IF NOT EXISTS `recall_blacklist_history` (
    `rbid` int(11) NOT NULL COMMENT 'recall_blacklist的id',
    `checker` varchar(255) DEFAULT NULL COMMENT '查询者的名字',
    `result_status_id` int(11) DEFAULT NULL COMMENT '返回的status_code里pid是39的状态',
    `result_reason_id` int(11) DEFAULT NULL COMMENT '返回的status_code里pid是30的理由',
    `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
    KEY `rbid` (`rbid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    blacklist_sql_3="""CREATE TABLE IF NOT EXISTS `recall_blacklist_reason` (
    `rbid` int(11) NOT NULL COMMENT 'recall_blacklist的id',
    `reason_id` int(11) DEFAULT NULL COMMENT 'status_code里pid是30的状态',
    `reason_owner` varchar(255) DEFAULT NULL COMMENT '修改人',
    `reason_comment` varchar(255) DEFAULT NULL COMMENT '修改的备注',
    `final_status_id` int(11) DEFAULT NULL COMMENT '最后写入recall_blacklist的status_code里pid是39的状态',
    `created_at` varchar(255) DEFAULT NULL COMMENT '创建的时间',
    KEY `rbid` (`rbid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    sql_access_control = """CREATE TABLE IF NOT EXISTS `access_control` (
    `project` varchar(255) NOT NULL COMMENT '项目名',
    `key` varchar(255) NOT NULL COMMENT 'status_code里pid=56',
    `type` int(4) NOT NULL COMMENT 'key类型',
    `event` varchar(255) NOT NULL COMMENT 'event类型',
    `status` int(4) DEFAULT NULL COMMENT 'status_code里pid=59',
    `date` date NOT NULL COMMENT '日期',
    `hour` int(4) NOT NULL COMMENT '小时',
    `pv` int(10) DEFAULT NULL COMMENT '事件量',
    `updated_at` int(10) DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`project`,`key`,`type`,`event`,`date`,`hour`),
    KEY `hour_key` (`date`,`hour`,`key`),
    KEY `key` (`key`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    do_tidb_exe(create_project_list)
    do_tidb_exe(create_shortcut)
    do_tidb_exe(create_shortcut_history)
    do_tidb_exe(create_mobile_ad_src)
    do_tidb_exe(create_mobile_ad_list)
    do_tidb_exe(created_shortcut_read)
    do_tidb_exe(blacklist_sql_1)
    do_tidb_exe(blacklist_sql_2)
    do_tidb_exe(blacklist_sql_3)
    do_tidb_exe(sql_access_control)
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
    `lib` varchar(200) DEFAULT NULL,
    `device_id` varchar(255) DEFAULT NULL,
    `manufacturer` varchar(200) DEFAULT NULL,
    `model` varchar(200) DEFAULT NULL,
    `os` varchar(200) DEFAULT NULL,
    `os_version` varchar(200) DEFAULT NULL,
    `ua_platform` varchar(200) DEFAULT NULL,
    `ua_browser` varchar(200) DEFAULT NULL,
    `ua_version` varchar(200) DEFAULT NULL,
    `ua_language` varchar(200) DEFAULT NULL,
    `screen_width` int(11) DEFAULT NULL,
    `screen_height` int(11) DEFAULT NULL,
    `network_type` varchar(32) DEFAULT NULL,
    `user_agent` varchar(768) DEFAULT NULL,
    `accept_language` varchar(255) DEFAULT NULL,
    `ip` varchar(255) DEFAULT NULL,
    `ip_city` json DEFAULT NULL,
    `ip_asn` json DEFAULT NULL,
    `wifi` varchar(20) DEFAULT NULL,
    `app_version` varchar(255) DEFAULT NULL,
    `carrier` varchar(255) DEFAULT NULL,
    `referrer` text DEFAULT NULL,
    `referrer_host` varchar(512) DEFAULT NULL,
    `bot_name` varchar(255) DEFAULT NULL,
    `browser` varchar(128) DEFAULT NULL,
    `browser_version` varchar(128) DEFAULT NULL,
    `is_login_id` varchar(32) DEFAULT NULL,
    `screen_orientation` varchar(64) DEFAULT NULL,
    `gps_latitude` decimal(11,7) DEFAULT NULL,
    `gps_longitude` decimal(11,7) DEFAULT NULL,
    `first_visit_time` datetime DEFAULT NULL,
    `first_referrer` text DEFAULT NULL,
    `first_referrer_host` varchar(512) DEFAULT NULL,
    `first_browser_language` varchar(128) DEFAULT NULL,
    `first_browser_charset` varchar(128) DEFAULT NULL,
    `first_search_keyword` varchar(768) DEFAULT NULL,
    `first_traffic_source_type` varchar(255) DEFAULT NULL,
    `utm_content` varchar(768) DEFAULT NULL,
    `utm_campaign` varchar(768) DEFAULT NULL,
    `utm_medium` varchar(768) DEFAULT NULL,
    `utm_term` varchar(768) DEFAULT NULL,
    `utm_source` varchar(768) DEFAULT NULL,
    `latest_utm_content` varchar(768) DEFAULT NULL,
    `latest_utm_campaign` varchar(768) DEFAULT NULL,
    `latest_utm_medium` varchar(768) DEFAULT NULL,
    `latest_utm_term` varchar(768) DEFAULT NULL,
    `latest_utm_source` varchar(768) DEFAULT NULL,
    `latest_referrer` text DEFAULT NULL,
    `latest_referrer_host` varchar(512) DEFAULT NULL,
    `latest_search_keyword` varchar(768) DEFAULT NULL,
    `latest_traffic_source_type` varchar(255) DEFAULT NULL,
    `created_at` int(11) DEFAULT NULL,
    `updated_at` int(11) DEFAULT NULL,
    PRIMARY KEY (`distinct_id`),
    KEY `utm_campaign` (`utm_campaign`),
    KEY `utm_source` (`utm_source`),
    KEY `utm_medium` (`utm_medium`),
    KEY `utm_term` (`utm_term`),
    KEY `utm_content` (`utm_content`),
    KEY `created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;""".format(project_name=project_name)
        table_user_sql = """CREATE TABLE `{project_name}_user` (
    `distinct_id` varchar(200) NOT NULL,
    `lib` varchar(127) NOT NULL,
    `map_id` varchar(200) NOT NULL,
    `original_id` varchar(200) NOT NULL,
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
    `access_control_threshold` int(10) DEFAULT NULL,
    PRIMARY KEY (`lib`,`remark`,`event`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;""".format(project_name=project_name)
        do_tidb_exe(table_sql)
        print(project_name+'table表单已插入')
        do_tidb_exe(table_device_sql)
        print(project_name+'device表单已插入')
        do_tidb_exe(table_user_sql)
        print(project_name+'user表单已插入')
        do_tidb_exe(table_properties_sql)
        print(project_name+'properties表单已插入')
        sql_insert_status_code = """CREATE TABLE IF NOT EXISTS `status_code` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
    `desc` varchar(255) DEFAULT NULL COMMENT '含义',
    `p_id` int(11) DEFAULT NULL COMMENT '父id',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;"""
        do_tidb_exe(sql_insert_status_code)
        print('状态码表创建完')
        status_codes = ["INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (1, '分群列表状态', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (2, '创建列表开始', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (3, '分群信息写入中', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (4, '分群写入完成并包含错误', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (5, '分群写入完成', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (6, '分群写入失败', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (7, '生效策略', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (8, '自动', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (9, '手动', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (10, '禁用', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (11, '进入分群队列', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (12, '优先级', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (13, '普通', 12);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (14, '高', 12);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (15, '最高', 12);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (16, '已添加任务队列', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (17, '任务已被选取', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (18, '任务方法加载完', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (19, '任务执行成功', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (20, '分群ETL失败', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (21, '任务执行失败', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (22, '通知方式', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (23, 'email', 22);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (24, '自动分群但不自动应用模板', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (25, '推送状态', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (26, '推送成功', 25);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (27, '推送失败', 25);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (28, '自动分群自动应用模板但不自动发送', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (29,'微信公众号',22);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (30,'黑名单修改原因',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (31,'用户自助退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (32,'用户自助取消退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (33,'客服投诉退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (34,'客服取消退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (35,'接收地址错误',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (36,'接收地址判定为垃圾邮件',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (37,'导入第三方黑名单',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (38,'第三方白名单覆盖',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (39,'黑名单状态',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (40,'全部禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (41,'推广类禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (42,'通知类禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (43,'拟加入黑名单待确认（如等待运营确认）',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (44,'已解禁',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (45,'不允许解禁',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (46,'误判人工解除',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (47,'客服主观退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (48,'消息级别',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (49,'紧急广播（忽略一切退订限制）',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (50,'IM',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (51,'通知',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (52,'运营',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (53,'推广',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (54,'运营类禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (55,'接入控制状态',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (56,'取消黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (57,'临时黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (58,'永久黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (59,'接入控制类型',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (60,'ip',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (61,'ip_group',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (62,'distinct_id',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (63,'add_on_key',59);","INSERT IGNORE INTO `status_code` VALUES (64, '配置文件状态', 0);","INSERT IGNORE INTO `status_code` VALUES (65, '配置生效', 64);","INSERT IGNORE INTO `status_code` VALUES (66, '升级下一个配置', 64);","INSERT IGNORE INTO `status_code` VALUES (67, '停留在此配置', 64);","INSERT IGNORE INTO `status_code` VALUES (68, '失效配置', 64);","INSERT IGNORE INTO `status_code` VALUES (69, '函数执行状态', 0);","INSERT IGNORE INTO `status_code` VALUES (70, '函数执行成功', 69);","INSERT IGNORE INTO `status_code` VALUES (71, '函数执行失败', 69);","INSERT IGNORE INTO `status_code` VALUES (72, '等待确认的配置', 64);","INSERT IGNORE INTO `status_code` VALUES (73, '灰度升级', 64);","INSERT IGNORE INTO `status_code` VALUES (74, 'referrer', 59);","INSERT IGNORE INTO `status_code` VALUES (75, '控制列表排除方向', 0);","INSERT IGNORE INTO `status_code` VALUES (76, '白名单', 75);","INSERT IGNORE INTO `status_code` VALUES (77, '黑名单', 75);","INSERT IGNORE INTO `status_code` VALUES (78, '永久取消黑名单', 55);","INSERT IGNORE INTO `status_code` VALUES (79, '请求频繁进入接入控制名单', 30);","INSERT IGNORE INTO `status_code` VALUES (80, 'ip_group_extend', 59);","INSERT IGNORE INTO `status_code` VALUES (81, 'umail', 22);","INSERT IGNORE INTO `status_code` VALUES (82, 'aliyun_sms', 22);","INSERT IGNORE INTO `status_code` VALUES (83, 'qcloud_sms', 22);"]
        for code in status_codes:
            do_tidb_exe(code)
        print('状态码添加完毕')
        sql_scheduler_jobs = """CREATE TABLE IF NOT EXISTS `scheduler_jobs` (
        `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '任务id',
        `project` varchar(255) DEFAULT NULL COMMENT '项目id',
        `group_id` int(11) DEFAULT NULL COMMENT 'group_plan的id',
        `list_index` int(11) DEFAULT NULL COMMENT 'group_index任务完成后，补充',
        `datetime` int(11) DEFAULT NULL COMMENT '执行的日期，即要执行的那个任务的时间（不是任务执行时间，是要执行的时间。如周三时执行周一的任务。也用来防止任务重复添加）',
        `data` json DEFAULT NULL COMMENT '其他附带的参数',
        `priority` int(4) DEFAULT NULL COMMENT '优先级',
        `status` int(4) DEFAULT NULL COMMENT '状态',
        `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
        `updated_at` int(11) DEFAULT NULL COMMENT '更新时间',
        PRIMARY KEY (`id`),
        UNIQUE KEY `ind_task` (`project`,`group_id`,`datetime`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;"""
        do_tidb_exe(sql_scheduler_jobs)
        print('任务计划表添加完毕')
        insert_data = """CREATE TABLE IF NOT EXISTS `{project_name}_usergroup_data` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `group_list_id` int(11) DEFAULT NULL COMMENT '分群列表id',
    `data_index` int(11) DEFAULT NULL COMMENT '最新一组数据的index_id',
    `data_key` varchar(255) DEFAULT NULL COMMENT '数据的唯一识别id',
    `data_json` json DEFAULT NULL COMMENT '数据包',
    `enable` int(11) DEFAULT NULL COMMENT '生效策略。参考status_code，p_id=7',
    `created_at` int(11) DEFAULT NULL,
    `updated_at` int(11) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `group_list_id` (`group_list_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project_name)
        do_tidb_exe(insert_data)
        insert_list = """CREATE TABLE IF NOT EXISTS `{project_name}_usergroup_list` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '分群列表id',
    `group_id` int(11) DEFAULT NULL COMMENT '分群id',
    `group_list_index` int(11) DEFAULT NULL COMMENT '分群列表顺位',
    `list_init_date` int(11) DEFAULT NULL COMMENT '触发时间',
    `list_desc` varchar(255) DEFAULT NULL COMMENT '清单所描述的',
    `jobs_id` int(4) DEFAULT NULL COMMENT 'scheduler_jbos的id',
    `item_count` int(11) DEFAULT NULL COMMENT '分组条目数',
    `status` int(4) DEFAULT NULL COMMENT '分群状态。参考status_code,p_id=1',
    `complete_at` int(11) DEFAULT NULL COMMENT '分群完成时间',
    `apply_temple_times` int(2) DEFAULT 0 COMMENT '被套用模板的次数',
    `created_at` int(11) DEFAULT NULL COMMENT '条目创建时间',
    `updated_at` int(11) DEFAULT NULL COMMENT '条目更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_key` (`group_id`,`group_list_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project_name)
        do_tidb_exe(insert_list)
        insert_plan = """CREATE TABLE IF NOT EXISTS `{project_name}_usergroup_plan` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '分群id',
    `group_title` varchar(255) DEFAULT NULL COMMENT '分群标题',
    `group_desc` varchar(255) DEFAULT NULL COMMENT '分群描述',
    `func` json DEFAULT NULL COMMENT '分群执行方法参考/scheduler_jobs/scheduler_job_creator.py',
    `latest_data_list_index` int(11) DEFAULT NULL COMMENT '最新一组数据的id',
    `repeatable` varchar(20) DEFAULT NULL COMMENT '定时器，分，时，日，月，周。不填的用*代替。跟crontab一个逻辑，不支持1-10的方式表达，多日的需要1,2,3,4,5,6,7,8这样的形式填',
    `priority` int(4) DEFAULT NULL COMMENT '任务执行优先级',
    `latest_data_time` int(11) DEFAULT NULL COMMENT '最新一组数据的完成时间',
    `repeat_times` int(11) DEFAULT 0 COMMENT '分群完成次数',
    `enable_policy` int(11) DEFAULT NULL COMMENT '生效策略。参考status_code，p_id=7',
    `latest_apply_temple_id` int(11) DEFAULT NULL COMMENT '最后一次执行的模板类型',
    `latest_apply_temple_time` int(11) DEFAULT NULL COMMENT '最后一次执行的模型时间',
    `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
    `updated_at` int(11) DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project_name) 
        do_tidb_exe(insert_plan)
        print(project_name+'的分群附加表表已添加完')
        do_tidb_exe(insert_list)
        insert_noti = """CREATE TABLE IF NOT EXISTS `{project_name}_noti` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `plan_id` int(11) DEFAULT NULL COMMENT '计划id',
    `list_id` int(11) DEFAULT NULL COMMENT '列表id',
    `data_id` int(11) DEFAULT NULL COMMENT '数据id',
    `temple_id` int(4) DEFAULT NULL COMMENT '模板id',
    `noti_group_id` int(11) DEFAULT NULL COMMENT '消息群组id',
    `distinct_id` varchar(512) DEFAULT NULL COMMENT '用户识别id',
    `priority` int(4) DEFAULT NULL COMMENT '优先级',
    `status` int(4) DEFAULT NULL COMMENT '状态',
    `owner` varchar(255) DEFAULT NULL COMMENT '添加人',
    `level` int(4) DEFAULT NULL COMMENT '消息级别',
    `type` int(4) DEFAULT NULL COMMENT '消息类型',
    `key` varchar(255) DEFAULT NULL COMMENT '消息接受方式key',
    `content` json DEFAULT NULL COMMENT '消息内容',
    `send_at` int(11) DEFAULT NULL COMMENT '计划发送时间',
    `recall_result` text DEFAULT NULL COMMENT '发送结果',
    `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
    `updated_at` int(11) DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `distinct_id` (`distinct_id`),
    KEY `send_plan` (`status`,`priority`,`send_at`),
    KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project_name)
        do_tidb_exe(insert_noti)
        insert_noti_group = """CREATE TABLE IF NOT EXISTS `{project_name}_noti_group` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `plan_id` int(11) DEFAULT NULL COMMENT '分群计划id',
    `list_id` int(11) DEFAULT NULL COMMENT '分群列表id',
    `data_id` int(11) DEFAULT NULL COMMENT '分群数据id',
    `temple_id` int(11) DEFAULT NULL COMMENT '应用模板id',
    `priority` int(4) DEFAULT NULL COMMENT '优先级id',
    `status` int(4) DEFAULT NULL COMMENT '状态id',
    `owner` varchar(255) DEFAULT NULL COMMENT '添加人',
    `send_at` int(11) DEFAULT NULL COMMENT '计划发送时间',
    `sent` int(11) DEFAULT NULL COMMENT '已发送数目',
    `total` int(11) DEFAULT NULL COMMENT '该计划总数目',
    `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
    `updated_at` int(11) DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1001;""".format(project_name=project_name)
        do_tidb_exe(insert_noti_group)
        insert_noti_temple = """CREATE TABLE IF NOT EXISTS `{project_name}_noti_temple` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) DEFAULT NULL COMMENT '模板名称',
    `temple_desc` varchar(255) DEFAULT NULL COMMENT '模板描述',
    `args` json DEFAULT NULL COMMENT '模板参数',
    `content` json DEFAULT NULL COMMENT '模板内容',
    `apply_times` int(11) DEFAULT 0 COMMENT '应用次数',
    `lastest_apply_time` int(11) DEFAULT NULL COMMENT '最后一次应用时间',
    `lastest_apply_list` int(11) DEFAULT NULL COMMENT '最后一次应用列表',
    `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
    `updated_at` int(11) DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1001;""".format(project_name=project_name)
        do_tidb_exe(insert_noti_temple)
        print(project_name+'的消息附加表表已添加完')
        if expired == None:
            expired_at = 2147483647
        else:
            expired_at = int(time.mktime(time.strptime(expired, "%Y-%m-%d")))
        timenow = int(time.time())
        insert_project_list = """insert project_list (`project_name`,`created_at`,`expired_at`) values ('{project_name}',{created_at},{expired_at})""".format(project_name=project_name,created_at=timenow,expired_at=expired_at)
        do_tidb_exe(insert_project_list)
        print(project_name+'project列表已插入')

def update_mobile_ad_src():
    with open(os.path.join(os.path.dirname(__file__).replace('component',''),'configs','mobile_ad_src_list.csv'),encoding='utf-8') as f:
        row = csv.reader(f, delimiter = ',')
        next(row)    #跳过首行
        total_count= 0
        for r in row:
            result,count =insert_mobile_ad_src(src=r[0],src_name=r[1],src_args=r[2],utm_source=r[3],utm_medium=r[4],utm_campaign=r[5],utm_content=r[6],utm_term=r[7])
            total_count = total_count+count
    print(str(total_count)+'条移动广告来源插入或更新完成（更新会记2次）')
    
def init_deduplication_key():
    sql_dedu ="""CREATE TABLE `deduplication_key` (
  `project` varchar(64) NOT NULL,
  `distinct_id` varchar(254) NOT NULL,
  `track_id` varchar(64) NOT NULL,
  `sdk_time13` bigint(17) NOT NULL,
  `created_at` TIMESTAMP,
  UNIQUE INDEX `nx`(`project`, `distinct_id`, `track_id`, `sdk_time13`)
) TTL = `created_at` + INTERVAL {minute} MINUTE TTL_ENABLE = 'ON';""".format(minute=admin.batch_send_max_window)
    if admin.batch_send_deduplication_mode in ('tidb6.5+','tidb6.4-','mysql'):
        req = do_tidb_exe(sql=sql_dedu,skip_mysql_code=1050)
        if req[0] == 'sql_err':
            print('去重表存在重复，如果没有变更admin.batch_send_deduplication_mode的去重模式，可以忽略此信息。如果变更过，请删掉去重表重新初始化。')
        else:
            print('去重表初始化成功')
    sql_event = """CREATE EVENT clean_deduplication_key
ON SCHEDULE EVERY 60 MINUTE 
ON COMPLETION PRESERVE 
DO DELETE `deduplication_key` where created_at <= current_timestamp - {minute} MINUTE;
    """.format(minute=admin.batch_send_max_window)
    sql_event_switch ='SET GLOBAL event_scheduler = ON;'
    if admin.batch_send_deduplication_mode in ('mysql'):
        req = do_tidb_exe(sql=sql_event)
        if req[0] != 'sql_err':
            print('mysql定时任务设置成功')
        else:
            print('mysql定时任务设置失败')
        
        req = do_tidb_exe(sql=sql_event_switch)
        if req[0] != 'sql_err':
            print('mysql定时器打开成功')
        else:
            print('mysql定时器打开失败')
        

if __name__ == "__main__":
        # create_project(project_name='test_app_with_date',expired='2020-01-01')
        create_project(project_name='test_me')
        update_mobile_ad_src()
        init_deduplication_key()