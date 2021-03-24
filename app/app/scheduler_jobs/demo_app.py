# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import time
from app.component.db_func import insert_event
import json
from app.component.api_req import get_json_from_postjson
from app.component.db_op import do_tidb_select,do_tvcbook_select
from app.component.public_value import *
from app.scheduler_jobs.etl_model import insert_usergroup
import traceback
from app.configs.export import write_to_log
from app.component.api_req import get_json_from_api

 



def last_1500_email(args):
    date = args['date']
    days = args['days'] if 'days' in args and args['days'] else 1
    count = args['count'] if 'count' in args and args['count'] else 50
    timenow = int(time.time())
    stauts = 0
    index_id = 0
    job_id = args['job_id']
    try:
        start_day = get_display_day(start_day=date,calc=1-days)
        sql_find_user ="""select tvcbook.distinct_id,max(tvcbook.created_at) as max_c from tvcbook left join tvcbook_user on tvcbook.distinct_id=tvcbook_user.distinct_id where tvcbook.date>=DATE_SUB('{start_day}',INTERVAL 1 DAY) and date<=DATE_SUB('{end_day}',INTERVAL 1 DAY) and event = '$pageview' and tvcbook_user.original_id is not null and tvcbook_user.original_id != '' GROUP BY tvcbook.distinct_id order by max_c desc limit {count}""".format(start_day=start_day,end_day=date,count=count)
        users_result = do_tidb_select(sql=sql_find_user)
        # print(users_count)
        total_insert = 0
        all_data = {'data_list':[]}
        for user in users_result[0]:
            sql_email = """select email,nickname from yii2_user left join yii2_user_profile on yii2_user.id = yii2_user_profile.user_id where uid = '{uid}';""".format(uid=user[0])
            sql_email_result,sql_email_count = do_tvcbook_select(sql=sql_email)
            if sql_email_count>0 and sql_email_result[0][0] is not None and sql_email_result[0][0] !='' and total_insert<count:
                all_data['data_list'].append({'key':user[0],'enable':9,'json':{'email':sql_email_result[0][0],'nickname':sql_email_result[0][1],'last_active_time':get_time_str(inttime=user[1])}})
                total_insert = total_insert + 1
                # print(total_insert,user[0],sql_email_result[0][0],sql_email_result[0][1],get_time_str(inttime=user[1]))
        # print(all_data)
        status,index_id = insert_usergroup(project='tvcbook',group_id=4301,data=all_data,init_time=timenow,list_desc=date,jobs_id=job_id)
        return status,index_id

    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='tvcbook', defname='last_1500_email', result=error)
        return 20,index_id

def test_oo(keys):
    return keys 

def home_ref(data=None):
    # ref_data = json.loads(get_json_from_api(url='https://api.tvcbook.com/r/top?r=1&sort=recommend_desc&per-page=24&expand=credits_total,credits_list,is_verified,social'))
    ref_data = get_json_from_api(url='https://api.tvcbook.com/r/top?r=1&sort=recommend_desc&per-page=24&expand=credits_total,credits_list,is_verified,social')
    v = {'subject':'测试标题'}
    # print(ref_data['data']['data']['items'])
    # print(len(ref_data['data']['data']['items']))
    for r in range(len(ref_data['data']['data']['items'])):
        v['video_title_'+str(r+1)]=ref_data['data']['data']['items'][r]['title']
        v['video_cover_'+str(r+1)+'_img_url'] =  ref_data['data']['data']['items'][r]['cover_url']
        v['vid_'+str(r+1)+'_url'] =  ref_data['data']['data']['items'][r]['video_id']
        v['vid_'+str(r+1)+'_code'] =  ref_data['data']['data']['items'][r]['code']
        v['user_id_'+str(r+1)] =  ref_data['data']['data']['items'][r]['credits_list'][0]['user_id']
        v['auther_title_'+str(r+1)+'_url'] =  ref_data['data']['data']['items'][r]['credits_list'][0]['avatar']
        v['user_id_'+str(r+1)+'_code'] =  'null'
        v['author_name_'+str(r+1)] =  ref_data['data']['data']['items'][r]['credits_list'][0]['creator_name']
    return v

if __name__ == "__main__":
    # last_1500_email()
    # print(get_display_day(start_day='2020-10-20',calc=-2))
    print(home_ref(data=None))