# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import datetime
import time
import random
from configs.export import write_to_log
# 输出时间范围变量


def getdate(dateinput):
    # 第一个参数是yesterday取昨天数据，第一个参数是today取今天数据，第一个参数是日期，则取对应日期的数据
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    tomorrow = today+oneday

    if dateinput == 'yesterday':
        manualdate = yesterday
    elif dateinput == 'today':
        manualdate = today
    elif dateinput == 'tomorrow':
        manualdate = tomorrow
    else:
        manualdate = dateinput
    return manualdate


def date_diff(dateinput, granularity, calc):
    #获取相对日期，输入日期，间隔的方式，增减的幅度
    if granularity == 'month':
        predate = datetime.datetime.strptime(dateinput, '%Y-%m-%d')
        if predate.day == 1:
            if calc == 'sub':
                if predate.month == 1:
                    premonth = datetime.date(predate.year-1, 12, 1)
                elif predate.month != 1:
                    premonth = datetime.date(predate.year, predate.month-1, 1)
                return premonth
            elif calc == 'add':
                if predate.month == 12:
                    premonth = datetime.date(predate.year+1, 1, 1)
                elif predate.month != 12:
                    premonth = datetime.date(predate.year, predate.month+1, 1)
                return premonth
        elif predate.day != 1:
            if calc == 'sub':
                if predate.month == 1:
                    premonth = datetime.date(predate.year-1, 12, 31)
                elif predate.month != 1:
                    premonth = datetime.date(
                        predate.year, predate.month, 1)-datetime.timedelta(days=1)
                return premonth
            elif calc == 'add':
                if predate.month == 12:
                    premonth = datetime.date(predate.year+1, 1, 31)
                elif predate.month == 11:
                    premonth = datetime.date(predate.year, 12, 31)
                elif predate.month != 12:
                    premonth = datetime.date(
                        predate.year, predate.month+2, 1)-datetime.timedelta(days=1)
    elif granularity == 'week':
        if calc == 'sub':
            predate = datetime.datetime.strptime(
                dateinput, '%Y-%m-%d')-datetime.timedelta(days=7)
            report_predate = predate.strftime('%Y-%m-%d')
            return report_predate
        elif calc == 'add':
            predate = datetime.datetime.strptime(
                dateinput, '%Y-%m-%d')+datetime.timedelta(days=7)
            report_predate = predate.strftime('%Y-%m-%d')
            return report_predate


def get_start_end_days(datainput):
    # 获取给定时间所在的日期起止点
    this_week_start = str(datetime.date.today() -
                          datetime.timedelta(days=datetime.date.today().weekday()))
    this_week_end = str(datetime.date.today() +
                        datetime.timedelta(days=6-datetime.date.today().weekday()))
    last_week_start = str(date_diff(this_week_start, 'week', 'sub'))
    last_week_end = str(date_diff(this_week_end, 'week', 'sub'))
    last_2week_start = str(date_diff(last_week_start, 'week', 'sub'))
    last_2week_end = str(date_diff(last_week_end, 'week', 'sub'))
    # 月
    this_month_start = str(datetime.date(
        datetime.date.today().year, datetime.date.today().month, 1))
    if datetime.date.today().month != 12:
        this_month_end = str(datetime.date(datetime.date.today(
        ).year, datetime.date.today().month+1, 1)-datetime.timedelta(days=1))
    elif datetime.date.today().month == 12:
        this_month_end = str(datetime.date(
            datetime.date.today().year+1, 1, 1)-datetime.timedelta(days=1))

    last_month_start = str(date_diff(this_month_start, 'month', 'sub'))
    last_month_end = str(date_diff(this_month_end, 'month', 'sub'))
    last_2month_start = str(date_diff(last_month_start, 'month', 'sub'))
    last_2month_end = str(date_diff(last_month_end, 'month', 'sub'))

    if datainput == 'thisweek':
        return this_week_start, this_week_end
    elif datainput == 'lastweek':
        return last_week_start, last_week_end
    elif datainput == 'thismonth':
        return this_month_start, this_month_end
    elif datainput == 'lastmonth':
        return last_month_start, last_month_end
    elif datainput == 'last2month':
        return last_2month_start, last_2month_end
    elif datainput == 'last2week':
        return last_2week_start, last_2week_end
    else:
        predate = datetime.datetime.strptime(datainput, '%Y-%m-%d')
        if predate.month == 1:
            premonth = datetime.date(predate.year-1, 12, 1)
        elif predate.month != 1:
            premonth = datetime.date(predate.year, predate.month-1, 1)
        return premonth


def get_end_day(endtype, startdate):
    #获取日期结尾的那一天
    startday = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    # startdate = datetime.datetime.strptime(startdate,'%Y-%m-%d')
    if endtype == 'week':
        endday = datetime.date(startday.year, startday.month,
                               startday.day) + datetime.timedelta(days=6)
    elif endtype == 'month':
        if startday.month != 12:
            endday = datetime.date(startday.year, startday.month+1,
                                   1) - datetime.timedelta(days=1)
        elif startday.month == 12:
            endday = datetime.date(startday.year+1, 1, 1) - datetime.timedelta(days=1)
    return str(endday)


def get_display_day(start_day, calc):
    #获取显示日期（用于显示与输入日期相对的日期。注意，增减幅度不包含输入的日期）
    org_day = datetime.datetime.strptime(start_day, '%Y-%m-%d')
    display_day = datetime.date(
        org_day.year, org_day.month, org_day.day) + datetime.timedelta(days=calc)
    return str(display_day)


