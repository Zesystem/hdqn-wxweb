##########################################
#
# 字符串工具函数封装
# author: TuYaxuan
# time: 2019/3/14
#
###########################################

def strstr(str1, str2):
    return str1.strip() == str2.strip()

def empty(string):
	return string.strip() == ""