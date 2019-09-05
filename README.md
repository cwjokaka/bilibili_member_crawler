# bilibili_member_crawler 
B站用户信息爬虫 (求Star\(^o^)/~
仅供娱乐学习使用

### 环境
* python 3.6+
* mysql 5.7+

### 下载安装

* 下载源码:

```shell
git clone git@github.com:cwjokaka/bilibili_member_crawler.git

或者在https://github.com/cwjokaka/bilibili_member_crawler 下载zip文件
```

* 安装相关依赖:

```shell
pip install -r requirements.txt
```

### 文件介绍
* `bilibili_member_crawler.py`：爬虫入口
* `distributor.py`：任务分发器,负责生成任务到任务队列
* `worker.py`：工作线程,负责从任务队列拉取任务,并把B站用户信息持久化到mysql
* `res_manager.py`：资源管理,用于管理任务队列
* `variable.py`: 配置文件, 包含代理、数据库、线程设置等
* `sql/bilibili.sql`：数据库初始化文件
* `user-agents.txt`：浏览器agent列表文件
* `exception/*`：各类异常

### 注意
* 请控制好您的车速(由variable.py的线程数、爬取时间间隔决定)
* 代理PROXIES需要定期更换(2019/9/4已加入外部代理池)


PS:有时间会做相关统计 (溜了溜了
