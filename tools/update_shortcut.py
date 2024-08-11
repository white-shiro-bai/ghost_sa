# -*- coding: utf-8 -*-
#
#Date: 2023-05-27 15:03:45
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2023-05-28 15:15:49
#FilePath: \ghost_sa_github_cgq\tools\update_shortcut.py
#
import sys
sys.path.append('./')
from component.db_op import do_tidb_exe,do_tidb_select
from component.url_tools import is62hex
from component.db_func import update_shortdec
from component.base62 import Base62
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED

base62 = Base62()

def update_shortcut_table(import_list):
    #this function is compatible with  tidb since version 3.0.3
    create_temp_table_sql = """CREATE TABLE `shortcut_new` (
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
    duplicate_shortcut_date = """INSERT INTO shortcut_new SELECT
`project`,
`short_url`,
0 AS `short_url_dec`,
`long_url`,
`expired_at`,
`created_at`,
`src`,
`src_short_url`,
`submitter`,
`utm_source`,
`utm_medium`,
`utm_campaign`,
`utm_content`,
`utm_term` 
FROM
shortcut 
GROUP BY
`project`,
`short_url`,
`short_url_dec`,
`long_url`,
`expired_at`,
`created_at`,
`src`,
`src_short_url`,
`submitter`,
`utm_source`,
`utm_medium`,
`utm_campaign`,
`utm_content`,
`utm_term`;"""
    disable_oldversion = """RENAME TABLE shortcut TO shortcut_backup;"""
    enable_newversion = """RENAME TABLE shortcut_new TO shortcut;"""
    result = do_tidb_exe(sql=create_temp_table_sql,retrycount=0)
    print("创建shortcut_new",result[0])
    result = do_tidb_exe(sql=duplicate_shortcut_date,retrycount=0)
    print("从原shortcut复制数据",result[1])
    result = do_tidb_exe(sql=disable_oldversion,retrycount=0)
    print("将原表改名shortcut_old",result[1])
    result = do_tidb_exe(sql=enable_newversion,retrycount=0)
    print("启用新表")
    src_list = ','.join(import_list)
    select_manual_history = """select short_url from shortcut where src in ({src_list})""".format(src_list=src_list)
    short_url_list = do_tidb_select(sql=select_manual_history)[0]
    global success_count,fail_count
    success_count = 0
    fail_count = 0
    tasklist = []
    print('根据',src_list,'找到需要转换的自主shorturl共',len(short_url_list))
    with ThreadPoolExecutor(max_workers=5) as worker:
        for short_url in short_url_list:
            tasklist.append(worker.submit(update_history,short_url[0]))
        wait(tasklist, return_when=ALL_COMPLETED)
    print('根据',src_list,'找到需要转换的自主shorturl共',len(short_url_list))
    print('已完成历史自主key的10进制转换其中成功：',success_count,'，失败：',fail_count)
    
def update_history(short_url):
    global success_count,fail_count
    result62 = is62hex(text=short_url)
    if result62[0] == 0:
        update_shortdec(short_url=short_url,short_url_dec=-1)
        print(short_url,'无法转换为10进制，因为包含',result62[1],'。认为这是人工编写的，所以short_url_dec讲标记为-1。')
        fail_count += 1
    elif result62[0] == 1:  # if the text is valid, convert it to 10-base and save it.
        dec = base62.decode_62to10(str62=short_url)
        update_shortdec(short_url=short_url,short_url_dec=dec)
        # print(short_url,'已被转换为',dec)
        success_count += 1
        if success_count%200 == 0:
            print('已完成转换',success_count)


if __name__ == "__main__":
    import_list = ['"import"','"importer"','"sensors"'] #用来定义哪些创建的源是需要转换为10进制的。默认转换导入的和从神策迁入的
    update_shortcut_table(import_list=import_list)