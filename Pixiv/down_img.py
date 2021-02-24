#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/24 11:37
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : down_img.py
# @Software: PyCharm
import pymysql
import requests
import time
import random
import configparser
import os

config_info = configparser.ConfigParser()
fui = config_info.read("config.ini")
mysql_info_host = config_info.get("mysql", "host")
mysql_info_name = config_info.get("mysql", "db_name")
mysql_info_username = config_info.get("mysql", "username")
mysql_info_password = config_info.get("mysql", "password")


# 获取数据库信息

# 打开数据库连接
# 使用cursor()方法获取操作游标
def get_all():
	db = pymysql.connect(host=mysql_info_host, user=mysql_info_username, password=mysql_info_password,
	                     database=mysql_info_name)
	# 连接数据库
	cursor = db.cursor()
	# 遍历全表
	sql = "select * from PIXIV_day"
	# 执行语句
	cursor.execute(sql)
	# 获取所有记录列表
	down_url = cursor.fetchall()
	return down_url
	# 断开
	db.close()


for all in get_all():
	headers = {
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"sec-fetch-dest": "document",
		"sec-fetch-mode": "navigate",
		"sec-fetch-site": "cross-site",
		"sec-fetch-user": "?1",
		"referer": "https://www.pixiv.net/",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.49"
	}
	img_pid = all[1]  # 获取图片PID（从数据库中）
	img_down_url = all[7]  # 获取图片下载地址（从数据库中）
	img = requests.get(url=img_down_url, headers=headers)
	# 上方为下载图片
	print("当前状态码：" + str(img.status_code))  # 输出状态码
	if img.status_code == 200:  # 判断是否获取成功
		file_name = str(all[1]) + img_down_url[-4:]
		print("开始保存图片，图片名称：" + file_name)
		with open(("./img/" + file_name), "wb+") as files:
			files.write(img.content)
		# 保存图片到img路径
		print("保存成功")
		time_num = random.randint(1, 10)
		print("系统开始休眠，下次运行时间：" + str(time_num) + "s")
		time.sleep(time_num)
		print("系统休眠结束,开始下一次运行")
	# 随机休眠机制
	else:
		print("发生错误，图片下载失败，具体请查看状态码，系统将自动跳出循环并查询下一个图片")
		continue
