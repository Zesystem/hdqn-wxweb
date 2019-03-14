##########################################
#
# 时间处理工具类封装
# author: TuYaxuan
# time: 2019/3/14
#
###########################################

import time
from datetime import datetime, timedelta

def time_afterday(n):
    if n < 0:
        n = abs(n)
        return datetime.now()-timedelta(days=n)
    return datetime.now()+timedelta(days=n)

def week_now():
    return (datetime.now().weekday() + 1) % 7

def month_now():
	return time.strftime('%m', time_afterday(week_now()).timetuple())

def day_after(n):
    return time.strftime('%d', time_afterday(n).timetuple())

def get_week_day():
    t = -(week_now() + 6) % 7
    week = [{'ch':'周一'},{'ch':'周二'},{'ch':'周三'},{'ch':'周四'},{'ch':'周五'},{'ch':'周六'},{'ch':'周日'}]
    for i in range(7):
        week[i]['num'] = day_after(t)
        t += 1
    return week

def week_to_num(ch_week):
    return ['周一', '周二', '周三', '周四', '周五', '周六', '周日'].index(ch_week)