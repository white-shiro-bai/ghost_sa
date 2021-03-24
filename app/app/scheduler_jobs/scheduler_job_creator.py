# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from app.component.db_func import insert_usergroup_plan,insert_noti_temple
import json

def create_usergroup_plan():
    
    #计划策略
    project = 'demo_app' #项目名称
    group_title = '最近登录的2500位用户' #分群标题、
    group_desc = '最近到访用户的2500位已注册用户。从T-1天开始向前查七天，如果七天凑不够2500，以实际数量为准。包含T-1天。	' #分群描述
    repeatable = '* 3 * * *' #任务重复定时器，分，时，日，月，周。不填的用*代替。跟crontab一个逻辑，但不支持1-10的方式表达，多日的需要1,2,3,4,5,6,7,8这样的形式填 如'* 1 1,2,3 * *'即为每月1,2,3日的凌晨1点执行,周的表达方式0是周一，6是周日
    priority = 13 #任务的优先级
    enable_policy = 28 #模板生效的策略,8自动，9手动，10禁用，24自动分群但不自动应用模板,28自动分群自动应用模板但不自动发送
    
    #计划内容
    default_temple = [1] #默认推送模板（如果开启自动应用模板,enable_policy=8，则依次应用array里的所有模板，如果不需要自动应用模板，可以为空或者enable_policy=24)
    func_dir = "scheduler_jobs.demo_app" #计划所调用的func位置
    func_name = "last_1500_email" #计划所调用的func名称
    args = {"count": 2500, "date": "___date___", "days": 7} # 计划需要传递的变量名及变量

    #入库
    func = {"args": args, "default_temple": default_temple, "dir": func_dir, "name": func_name}
    result = insert_usergroup_plan(project=project,group_title=group_title,group_desc=group_desc,repeatable=repeatable,priority=priority,enable_policy=enable_policy,func_args=json.dumps(func,ensure_ascii=False))
    print(result)


