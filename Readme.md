# <h1><center>YH_Kaiheila_Bot</center></h1>

<h2><center>一款基于Python的P站日榜爬取与下载软件</center></h2>

### 本软件基于P站官方API
### 本软件使用Mysql进行操作
### 本软件使用pymysql进行数据库管理
目前状态：收尾状态
------
使用方法：<br/>
安装依赖库：pip install -r requirements.txt<br/>
导入setup.sql<br/>
修改config.ini文件，连接Mysql<br/>
保证你的网络能够正常连接P站<br/>
运行Get_pixiv_day_list.py<br/>
检查数据库，发现信息填充完毕后运行down_img.py<br/>
图片将自动生成在img文件夹<br/>
Power By YH
