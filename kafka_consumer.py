# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
from component.api import insert_data
import json
from component.kafka_op import get_message_from_kafka
import sys
import traceback
import multiprocessing
from configs.export import write_to_log
sys.path.append("./")
sys.setrecursionlimit(10000000)


def use_kafka():
    results = get_message_from_kafka()
    p = multiprocessing.Pool(processes=8)
    for result in results:
        # do_insert(msg=result)
        try:
            p.apply_async(func=do_insert, kwds={
                "msg": result})
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='kafka_consumer',
                     defname='use_kafka', result=error)
    p.close()
    p.join()


def do_insert(msg):
    try:
        data = json.loads(msg.value.decode('utf-8'))['data']
        offset = msg.offset
        print(offset)
        # print(data['project'])
        insert_data(project=data['project'], data_decode=data['data_decode'], User_Agent=data['User_Agent'], Host=data['Host'], Connection=data['Connection'], Pragma=data['Pragma'], Cache_Control=data['Cache_Control'], Accept=data['Accept'], Accept_Encoding=data['Accept_Encoding'], Accept_Language=data['Accept_Language'], ip=data['ip'], ip_city=data['ip_city'],
                    ip_asn=data['ip_asn'], url=data['url'], referrer=data['referrer'], remark=data['remark'], ua_platform=data['ua_platform'], ua_browser=data['ua_browser'], ua_version=data['ua_version'], ua_language=data['ua_language'], ip_is_good=data['ip_is_good'], ip_asn_is_good=data['ip_asn_is_good'], created_at=data['created_at'], updated_at=data['updated_at'], use_kafka=False)
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='kafka_consumer',
                     defname='do_insert', result=error)


if __name__ == "__main__":
    use_kafka()