def create_noti_temple():
    
    #模板信息
    name = '你在demo_app的视频有更新了' #模板的名称
    temple_desc = '视频取当前推荐影片的前5条，自动应用模板时，所有人是create_auto_group，手动应用的所有人是应用人。' #描述模板

    #模板策略
    project = 'tvcbook' #项目名称
    track_url = 'http://你的域名/sa.gif' #鬼策的监测地址（用来接收数据的地址）
    remark = 'production' #鬼策的remark标记
    default_send_time = '* 15 * * 5' #自动发送的时间，分，时，日，月，周。不填的用*代替。跟crontab一个逻辑，但不支持1-10的方式表达，多日的需要1,2,3,4,5,6,7,8这样的形式填 如'* 1 1,2,3 * *'即为每月1,2,3日的凌晨1点执行

    #附加组件调用
    required = True #模板是否需要调用外部程序补充数据，True时会调用func_dir和func_name所指定的程序。调用外部程序的功能主要用来解决用户分群时无法创建千人千面结果的情况，如分群只分出了用户信息，但是推送内容并不同步生产，如一个分群对应多次个模板套用的情况。
    func_dir = "scheduler_jobs.demo_app" #模板所需要调用的外部程序目录
    func_name = "home_ref" #模板所需要调用的外部程序名称

    #meta信息（模板描述信息）
    medium = "email" #模板适配的媒介名称（对应status_code表）
    medium_id = 23 #模板适配的媒介id（对应status_code表）

    #替换参数
    args = {"content": "___content___", "email": "___email___", "nickname": "___nickname___", "subject": "hey，___nickname___，你在demo_app搜索的创意视频有更新了，快来看看吧", "utm_campaign": "___owner___", "utm_content": "___group_id___", "utm_email": "___email___", "utm_medium": "noti_temple_1", "utm_source": "邮件", "utm_term": "___etl_date___"} #temple_args,data_args和func里返回的内容会替换content里的___key___部分，

    #推送正文
    content = '''<table width="600" border="0"  class="ke-zeroborder">
	<tbody>
		<tr>
			<td>
				<p align="center">
					<img src="https://www.baidu.com/img/flexible/logo/pc/result.png" alt="LOGO" width="460" /> 
				</p>
				<p align="center">
					<span style="font-family:微软雅黑, Microsoft YaHei;"><strong>Hey,&nbsp;&nbsp;___nickname___:&nbsp;</strong></span> 
				</p>
				<p align="center">
					<span>最近热门的新鲜创意都看全了吗？</span> 
				</p>
				<p align="center">
					<span>我们为你整理了这些~</span> 
				</p>
				<p align="center">
					<strong><span style="font-size:16px;"> 下滑查看新鲜创意</span></strong> 
				</p>
				<p align="center">
					<strong><span style="font-size:16px;"> ▽▽▽</span></strong> 
				</p>
			</td>
		</tr>
		<tr>
			<td >
				<table width="520" border="0" align="center" cellspacing="0" class="ke-zeroborder">
					<tbody>
						<tr>
							<td >
								<a href="https://www.bilibili.com/video/___vid_1_url___?utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___video_title_1___" target="_blank"><img width="520" src="___video_cover_1_img_url___" alt="___video_title_1___" /></a> 
							</td>
						</tr>
						<tr>
							<td>
								<strong><a href="https://www.bilibili.com/video/___vid_1_url___?utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___video_title_1___" style="text-decoration:none" target="_blank"><span style="color:#000000;font-size:16px;line-height: 32px;" > ___video_title_1___</span></a></strong> 
							</td>
						</tr>
						<tr>
							<td>
								<table width="520" border="0" cellspacing="0" class="ke-zeroborder">
									<tbody>
										<tr>
											<td width="50">
												<a href="https://www.tvcbook.com/personalPage.html#/mainpage/mainPublic?user_id=___user_id_1___&code=___user_id_1_code___&utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___author_name_1___" target="_blank"><img src="___auther_title_1_url___" alt="___author_name_1___" width="40" border="0" /></a> 
											</td>
											<td >
												<span style="font-size:16px;"><strong><a href="https://www.tvcbook.com/personalPage.html#/mainpage/mainPublic?user_id=___user_id_1___&code=___user_id_1_code___&utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___author_name_1___" style="text-decoration:none" target="_blank"> <span style="color:#000000;">___author_name_1___</span></a></strong></span>
											</td>
										</tr>
									</tbody>
								</table>
							</td>
						</tr>
						<tr>
							
							<td >
								<br><br><br>
								<a href="https://www.tvcbook.com/showVideo.html?vid=___vid_2_url___&code=___vid_2_code___&utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___video_title_2___" target="_blank"><img src="___video_cover_2_img_url___" alt="___video_title_2___" width="520" /> </a>
							</td>
						</tr>
						<tr>
							<td  >
								<strong><a href="https://www.tvcbook.com/showVideo.html?vid=___vid_2_url___&code=___vid_2_code___&utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___video_title_2___" style="text-decoration:none" target="_blank"><span style="color:#000000;font-size:16px;line-height: 32px;"> ___video_title_2___</span></a></strong> 
							</td>
						</tr>
						<tr>
							<td>
								<table width="520" border="0" class="ke-zeroborder"  >
									<tbody>
										<tr>
											<td width="50">
												<a href="https://www.tvcbook.com/personalPage.html#/mainpage/mainPublic?user_id=___user_id_2___&code=___vid_2_code___&utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___author_name_2___" target="_blank"><img src="___auther_title_2_url___" alt="___author_name_2___" width="40" border="0" /></a> 
											</td>
											<td>
												<span style="font-size:16px;"><strong><a href="https://www.tvcbook.com/personalPage.html#/mainpage/mainPublic?user_id=___user_id_2___&code=___user_id_2_code___&utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=___author_name_2___" style="text-decoration:none" target="_blank"> <span style="color:#000000;">___author_name_2___</span></a></strong></span>
											</td>
										</tr>
									</tbody>
								</table>
							</td>
						</tr>
					</tbody>
				</table>
			</td>
		</tr>
		<tr>
			<td>
				<table align="center" width="520" border="0" class="ke-zeroborder">
					<tbody>
						<tr>
							<td >
								<br><br><br>
								<div align="center">
									<a href="https://www.tvcbook.com/homepage.html?utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=查看更多" target="_blank"><img  height="60" src="https://image-cn2.tvcbook.com//attach/20190926/156948319913162953.png" alt="查看更多" /></a> 
								</div>
							</td>
						</tr>
						<tr>
							<td>
								<br><br><br>
								<p align="center">
									<br />
								</p>
								<p align="center">
									<strong><span style="font-size:16px;"> 广告合作联系方式<br />
邮箱：<a href="mailto:pm@tvcbook.com"><span style="font-size:16px;">pm@tvcbook.com</span></a> <br />
添加VX：T13342875311</span></strong> <br><img src="https://image-cn2.tvcbook.com//attach/20201125/160630711321597672.jpg" alt="wechat" width="200">
								</p>
								<p align="center">
									<HR align=center width=520 color=#000000 SIZE=1>
								</p>
								<p align="center">
									<span style="font-size:16px;"><strong><br />
</strong></span><span style="font-size:16px;">如有任何疑问欢迎随时联系</span> 
								</p>
								<p align="center">
									<span style="font-size:16px;">电话：400-876-0103 | 邮箱：</span><a href="mailto:pm@tvcbook.com"><span style="font-size:16px;">pm@tvcbook.com</span></a> 
								</p>
								<p align="center">
									<span style="font-size:16px;">如不想再收到此类邮件，请</span><a href="https://www.tvcbook.com/unsubscribe.html?utm_source=___utm_source___&utm_campaign=___utm_campaign___&utm_term=___utm_term___&utm_medium=___utm_medium___&utm_content=退订"><span style="font-size:16px;">退订</span></a> 
								</p>
							</td>
						</tr>
					</tbody>
				</table>
				<p align="center">&nbsp;
				<img src="___read_tracker___" width="0" height="0" alt="" />
				</p>
					
				</p>
			</td>
		</tr>
	</tbody>
</table>''' #推送的正文内容，需要替换的部分前后加上___，应用模板的时候，会被temple_args,data_args和func里返回的内容替换.
    # content = "这是一个测试内容，用户昵称是___nickname___，跳转链接是http://www.tvcbook.com/?utm_source=___utm_source___\u0026tm_campaign=___utm_campaign___\u0026utm_term=___utm_term___\u0026utm_content=___group_id___\u0026utm_medium=___utm_medium___,跟踪链接是___read_tracker___" #推送的正文内容，需要替换的部分前后加上___，应用模板的时候，会被temple_args,data_args和func里返回的内容替换.
    subject = "___subject___" #推送的标题内容，需要替换的部分前后加上___，应用模板的时候，会被temple_args,data_args和func里返回的内容替换.
    mail_to = "___email___" #推送的目标地址，不一定是email地址，也可以是手机号，看自定义变量定义的是什么
    mail_from = "" #推送的发件人地址，不一定是email，看自定义变量定义的是什么

    #入库
    pending_args = {"add_on_func": {"dir": func_dir, "name": func_name , "required": required}, "args": args, "ghost_sa": {"remark": remark, "track_url": track_url}, "meta": {"medium": medium, "medium_id": medium_id, "default_send_time":default_send_time}}
    pending_content = {"content": content, "mail_from": mail_from, "mail_to": mail_to, "subject": subject}
    result = insert_noti_temple(project=project,name=name,args=json.dumps(pending_args,ensure_ascii=False),content=json.dumps(pending_content,ensure_ascii=False),temple_desc=temple_desc)
    
