# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai

# 该程序用来把老版本鬼策升级到支持用户分群的新版本。仅老用户在升级2020年10月15日之后的版本使用。如果新装就是2020年10月15日后的版本，无需运行此程序。
import sys
sys.path.append("./")
from component.db_func import select_all_project
from component.db_op import do_tidb_exe,do_tidb_select

#!用于最早期版本升级到20210406版本。

def update():
    sql_alter_update = """ALTER TABLE `project_list` ADD COLUMN `enable_scheduler` int(4) NULL DEFAULT 1 COMMENT '是否启动定时器支持' AFTER `user_count`;"""
    do_tidb_exe(sql_alter_update)
    sql_access_control_threshold_sum = """ALTER TABLE `project_list` 
ADD COLUMN `access_control_threshold_sum` int(11) NULL COMMENT '接入控制的全局缺省值' AFTER `enable_scheduler`;"""
    do_tidb_exe(sql=sql_access_control_threshold_sum)
    sql_access_control_threshold_event = """ALTER TABLE `project_list` 
ADD COLUMN `access_control_threshold_event` int(11) NULL COMMENT '接入控制的单项缺省值' AFTER `access_control_threshold_sum`;"""
    do_tidb_exe(sql=sql_access_control_threshold_event)
    print('project_list加字段完成')
    print('项目表已更新')
    sql_insert_status_code = """CREATE TABLE IF NOT EXISTS `status_code` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
    `desc` varchar(255) DEFAULT NULL COMMENT '含义',
    `p_id` int(11) DEFAULT NULL COMMENT '父id',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;"""
    do_tidb_exe(sql_insert_status_code)
    print('状态码表创建完')
    status_codes = ["INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (1, '分群列表状态', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (2, '创建列表开始', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (3, '分群信息写入中', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (4, '分群写入完成并包含错误', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (5, '分群写入完成', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (6, '分群写入失败', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (7, '生效策略', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (8, '自动', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (9, '手动', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (10, '禁用', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (11, '进入分群队列', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (12, '优先级', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (13, '普通', 12);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (14, '高', 12);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (15, '最高', 12);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (16, '已添加任务队列', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (17, '任务已被选取', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (18, '任务方法加载完', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (19, '任务执行成功', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (20, '分群ETL失败', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (21, '任务执行失败', 1);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (22, '通知方式', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (23, 'email', 22);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (24, '自动分群但不自动应用模板', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (25, '推送状态', 0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (26, '推送成功', 25);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (27, '推送失败', 25);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (28, '自动分群自动应用模板但不自动发送', 7);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (29,'微信公众号',22);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (30,'黑名单修改原因',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (31,'用户自助退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (32,'用户自助取消退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (33,'客服投诉退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (34,'客服取消退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (35,'接收地址错误',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (36,'接收地址判定为垃圾邮件',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (37,'导入第三方黑名单',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (38,'第三方白名单覆盖',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (39,'黑名单状态',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (40,'全部禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (41,'推广类禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (42,'通知类禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (43,'拟加入黑名单待确认（如等待运营确认）',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (44,'已解禁',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (45,'不允许解禁',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (46,'误判人工解除',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (47,'客服主观退订',30);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (48,'消息级别',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (49,'紧急广播（忽略一切退订限制）',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (50,'IM',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (51,'通知',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (52,'运营',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (53,'推广',48);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (54,'运营类禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (55,'接入控制状态',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (56,'取消黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (57,'临时黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (58,'永久黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (59,'接入控制类型',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (60,'ip',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (61,'ip_group',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (62,'distinct_id',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (63,'add_on_key',59);"]
    for code in status_codes:
        do_tidb_exe(code)
    print('状态码添加完毕')
    blacklist_sql_1="""CREATE TABLE `recall_blacklist` (
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
    blacklist_sql_2="""CREATE TABLE `recall_blacklist_history` (
  `rbid` int(11) NOT NULL COMMENT 'recall_blacklist的id',
  `checker` varchar(255) DEFAULT NULL COMMENT '查询者的名字',
  `result_status_id` int(11) DEFAULT NULL COMMENT '返回的status_code里pid是39的状态',
  `result_reason_id` int(11) DEFAULT NULL COMMENT '返回的status_code里pid是30的理由',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  KEY `rbid` (`rbid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    blacklist_sql_3="""CREATE TABLE `recall_blacklist_reason` (
  `rbid` int(11) NOT NULL COMMENT 'recall_blacklist的id',
  `reason_id` int(11) DEFAULT NULL COMMENT 'status_code里pid是30的状态',
  `reason_owner` varchar(255) DEFAULT NULL COMMENT '修改人',
  `reason_comment` varchar(255) DEFAULT NULL COMMENT '修改的备注',
  `final_status_id` int(11) DEFAULT NULL COMMENT '最后写入recall_blacklist的status_code里pid是39的状态',
  `created_at` varchar(255) DEFAULT NULL COMMENT '创建的时间',
  KEY `rbid` (`rbid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    do_tidb_exe(blacklist_sql_1)
    print('黑名单表添加完毕')
    do_tidb_exe(blacklist_sql_2)
    print('黑名单查询历史表添加完毕')
    do_tidb_exe(blacklist_sql_3)
    print('黑名单修改历史表添加完毕')
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
    project_list,project_count = select_all_project()
    for project in project_list:
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project[0])
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project[0])
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project[0]) 
        do_tidb_exe(insert_plan)
        print(project[0]+'的分群附加表表已添加完')
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;""".format(project_name=project[0])
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1001;""".format(project_name=project[0])
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1001;""".format(project_name=project[0])
        do_tidb_exe(insert_noti_temple)
        print(project[0]+'的消息附加表表已添加完')

def update_properties():
    sql = """select project_name from project_list"""
    result = do_tidb_select(sql=sql)
    for project in result[0]:
        sql2="""ALTER TABLE `events`.`{project}_properties` 
ADD COLUMN `access_control_threshold` int(10) NULL AFTER `total_count`;""".format(project=project[0])
        do_tidb_exe(sql=sql2)
    print('properities加字段完成')

def create_new_talbe():
    sql = """CREATE TABLE `access_control` (
    `project` varchar(255) NOT NULL COMMENT '项目名',
    `key` varchar(255) NOT NULL COMMENT 'status_code里pid=56',
    `type` int(4) NOT NULL COMMENT 'key类型',
    `event` varchar(255) NOT NULL COMMENT 'event类型',
    `status` int(4) DEFAULT NULL COMMENT 'status_code里pid=59',
    `date` date NOT NULL COMMENT '日期',
    `hour` int(4) NOT NULL COMMENT '小时',
    `pv` int(10) DEFAULT NULL COMMENT '事件量',
    `updated_at` int(10) DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`project`,`key`,`type`,`event`,`date`,`hour`) /*T![clustered_index] NONCLUSTERED */,
    KEY `hour_key` (`date`,`hour`,`key`),
    KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"""
    do_tidb_exe(sql=sql)

if __name__ == "__main__":
    update()
    update_properties()
    create_new_talbe()