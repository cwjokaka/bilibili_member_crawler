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

# 代理设置(需要自行添加)
PROXIES = ["183.146.213.198:80","42.238.91.38:9999","183.146.213.157:80","27.208.89.118:8060","116.62.198.43:8080"]


# 浏览器agent列表, 初始化时会加附加上user-agents.txt里的内容
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0'
]

# 开启抓取线程的数量
THREADS_NUM = 64
# 每条线程抓取的间隔范围(s)
FETCH_INTERVAL_MIN = 0.1
FETCH_INTERVAL_MAX = 0.3
# 想要抓取的用户id范围
FETCH_MID_FROM = 11000
FETCH_MID_TO = 200000
