# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
from component.api import insert_data,insert_installation_track,insert_shortcut_history,insert_shortcut_read
import json
from component.kafka_op import get_message_from_kafka
import sys
import traceback
# import multiprocessing
from configs.export import write_to_log
sys.path.append("./")
sys.setrecursionlimit(10000000)
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from configs import admin
if admin.access_control_commit_mode =='kafka_consumer':
    from component.access_control import access_control
    ac_kafka_consumer = access_control()
if admin.batch_send_deduplication_mode == 'consumer':
    from component.batch_send import batch_cache
    # from apscheduler.schedulers.background import BackgroundScheduler
    # batch_send_scheduler = BackgroundScheduler()
    # batch_send_scheduler.add_job(batch_cache.clean_expired, 'interval', seconds=admin.batch_send_max_memory_gap)
    # batch_send_scheduler.start()
import time



def use_kafka():
    results = get_message_from_kafka()
    # for result in results:
    #     do_insert(result)
    with ThreadPoolExecutor(max_workers=2) as worker:
        # global batch_cache
        for result in results:
            time.sleep(0.01)
            worker.submit(do_insert,result)

def do_insert(msg):
    # global batch_cache
    try:
        group= json.loads(msg.value.decode('utf-8'))['group'] if "group" in json.loads(msg.value.decode('utf-8')) else None
        data = json.loads(msg.value.decode('utf-8'))['data']
        data['data_decode']['kafka_offset'] = msg.offset
        if group == 'event_track':
            req = 'go'
            if admin.batch_send_deduplication_mode == 'consumer':
                # if data['data_decode']['_track_id'] and data['data_decode']['_track_id'] != 0 and data['data_decode']['_track_id'] !='' and data['data_decode']['_track_id'] !='0' and data['data_decode']['time'] and data['data_decode']['time'] !=0:
                req = batch_cache.query(project=data['project'],distinct_id=data['data_decode']['distinct_id'],track_id=data['data_decode']['_track_id'],time13=data['data_decode']['time'],source='consumer')
            if req == 'skip':
                print(req,admin.batch_send_deduplication_insert,admin.batch_send_deduplication_mode)
            if admin.batch_send_deduplication_mode != 'consumer' or req == 'go':
                insert_data(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'], Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'], Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark=data['remark'], ua_platform=data['ua_platform'], ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'], ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
                if admin.access_control_commit_mode =='kafka_consumer':
                    ac_kafka_consumer.traffic(project=data['project'],event=data['data_decode']['event'] if 'event' in data['data_decode'] else None,ip_commit=data['ip'],distinct_id_commit=data['data_decode']['distinct_id'],add_on_key_commit=data['data_decode']['properties'][admin.access_control_add_on_key] if admin.access_control_add_on_key in data['data_decode']['properties'] else None)
            elif req == 'skip' and admin.batch_send_deduplication_insert == 'remark':
                print('remark')
                insert_data(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'], Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'], Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark='du-'+data['remark'], ua_platform=data['ua_platform'], ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'], ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
            else:
                print('remark')
                insert_data(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'], Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'], Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark='missrule-'+data['remark'], ua_platform=data['ua_platform'], ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'], ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
                
        elif group == 'installation_track':
            insert_installation_track(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'], Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'], Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                    ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark=data['remark'], ua_platform=data['ua_platform'], ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'], ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
        elif group == 'shortcut_history':
            insert_shortcut_history(short_url=data['short_url'],result=data['status'],cost_time=data['time2'],ip=data['ip'],user_agent=data['user_agent'],accept_language=data['accept_language'],ua_platform=data['ua_platform'],ua_browser=data['ua_browser'],ua_version=data['ua_version'],ua_language=data['ua_language'],created_at=data['created_at'])
        elif group == 'shortcut_read':
            insert_shortcut_read(short_url=data['short_url'],ip=data['ip'],user_agent=data['user_agent'],accept_language=data['accept_language'],ua_platform=data['ua_platform'],ua_browser=data['ua_browser'],ua_version=data['ua_version'],ua_language=data['ua_language'],referrer=data['referrer'],created_at=data['created_at'])
        else:
            insert_data(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'], Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'], Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                    ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark=data['remark'], ua_platform=data['ua_platform'], ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'], ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='kafka_consumer',
                     defname='do_insert', result=error)


if __name__ == "__main__":

    use_kafka()