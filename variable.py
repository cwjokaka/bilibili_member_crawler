# 用户信息页面URL
PAGE_URL = 'https://space.bilibili.com'
# 获取用户信息接口
API_MEMBER_INFO = 'http://api.bilibili.com/x/space/acc/info'

# MySQL配置
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'bilibili'

# 代理设置(需要随时替换)
PROXIES = [
    "82.114.241.138:8080",
    "144.123.71.209:9999",
    "112.247.183.88:8060",
    "222.135.29.176:8060",
    "27.203.208.215:8060",
    "180.168.13.26:8000",
    "27.208.184.227:8060",
    "119.179.151.250:8060",
    "112.80.41.78:8888",
    "82.114.241.138:8080",
    "111.197.249.231:8060"
]

# 浏览器agent列表, 初始化时会加附加上user-agents.txt里的内容
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0'
]

# 开启抓取线程的数量
THREADS_NUM = 4
# 每条线程抓取的间隔范围(s)
FETCH_INTERVAL_MIN = 0.5
FETCH_INTERVAL_MAX = 2
# 想要抓取的用户id范围
FETCH_MID_FROM = 1
FETCH_MID_TO = 2000
