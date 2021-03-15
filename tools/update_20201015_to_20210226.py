# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.db_func import select_all_project
from component.db_op import do_tidb_exe

#!用于之前升级过20201015版本的升级到20210226版本。

def update():
    status_codes = ["INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (29,'微信公众号',22);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (30,'黑名单修改原因',0);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (31,'用户自助退订',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (32,'用户自助取消退订',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (33,'客服投诉退订',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (34,'客服取消退订',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (35,'接收地址错误',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (36,'接收地址判定为垃圾邮件',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (37,'导入第三方黑名单',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (38,'第三方白名单覆盖',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (39,'黑名单状态',0);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (40,'全部禁用',39);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (41,'推广类禁用',39);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (42,'通知类禁用',39);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (43,'拟加入黑名单待确认（如等待运营确认）',39);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (44,'已解禁',39);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (45,'不允许解禁',39);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (46,'误判人工解除',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (47,'客服主观退订',30);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (48,'消息级别',0);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (49,'紧急广播（忽略一切退订限制）',48);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (50,'IM',48);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (51,'通知',48);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (52,'运营',48);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (53,'推广',48);","INSERT IGNORE INTO `events`.`status_code`(`id`, `desc`, `p_id`) VALUES (54,'运营类禁用',39);"]
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
    project_list,project_count = select_all_project()
    for project in project_list:
        sql1="""ALTER TABLE `events`.`{project_name}_noti` 
        ADD COLUMN `key` varchar(255) NULL COMMENT '消息接受方式key' AFTER `type`;
        """.format(project_name=project[0])
        do_tidb_exe(sql1)
        sql2="""ALTER TABLE `events`.`{project_name}_noti` 
        ADD INDEX `key`(`key`) USING BTREE;""".format(project_name=project[0])
        do_tidb_exe(sql2)
        sql3="""ALTER TABLE `events`.`{project_name}_noti` 
ADD COLUMN `level` int(4) NULL COMMENT '消息级别' AFTER `owner`;""".format(project_name=project[0])
        do_tidb_exe(sql3)
        print(project[0],'表升级完成')

if __name__ == "__main__":
    update()