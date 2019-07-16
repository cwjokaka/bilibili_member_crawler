import random

from distributor import Distributor
from variable import USER_AGENTS, THREADS_NUM, FETCH_MID_FROM, FETCH_MID_TO
from worker import Worker


class BilibiliMemberCrawler:
    """
    B站爬虫入口,用于初始化配置与开启线程
    """
    @classmethod
    def start(cls):
        cls.init()
        # 开启任务分发线程
        Distributor(FETCH_MID_FROM, FETCH_MID_TO + 1).start()
        # 开启爬虫线程
        for i in range(0, THREADS_NUM):
            Worker(f'Worker-{i}').start()

    @staticmethod
    def init():
        """
        读取并初始化浏览器agent
        """
        with open('user-agents.txt', 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    USER_AGENTS.append(ua.strip()[:-1])
        random.shuffle(USER_AGENTS)


if __name__ == '__main__':
    BilibiliMemberCrawler.start()
