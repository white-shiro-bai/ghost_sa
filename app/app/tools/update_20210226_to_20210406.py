# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from app.component.db_op import do_tidb_select,do_tidb_exe

def update_properties():
    sql = """select project_name from project_list"""
    result = do_tidb_select(sql=sql)
    for project in result[0]:
        sql2="""ALTER TABLE `events`.`{project}_properties` 
ADD COLUMN `access_control_threshold` int(10) NULL AFTER `total_count`;""".format(project=project[0])
        do_tidb_exe(sql=sql2)
    print('properities加字段完成')


def update_project_list():
    sql = """ALTER TABLE `events`.`project_list` 
ADD COLUMN `access_control_threshold_sum` int(11) NULL COMMENT '接入控制的全局缺省值' AFTER `enable_scheduler`;"""
    do_tidb_exe(sql=sql)
    sql = """ALTER TABLE `events`.`project_list` 
ADD COLUMN `access_control_threshold_event` int(11) NULL COMMENT '接入控制的单项缺省值' AFTER `access_control_threshold_sum`;"""
    do_tidb_exe(sql=sql)
    print('project_list加字段完成')

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


def update_code():
    status_codes = ["INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (54,'运营类禁用',39);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (55,'接入控制状态',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (56,'取消黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (57,'临时黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (58,'永久黑名单',55);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (59,'接入控制类型',0);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (60,'ip',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (61,'ip_group',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (62,'distinct_id',59);","INSERT IGNORE INTO `status_code`(`id`, `desc`, `p_id`) VALUES (63,'add_on_key',59);"]
    for code in status_codes:
        do_tidb_exe(code)
    print('状态码添加完毕')

if __name__ == "__main__":
    update_properties()
    update_project_list()
    create_new_talbe()
    update_code()