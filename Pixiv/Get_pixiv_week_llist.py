#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/23 14:58
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : Get_pixiv_day_list.py
# @Software: PyCharm
import requests
import pymysql
import json
import time
import random
import configparser
config_info = configparser.ConfigParser()
fui=config_info.read("config.ini")
mysql_info_host = config_info.get("mysql","host")
mysql_info_name = config_info.get("mysql","db_name")
mysql_info_username = config_info.get("mysql","username")
mysql_info_password = config_info.get("mysql","password")
# 打开数据库连接
db = pymysql.connect(host=mysql_info_host, user=mysql_info_username, password=mysql_info_password, database=mysql_info_name)
cursor = db.cursor()
# 使用cursor()方法获取操作游标
tags_list = []#TAG列表
def get_database_pid_list():
	_pid_list = []
	_sql = "SELECT PID FROM pixiv_week"#执行搜索语句，搜索全部PID
	cursor.execute(_sql)
	_database_pid_list = cursor.fetchall()
	for pid in _database_pid_list:
		_pid_list.append(pid[0])
	return (_pid_list)
def sql_sava(PID, NAME, AUTHOR, img_big_link_num, Width, Height, tags_dist, img_big_link_regular,
             img_big_link_original):#保存到数据库方法

	list_id = 0
	print("-----开始进行SQL-----")
	_data = (str(PID),NAME,AUTHOR,json.dumps(tags_dist,ensure_ascii=False),img_big_link_regular,img_big_link_original,img_big_link_num,Width,Height)
	#别问，问就是我也不知道写的啥
	#print(_data) 需要的时候自行取消注释
	_sql = "INSERT INTO pixiv_week (PID,NAME,AUTHOR,TAGS,img_big_link,img_original_link,P_NUM,Width,Height) VALUES {}".format(_data)
	print("执行SQL语句："+_sql)
	print("hello")
	try:
		cursor.execute(_sql)
		db.commit()
		list_id = list_id + 1
		print("没进语句？")
		return (int(list_id))
	except:
		print("发送意料不到的错误")
		return("error")

get_database_pid_list()
for page in range(1,5):

	url = "https://www.pixiv.net/ranking.php?p="+str(page)+"&format=json&format%09=day"
	print("获取API")
	pixiv_day = requests.get(url)
	pixiv_day_json = pixiv_day.json()
	pixiv_day_json_list = pixiv_day_json["contents"]
	for num in range(1, 50):
		pixiv_day_json_data = pixiv_day_json_list[num]
		if pixiv_day_json_data["illust_id"] in get_database_pid_list():#如果有重复的就直接不执行，剩下一次get和一堆数据处理
			print("发现重复的PID:"+str(pixiv_day_json_data["illust_id"])+"系统自动跳过本UID")
			continue
		if "漫画" not in pixiv_day_json_data["tags"]:
			tags_dist = {
				"tags": pixiv_day_json_data["tags"]
			}
			PID = pixiv_day_json_data["illust_id"]
			print(PID)
			NAME = pixiv_day_json_data["title"]
			AUTHOR = pixiv_day_json_data["user_name"]
			Width = pixiv_day_json_data["width"]
			Height = pixiv_day_json_data["height"]
			tags_list = pixiv_day_json_data["tags"]
			_get_img_header = {
				"accept-encoding": "gzip, deflate, br",
				"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
				"referer": "https://www.pixiv.net/artworks/87991868",
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.58 Safari/537.36 Edg/89.0.774.34"
			}
			_get_img_url = "https://www.pixiv.net/ajax/illust/" + str(PID) + "/pages"#拼接API接口
			pixiv_day_img = requests.get(url=_get_img_url, headers=_get_img_header)
			pixiv_day_img_json = pixiv_day_img.json()
			#获取API接口信息
			img_big_link_num = len(pixiv_day_img_json["body"])#获取一共有多少个分P
			img_big_link_regular = pixiv_day_img_json["body"][0]["urls"]["regular"]#获取大图片地址（压缩）
			img_big_link_original = pixiv_day_img_json["body"][0]["urls"]["original"]#获取原始图片地址（不压缩）
			sleep_time = random.randint(1,3)#随机休眠
			print("采集完毕，正在准备休眠：" + str(sleep_time))
			time.sleep(sleep_time)
			list_num = sql_sava(PID, NAME, AUTHOR, str(img_big_link_num), str(Width), str(Height), tags_dist,img_big_link_regular,img_big_link_original)
			if list_num==0:
				print("未检测到榜单更新")
			elif list_num == "error":
				print("发送程序错误，请管理员尽快处理")
			else:
				print("本次更新已经保存"+str(list_num)+"张图片")
			#发送到数据库方法，保存到数据库
			# list_num_all = list_num_all + list_num
			# print("当前成功保存到数据库的图片序列："+list_num)
			#计算保存序列
