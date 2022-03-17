# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.db_func import create_user_profile,select_user_profile,update_user_profile
import json
import pprint
import random
from configs.export import write_to_log

class profile_control:
    def __init__(self,project,remark=None,owner=None):
        self.project = project
        self.remark = remark
        self.owner = owner
    
    def create(self,desc):
        #It is used for creating a profile include first time and others.
        result = create_user_profile(project=self.project,desc=desc,profile=self.profile,remark=self.remark,owner=self.owner)
        return result[2],70

    def update(self,profile_id,desc,gray_percent,update_now=None):
        #It is used for creating a profile and choose whether to start gray release.
        result = create_user_profile(project=self.project,desc=desc,profile=self.profile,remark=self.remark,owner=self.owner,gray_percent=gray_percent)
        if result[1]>0:
            pprint.pprint(self.show(profile_id=result[2]))
            loop_check = self.loop_inspection()
            if loop_check['loops_count'] > 0:
                return '存在循环引用'+str(loop_check['loops_list']),71
            else:
                update_now = input('确认开始灰度更新上述配置输入"yes"<-全小写:') if not update_now else update_now
                if update_now == 'yes':
                    result_update = update_user_profile(project=self.project,status=73,profile_id=result[2],desc='设为73')
                    result_update = update_user_profile(project=self.project,status=66,profile_id=profile_id,next_id=result[2],desc='设为66')
                    print('当前生效配置，如果有灰度可能显示新配置也可能显示旧配置')
                    print(self.my_profile())
                    return result[2],70
                else:
                    return '配置插入成功，没有确认更新，后续请手工更新或生效',71
        else:
            return '配置插入失败，请检查',71


    def enable(self,profile_id,update_now=None):
        # Enable a profile_id and ensure it was the only one which should be 
        loop_check = self.loop_inspection()
        if loop_check['loops_count'] > 0:
            return '存在循环引用'+str(loop_check['loops_list']),71
        else:
            previous_id = None
            org_info = self.show(limit=1,next_id=profile_id)
            if len(org_info.keys()) == 1:
                previous_id = org_info[list(org_info.keys())[0]]['profile_id']
            self.show(limit=3,status=[72,66,65,73])
            if len(self.all_profile_list) == 1 and profile_id in self.all_profile_list.keys():
                #initialize first profile.
                update_user_profile(project=self.project,status=65,profile_id=profile_id,desc='唯一配置生效65')
                print('当前生效配置')
                print(self.my_profile())
                return '初始化配置文件成功',70
            elif len(self.all_profile_list) == 2 and profile_id in self.all_profile_list.keys() and self.all_profile_list[profile_id]['status'] in [72,73] :
                #enable a gray release profile or a pending profile.
                if previous_id and previous_id in self.all_profile_list.keys():
                    for p_id in self.all_profile_list.keys():
                        if p_id == profile_id:
                            update_user_profile(project=self.project,status=65,profile_id=profile_id,desc='标准生效65')
                        elif p_id < profile_id and p_id == previous_id:
                            update_user_profile(project=self.project,status=68,profile_id=p_id,next_id=profile_id,desc='生效新配置后关闭68')
                        # elif p_id < profile_id and p_id != previous_id:
                        #     if self.all_profile_list[p_id]['status'] == 65 and self.all_profile_list[p_id]['next_id'] :
                        #         update_user_profile(project=self.project,status=66,profile_id=p_id)
                    print('当前生效配置')
                    print(self.my_profile())
                    return '已强制将{p_id}升级为{profile_id}'.format(p_id=str(p_id),profile_id=str(profile_id)),70
                elif previous_id and previous_id not in self.all_profile_list.keys():
                    if org_info[list(org_info.keys())[0]]['status'] == 65:
                        update_user_profile(project=self.project,status=65,profile_id=profile_id,desc='非标准生效65')
                        update_user_profile(project=self.project,status=68,profile_id=previous_id,desc='非标生效后关闭68')
                        return '已强制将{p_id}升级为{profile_id}'.format(p_id=str(previous_id),profile_id=str(profile_id)),70
                elif not previous_id:
                    # update_now = input('确认开始灰度更新上述配置输入"yes"<-全小写:') if not update_now else update_now
                    update_now = input('存在一个未指明的可替换配置，替换有风险，执行请输入"yes"<-全小写:')
                    if update_now == 'yes':
                        for p_id in self.all_profile_list.keys():
                            if p_id == profile_id:
                                update_user_profile(project=self.project,status=65,profile_id=profile_id,desc='未指明来源生效65')
                            elif p_id < profile_id:
                                update_user_profile(project=self.project,status=68,profile_id=p_id,next_id=profile_id,desc='未指明来源关闭68')
                        return '已强制将{p_id}升级为{profile_id}'.format(p_id=str(previous_id),profile_id=str(profile_id)),70
            elif len(self.all_profile_list) == 3:
                # there are some conflicting profile
                print('当前生效配置')
                print(self.my_profile())
                return '存在多个可替换配置，需要人工检查',71
            elif len(self.all_profile_list) == 0:
                # wrong profile id.
                return '找不到对应的配置文件',71
            else:
                return '没有对应任何一种情况，需要检查程序',71
            print(self.all_profile_list)


    def rollback(self,profile_id,target_profile_id=None,update_now=None):
        # rollback to previous profile (it must be assigned target profile id and target profile id must be less then profile id.
        # it will check previous profile if there is not any target profile id.It can only work on conditions in there is only one previous profile id.
        # Nomatter how much gray_percent provided,rollback will enforce be 100.)
        loop_check = self.loop_inspection()
        if loop_check['loops_count'] > 0:
            return '存在循环引用'+str(loop_check['loops_list']),71
        else:
            if not target_profile_id:
                org_profile_info = self.show(limit=2,next_id=profile_id)
                target_profile_id = list(org_profile_info.keys())[0] if len(org_profile_info.keys())==1 else None
            if target_profile_id and target_profile_id < profile_id:
                pprint.pprint(self.show(limit=1,profile_id=target_profile_id))
                update_now = input('确认降级到上述目标输入"yes"<-全小写:') if not update_now else update_now
                if update_now == 'yes':
                    result_update = update_user_profile(project=self.project,status=65,profile_id=target_profile_id,next_id=target_profile_id,desc='回滚生效65并设为最终') #profile_id = next_id means set next_id as null.
                    result_update = update_user_profile(project=self.project,status=68,profile_id=profile_id,desc='回滚关闭68')
                    print('当前生效配置')
                    pprint.pprint(self.my_profile())
                    return result_update[1],70
                else:
                    '确认指令不正确，未进行降级',71
            else:
                return '降级目标id不存在或降级目标id目标高于降级id或回滚id为合并后配置需要人工判断',71

                
    def disable(self,profile_id):
        #disable before enable.It is used for unusable profile such as created by mislead.
        loop_check = self.loop_inspection()
        if loop_check['loops_count'] > 0:
            return '存在循环引用'+str(loop_check['loops_list']),71
        else:
            self.show(limit=3,status=[65,66,73])
            if len(self.all_profile_list) == 0:
                return '存在循环引用'+str(loop_check['loops_list']),71
            else:
                profile_info = self.show(limit=1,profile_id=profile_id)
                if profile_id in profile_info:
                    if profile_info[profile_id]['status'] == 72:
                        result_update = update_user_profile(project=self.project,status=68,profile_id=profile_id,desc='未生效直接关闭68')
                        return '禁用成功',70
                    elif profile_info[profile_id]['status'] in [65,66,73]:
                        return '生效中的配置无法直接禁用，请使用回滚功能',71
                    elif profile_info[profile_id]['status'] == 68:
                        return '已经是失效配置',71
                    else:
                        return '其他无法关闭的配置，需要人工检查',71
                else:
                    return '该配置文件不存在',71

    def lock_version(self,profile_id):
        #set profile at lock statement to prevent client use new profile.It  would get same profile if client sent a profile request with a org_profile_id is a locked profile.
        loop_check = self.loop_inspection()
        if loop_check['loops_count'] > 0:
            return '存在循环引用'+str(loop_check['loops_list']),71
        else:
            profile_info = self.show(limit=1,profile_id=profile_id)
            if len(self.all_profile_list) == 0:
                return '找不到要锁定的配置',71
            else:
                if profile_id in profile_info:
                    if profile_info[profile_id]['status'] in [65,66,73] :
                        result_update = update_user_profile(project=self.project,status=67,profile_id=profile_id,desc='锁定该配置文件升级67')
                        return '锁定成功',70
                    elif profile_info[profile_id]['status'] in [72,67,68] :
                        return '非生效配置，锁定意义不明，须手工设定',71
                else:
                    return '该配置文件不存在',71

    def loop_inspection(self):
        #Ensure there is not any loop in profile and return possible loops if there are loops.
        #It is important to terminate loop otherwise an infinity loop will stop profile check.
        #Merge multi original ids is compatible,such as A1-->B  A2-->B A3-->B will get a loops_count 0.
        pending_loop = []
        result = self.my_profile()
        current_id = result['profile_id']
        next_id = result['next_id']
        next_list = []
        next_list.append(current_id)
        while next_id:
            next_result = self.show(limit=1,profile_id=next_id)
            next_profile = next_result[list(next_result.keys())[0]] if len(next_result)>0 else None
            if next_profile and next_profile['next_id'] and next_profile['next_id'] in next_list:
                pending_loop.append({'previous_id':next_id,'next_id':next_profile['next_id']})
                break
            elif next_profile and next_profile['next_id']:
                next_id = next_profile['next_id']
                next_list.append(next_id)
            else:
                next_id = None
        previous_list = []
        previous_list.append(current_id)
        while current_id:
            previous_result = self.show(limit=1,next_id=current_id)
            previous_profile = previous_result[list(previous_result.keys())[0]] if len(previous_result)>0 else None
            if previous_profile and previous_profile['profile_id'] and previous_profile['profile_id'] in previous_list:
                pending_loop.append({'previous_id':previous_profile['profile_id'],'next_id':current_id})
                break
            elif previous_profile and previous_profile['profile_id']:
                current_id = previous_profile['profile_id']
                previous_list.append(current_id)
            else:
                current_id = None
        return {'loops_count':len(pending_loop),'loops_list':pending_loop}


    def show(self,limit=1,status=0,profile_id=None,next_id=None):
        result = select_user_profile(project=self.project,remark=self.remark,limit=limit,status=status,profile_id=profile_id,next_id=next_id)
        self.all_profile_list = {}
        for all_profile in result[0]:
            self.all_profile_list[all_profile[0]] = {'profile_id':all_profile[0],'desc':all_profile[1],'profile':json.loads(all_profile[2]) if all_profile[2] else None,'remark':all_profile[3],'owner':all_profile[4],'next_id':all_profile[5],'status':all_profile[6],'created_at':all_profile[7],'updated_at':all_profile[8],'gray_percent':all_profile[9]}
        return self.all_profile_list

    def json(self,profile):
        self.profile = json.dumps(profile)
        pass

    def get_org_profile(self,org_profile_id=None):
        while True:
            if org_profile_id:
                org_profile = self.show(limit=1,profile_id=org_profile_id)
                if len(org_profile) == 0:
                    org_profile = self.show(limit=1,status=[65,66])
            else:
                org_profile = self.show(limit=1,status=[65,66])
            if len(org_profile) >0:
                last_profile_id = list(org_profile.keys())[0] #get the only profile id from list
                if org_profile[last_profile_id]['status'] in [67,65]:
                    #停留和最新配置的则不再升级
                    return {'org_profile':org_profile[last_profile_id],'org_profile_id':org_profile[last_profile_id]['profile_id'],'next_profile_id':None}
                elif org_profile[last_profile_id]['status'] in [68,72]:
                    #如使用失效配置，则当做无原始配置文件
                    org_profile_id=None
                    # org_profile = self.get_org_profile()
                elif org_profile[last_profile_id]['status'] == 66:
                    #如使用的配置文件有升级，则通知下一步进入升级流程
                    next_profile_id = org_profile[last_profile_id]['next_id']
                    return {'org_profile':org_profile[last_profile_id],'org_profile_id':org_profile[last_profile_id]['profile_id'],'next_profile_id':next_profile_id}
                elif org_profile[last_profile_id]['status'] == 73:
                    #if status means gray release,return profile and wait lottery.
                    return {'org_profile':org_profile[last_profile_id],'org_profile_id':org_profile[last_profile_id]['profile_id'],'next_profile_id':None}
            else:
                return {'org_profile':{'profile_id':None,'next_id':None},'org_profile_id':None,'next_profile_id':None}

    def my_profile(self,org_profile_id=None):
        #if froced a profile_id whose status code is 73 ,the return will be the forced profile id and it won't check a previous profile id.
        #get a profile what depended on user's profile.
        first_profile = self.get_org_profile(org_profile_id=org_profile_id) # init original_profile first
        org_profile = dict(first_profile['org_profile'])
        # org_id = int(first_profile['org_profile_id'])
        org_next_profile_id = int(first_profile['next_profile_id']) if first_profile['next_profile_id'] else None
        next_profile = None
        next_profile_id = int(org_next_profile_id) if org_next_profile_id else None

        while next_profile_id:
            #Keep find next_profile if there is a next_profile_id until there is a final one.
            #It won't stop in process like 11->12->13,no matter what status 12 is.
            next_profile = self.get_org_profile(org_profile_id=next_profile_id)
            next_profile_id = next_profile['next_profile_id'] if 'next_profile_id' in next_profile else None
            if next_profile_id:
                org_profile = dict(next_profile['org_profile'])
                org_id = int(next_profile['org_profile_id'])
                org_next_profile_id = int(next_profile['next_profile_id'])

        if next_profile and next_profile['org_profile']['status'] == 73 :
            num = random.randint(1,100)
            if next_profile['org_profile']['gray_percent'] and next_profile['org_profile']['gray_percent'] - num >= 0:
                # gray_percent must be provided otherwise it would be treated as 0 percent.
                return next_profile['org_profile']
            else:
                return org_profile
        elif next_profile and next_profile['org_profile']['status'] in (65,67):
            return next_profile['org_profile']
        else:
            return org_profile



