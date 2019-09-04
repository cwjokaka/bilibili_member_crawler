# 用户信息页面URL
PAGE_URL = 'http://space.bilibili.com'
# 获取用户信息接口
API_MEMBER_INFO = 'http://api.bilibili.com/x/space/acc/info'

# MySQL配置
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'bilibili'

# 使用https://github.com/jhao104/proxy_pool的代理池，也可自行部署其服务，然后把PROXY_POOL_URL的地址改成localhost
USE_PROXY_POOL = True
# https://github.com/jhao104/proxy_pool的测试服务器地址
PROXY_POOL_URL = 'http://118.24.52.95/get_all'
# 代理设置(需要自行添加), 如果
PROXIES = \
    ["211.152.33.24:59523", "211.152.33.24:59523", "103.35.64.12:3128", "117.127.16.206:8080", "51.77.162.148:3128"
     ,"119.41.236.180:8010", "124.42.68.152:90", "94.177.246.142:8080", "51.15.117.119:8080", "66.7.113.39:3128"
     ,"94.247.62.184:8080", "123.117.70.143:8060", "117.141.155.241:53281", "94.177.214.178:8080", "111.231.90.122:8888"
     , "210.22.5.117:3128", "51.79.57.158:3128", "58.17.125.215:53281"
     ]

# 浏览器agent列表, 初始化时会加附加上user-agents.txt里的内容
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0'
]
# 抓取等待最大时间(s)
WAIT_MAX = 2
# 开启抓取线程的数量
THREADS_NUM = 256
# 每条线程抓取的间隔范围(s)
FETCH_INTERVAL_MIN = 0.01
FETCH_INTERVAL_MAX = 0.05
# 想要抓取的用户id范围
FETCH_MID_FROM = 30000
FETCH_MID_TO = 200000
