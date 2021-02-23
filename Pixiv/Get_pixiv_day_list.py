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

db = pymysql.connect(host="127.0.0.1", user="test", password="TESTTEST", database="PIXIV_request")
list_id = 0
url = "https://www.pixiv.net/ranking.php?p=1&format=json&format%09=day"
pixiv_day = requests.get(url)
pixiv_day_json = pixiv_day.json()
pixiv_day_json_list = pixiv_day_json["contents"]
cursor = db.cursor()
tags_list = []


def sql_sava(PID, NAME, AUTHOR, img_big_link_num, Width, Height, tags_dist, img_big_link_regular,
             img_big_link_original):
	print("------------")
	_data = "(" + str(PID) + "," + '"' + NAME + '"'"," + '"' + AUTHOR + '"' + ",'" + json.dumps(tags_dist,
	                                                                                            ensure_ascii=False) + "',"
	_data = _data + '"' + img_big_link_regular + '",' + '"' + img_big_link_original + '",'
	_data = _data + '"' + img_big_link_num + '",' + '"' + Width + '",' + '"' + Height + '"' + ")"
	print(_data)
	_sql = "INSERT INTO pixiv_day (PID,NAME,AUTHOR,TAGS,img_big_link,img_original_link,P_NUM,Width,Height) VALUES " + _data
	print(_sql)
	cursor.execute(_sql)
	db.commit()


for num in range(1, 50):
	pixiv_day_json_data = pixiv_day_json_list[num]
	if "漫画" not in pixiv_day_json_data["tags"]:
		print(pixiv_day_json_data)
		tags_dist = {
			"tags": pixiv_day_json_data["tags"]
		}
		PID = pixiv_day_json_data["illust_id"]
		NAME = pixiv_day_json_data["title"]
		AUTHOR = pixiv_day_json_data["user_name"]
		Width = pixiv_day_json_data["width"]
		Height = pixiv_day_json_data["height"]
		# img_original_link = pixiv_day_json_data["title"]
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
		_get_img_url = "https://www.pixiv.net/ajax/illust/" + str(PID) + "/pages"

		pixiv_day_img = requests.get(url=_get_img_url, headers=_get_img_header)
		pixiv_day_img_json = pixiv_day_img.json()
		img_big_link_num = len(pixiv_day_img_json["body"])
		img_big_link_regular = pixiv_day_img_json["body"][0]["urls"]["regular"]
		img_big_link_original = pixiv_day_img_json["body"][0]["urls"]["original"]
		print(img_big_link_regular)
		print(img_big_link_original)

		sql_sava(PID, NAME, AUTHOR, str(img_big_link_num), str(Width), str(Height), tags_dist, (img_big_link_regular),
		         img_big_link_original)

	list_id = list_id + 1

	print(list_id)