def do_selftest():
    testa = profile_control(project='tvcbook',owner='ben',remark='selftest')
    write_to_log(filename='user_profile',defname='do_selftest',result='干净项目'+str(testa.my_profile()))
    testa.json({'ver':1})
    create_v1_result = testa.create(desc='ver1')
    write_to_log(filename='user_profile',defname='do_selftest',result='首个创建结果'+str(create_v1_result))
    write_to_log(filename='user_profile',defname='do_selftest',result='创建完未生效时的结果'+str(testa.my_profile()))
    write_to_log(filename='user_profile',defname='do_selftest',result='首个生效过程'+str(testa.enable(profile_id=create_v1_result[0])))
    write_to_log(filename='user_profile',defname='do_selftest',result='首个生效结果'+str(testa.my_profile()))
    testa.json({'ver':2})
    create_v2_result = testa.update(profile_id=create_v1_result[0],desc='ver2',gray_percent=50,update_now='yes')
    write_to_log(filename='user_profile',defname='do_selftest',result='首个升级过程'+str(create_v2_result))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='首次升级后，升级比例50%'+str(i)+str(testa.my_profile()))
    testa.json({'ver':3})
    create_v3_result = testa.update(profile_id=create_v2_result[0],desc='ver3',gray_percent=50,update_now='yes')
    write_to_log(filename='user_profile',defname='do_selftest',result='连续升级过程'+str(create_v3_result))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='连续升级后，新用户升级比例50%'+str(i)+str(testa.my_profile()))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='连续升级后，ver1用户升级比例50%'+str(i)+str(testa.my_profile(org_profile_id=create_v1_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='连续升级后，ver2用户升级比例50%'+str(i)+str(testa.my_profile(org_profile_id=create_v2_result[0])))
    write_to_log(filename='user_profile',defname='do_selftest',result='连续升级冲突'+str(testa.enable(profile_id=create_v2_result[0])))
    write_to_log(filename='user_profile',defname='do_selftest',result='手动升级ver2'+str(update_user_profile(project=testa.project,status=65,profile_id=create_v2_result[0],desc='手动生效65'))+str(update_user_profile(project=testa.project,status=68,profile_id=create_v1_result[0],next_id=create_v2_result[0],desc='手动停用68')))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='手动升级一个后，升级比例50%'+str(i)+str(testa.my_profile()))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='手动升级一个后，ver1用户升级比例50%'+str(i)+str(testa.my_profile(org_profile_id=create_v1_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='手动升级一个后，ver2用户升级比例50%'+str(i)+str(testa.my_profile(org_profile_id=create_v2_result[0])))
    write_to_log(filename='user_profile',defname='do_selftest',result='无冲突升级过程'+str(testa.enable(profile_id=create_v3_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='无冲突升级后，新用户升级比例50%'+str(i)+str(testa.my_profile()))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='无冲突升级后，ver1用户升级比例50%'+str(i)+str(testa.my_profile(org_profile_id=create_v1_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='无冲突升级后，ver2用户升级比例50%'+str(i)+str(testa.my_profile(org_profile_id=create_v2_result[0])))
    write_to_log(filename='user_profile',defname='do_selftest',result='回滚版本'+str(testa.rollback(profile_id=create_v3_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚最新后新用户'+str(i)+str(testa.my_profile()))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚最新后新用户的老版本'+str(i)+str(testa.my_profile(org_profile_id=create_v1_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚最新后的中版本'+str(i)+str(testa.my_profile(org_profile_id=create_v2_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚最新后的回滚版本'+str(i)+str(testa.my_profile(org_profile_id=create_v3_result[0])))
    testa.json({'ver':4})
    create_v4_result = testa.create(desc='ver4')
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚后新增配置未生效无前序'+str(i)+str(testa.my_profile()))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚后新增配置未生效无前序v1'+str(i)+str(testa.my_profile(org_profile_id=create_v1_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚后新增配置未生效无前序v2'+str(i)+str(testa.my_profile(org_profile_id=create_v2_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚后新增配置未生效无前序v3'+str(i)+str(testa.my_profile(org_profile_id=create_v3_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='回滚后新增配置未生效无前序v4'+str(i)+str(testa.my_profile(org_profile_id=create_v4_result[0])))
    write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件'+str(testa.enable(profile_id=create_v4_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序'+str(i)+str(testa.my_profile()))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v1'+str(i)+str(testa.my_profile(org_profile_id=create_v1_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v2'+str(i)+str(testa.my_profile(org_profile_id=create_v2_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v3'+str(i)+str(testa.my_profile(org_profile_id=create_v3_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v4'+str(i)+str(testa.my_profile(org_profile_id=create_v4_result[0])))
    testa.json({'ver':5})
    create_v5_result = testa.update(profile_id=create_v4_result[0],desc='ver5',gray_percent=50,update_now='yes')
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序'+str(i)+str(testa.my_profile()))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v1'+str(i)+str(testa.my_profile(org_profile_id=create_v1_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v2'+str(i)+str(testa.my_profile(org_profile_id=create_v2_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v3'+str(i)+str(testa.my_profile(org_profile_id=create_v3_result[0])))
    for i in range(10):
        write_to_log(filename='user_profile',defname='do_selftest',result='生效created的配置文件无前序v4'+str(i)+str(testa.my_profile(org_profile_id=create_v4_result[0])))
    # print(a.show())
    # for i in range(10):
    #     print(a.my_profile(org_profile_id=1))
    #     print(a.my_profile(org_profile_id=3))
    #     # print(a.get_org_profile(org_profile_id=3))
    #     print(a.my_profile())
    # a.json(profile={'ver':5})
    # print(a.create(desc='ver2'))
    # print(a.enable(profile_id=65601))
    # for i in range(100):
    #     print(a.loop_inspection())
    # print(a.rollback(profile_id=3))
    # print(a.enable(profile_id=3))
    # print(a.update(profile_id=1,desc='v5',gray_percent=30))



if __name__ == '__main__':
    do_selftest()