def current_timestamp():
    t = time.time()
    return int(t)


def get_day_list(start_day, end_day):
    #获取日期列表
    start_day = datetime.datetime.strptime(str(start_day), '%Y-%m-%d')
    end_day = datetime.datetime.strptime(str(end_day), '%Y-%m-%d')
    date_list = []
    date_list.append(start_day.strftime('%Y-%m-%d'))
    days = '"'+start_day.strftime('%Y-%m-%d')+'"'
    while start_day < end_day:
        # 日期叠加一天
        start_day += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(start_day.strftime('%Y-%m-%d'))
        days = days +',"'+start_day.strftime('%Y-%m-%d')+'"'
    return date_list,days


def get_time_str(inttime):
    datearray = datetime.datetime.fromtimestamp(inttime)
    strtime = datearray.strftime("%Y-%m-%d %H:%M:%S")
    return strtime


def get_next_time(timer=None,current_time=None):
    #该工具用来把corn的定时格式，转化为一个可执行的时间。多个时间选择的时候只支持 用','区分，如1,2,3,4,5。暂时不支持'-'如'1-10'和'/'如'3/15'。其中周位0表示周一。该工具只输出current_time时间当天的所有日期点。
    current_time=int(time.time()) if not current_time else current_time
    chour = str(time.localtime(current_time).tm_hour)
    cday = str(time.localtime(current_time).tm_mday)
    cmon = str(time.localtime(current_time).tm_mon)
    cweek = str(time.localtime(current_time).tm_wday)
    cyear = str(time.localtime(current_time).tm_year)
    cmin = str(time.localtime(current_time).tm_min)
    if timer:
        timer_array = timer.split(' ')
        mins=timer_array[0].split(',')
        hours=timer_array[1].split(',')
        days=timer_array[2].split(',')
        mons=timer_array[3].split(',')
        weeks=timer_array[4].split(',')
        tmins = ['00'] if '*' in mins else mins
        thours = ['00'] if '*' in hours else hours
        tday = cday if '*' in days or cday in days else None
        tmon = cmon if '*' in mons or cmon in mons else None
        tweek = cweek if '*' in weeks or cweek in weeks else None
        write_to_log(filename='public_value',defname='get_next_time',result=str(current_time))
        times = []
        # print(weeks,cweek,tweek)
        if tday and tmon and tweek:
            for thour in thours:
                for tmin in tmins:
                    times.append({'time_tuple':time.strptime('{yy}-{mm}-{dd} {hh}:{mi}:00'.format(yy=cyear,mm=cmon,dd=cday,hh=thour,mi=tmin), '%Y-%m-%d %H:%M:%S'),'time_int':int(time.mktime(time.strptime('{yy}-{mm}-{dd} {hh}:{mi}:00'.format(yy=cyear,mm=cmon,dd=cday,hh=thour,mi=tmin), '%Y-%m-%d %H:%M:%S')))})
    else:
        times = [{'time_tuple':time.strptime('{yy}-{mm}-{dd} {hh}:{mi}:00'.format(yy=cyear,mm=cmon,dd=cday,hh=chour,mi=cmin), '%Y-%m-%d %H:%M:%S'),'time_int':int(time.mktime(time.strptime('{yy}-{mm}-{dd} {hh}:{mi}:00'.format(yy=cyear,mm=cmon,dd=cday,hh=chour,mi=cmin), '%Y-%m-%d %H:%M:%S')))}]
    return times


def get_time_array_from_nlp(time_nlp):
    #自然语言输入时间，可以得到时间戳
    if ' ' in time_nlp:
        date = str(getdate(dateinput=time_nlp.split(' ')[0]))
        hour = time_nlp.split(' ')[1]
    else:
        date = str(getdate(dateinput=time_nlp))
        hour = '00:00:00'
    time_str = ''
    if ':' in hour:
        for item in hour.split(':'):
            if len(item) == 1 :
                if time_str != '' :
                    time_str = time_str+':'
                time_str = time_str+'0'+item
            elif len(item) == 2 :
                if time_str != '' :
                    time_str = time_str+':'
                time_str = time_str+item
    print(time_str)
    if len(time_str) == 5:
        time_str = time_str+':00'
    elif len(time_str) == 2:
        time_str = time_str+':00:00'
    elif len(time_str) == 0:
        time_str = '00:00:00'
    times = {'time_tuple':time.strptime(date+' '+time_str, '%Y-%m-%d %H:%M:%S'),'time_int':int(time.mktime(time.strptime(date+' '+time_str, '%Y-%m-%d %H:%M:%S'))),'date_str':date,'hour_str':time_str}
    return times


def get_priority():
    #获取优先级级别。15最高级，14优先，13普通
    num = random.randint(0,9)
    if num > 3 :
    #60%的资源分类立刻
        return 15
    elif num <3 :
    #30%的资源分给优先队列
        return 14
    else:
    #10%的资源分给正常队列
        return 13


if __name__ == '__main__':
    # print(get_start_end_days('lastmonth'))
    # print(get_end_day(endtype='week',startdate='2019-12-13'))
    # print(get_end_day(endtype='month',startdate='2019-12-01'))
    # print(get_display_day('2019-05-06',8))
    # print(get_day_list(start_day='2019-12-25', end_day='2020-01-03'))
    # print(get_time_str(inttime=1601135999))
    # hours = []
    # for i in range(0,24):
    #     hours.append(i)
    # print(hours)
    # while True:
    print(get_next_time(timer='* 15 * * 4'))
    # print(get_time_array_from_nlp('tomorrow 9:13'))