def create_noti_temple_wechat():
    #这是一个适用于发微信消息的特殊模板
    #模板信息
    name = '会员订阅成功' #模板的名称
    temple_desc = '用户成功订阅会员时发送微信通知' #描述模板

    #模板策略
    project = 'demo_app' #项目名称
    track_url = 'https://yourdomain/sa.gif' #鬼策的监测地址（用来接收数据的地址）
    remark = 'production' #鬼策的remark标记
    default_send_time = '* * * * *' #自动发送的时间，分，时，日，月，周。不填的用*代替。跟crontab一个逻辑，但不支持1-10的方式表达，多日的需要1,2,3,4,5,6,7,8这样的形式填 如'* 1 1,2,3 * *'即为每月1,2,3日的凌晨1点执行。其中周位0表示周一，6表示周日

    #附加组件调用
    required = True #模板是否需要调用外部程序补充数据，True时会调用func_dir和func_name所指定的程序。调用外部程序的功能主要用来解决用户分群时无法创建千人千面结果的情况，如分群只分出了用户信息，但是推送内容并不同步生产，如一个分群对应多次个模板套用的情况。
    func_dir = "trigger_jobs.sample" #模板所需要调用的外部程序目录
    func_name = "vip_order_complated" #模板所需要调用的外部程序名称

    #meta信息（模板描述信息）
    medium = "wechat_official_account" #模板适配的媒介名称（对应status_code表）
    medium_id = 29 #模板适配的媒介id（对应status_code表）

    #替换参数
    args = {"content": "___content___", "wechat_openid":"___wechat_openid___","order_id":"___order_id___","nickname": "___nickname___", "utm_campaign": "___owner___", "utm_content": "vip_purchased","utm_medium": "noti_temple_1", "utm_source": medium, "utm_term": "___vip_type___"} #temple_args,data_args和func里返回的内容会替换content里的___key___部分，

    #推送正文
    content = {"first": {"value":"恭喜您于 ___order_date___ 成功开通优视会员！","color":"#173177"},"keyword1":{"value":"___order_id___","color":"#173177"},"keyword2": {"value":"___vip_type___","color":"#173177"},"keyword3": {"value":"___totalpay_sum___","color":"#173177"},"keyword4": {"value":"___expire_at_str___","color":"#173177"},"remark":{"value":"___remark___","color":"#173177"}} #推送的正文内容，需要替换的部分前后加上___，应用模板的时候，会被temple_args,data_args和func里返回的内容替换.
    wechat_openid = "___wechat_openid___" #openid
    wechat_template_id = "wyCHxVmQ4AbtDjE5pVXyDCSm0jsLE3irOv4BfEwDT3k"#模板id
    target_url = "http://www.qq.com/" #目标的url


    #入库
    pending_args = {"add_on_func": {"dir": func_dir, "name": func_name , "required": required}, "args": args, "ghost_sa": {"remark": remark, "track_url": track_url}, "meta": {"medium": medium, "medium_id": medium_id, "default_send_time":default_send_time}}
    pending_content = {'content':json.dumps({'wechat_openid':wechat_openid,'wechat_template_id':wechat_template_id,'target_url':target_url,'data':content})}
    result = insert_noti_temple(project=project,name=name,args=json.dumps(pending_args,ensure_ascii=False),content=json.dumps(pending_content,ensure_ascii=False),temple_desc=temple_desc)


if __name__ == "__main__":
    # create_usergroup_plan()
	# create_noti_temple_wechat()
    create_noti_temple()