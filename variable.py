# 用户信息页面URL
PAGE_URL = 'https://space.bilibili.com'
# 获取用户信息接口
API_MEMBER_INFO = 'https://api.bilibili.com/x/space/acc/info'

# MySQL配置
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'bilibili'

# 代理设置(需要随时替换)
PROXIES = ["123.169.121.139:9999", "113.121.67.91:9999", "202.9.24.226:8080", "113.121.64.157:9999"]


# 浏览器agent列表, 初始化时会加附加上user-agents.txt里的内容
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0'
]

# 开启抓取线程的数量
THREADS_NUM = 16
# 每条线程抓取的间隔范围(s)
FETCH_INTERVAL_MIN = 0.5
FETCH_INTERVAL_MAX = 1.5
# 想要抓取的用户id范围
FETCH_MID_FROM = 97
FETCH_MID_TO = 20000
