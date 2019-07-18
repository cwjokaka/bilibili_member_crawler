import time
import MySQLdb
import random
import requests

from requests import ConnectTimeout, ReadTimeout
from threading import Thread
from typing import Optional

from requests.exceptions import ProxyError

from res_manager import res_manager
from variable import *


class Worker(Thread):

    def __init__(self, name) -> None:
        super().__init__(name=name)
        self.headers = {
            'Host': 'api.bilibili.com',
            'Origin': PAGE_URL,
            'Referer': f'{PAGE_URL}/{random.randint(1, 100000)}',
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'application/json',
            'Connection': 'close',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.cur_proxy = {'https': f'http://{random.choice(PROXIES)}'}

    def run(self) -> None:
        print(f'爬虫线程:{self.name}开始执行...')
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, charset='utf8')
        cur = conn.cursor()
        while True:
            task_url = res_manager.get_task()
            self._update_req_info()
            self._crawl(task_url, cur)
            conn.commit()
            time.sleep(random.uniform(FETCH_INTERVAL_MIN, FETCH_INTERVAL_MAX))

    def _crawl(self, mid, cur):
        """
        抓取并持久化用户信息
        :param mid: B站用户id
        :param cur: mysql游标
        :return: None
        """
        member_info = self._get_member_by_mid(mid)
        if member_info is None:
            return
        mid = member_info['mid']
        name = member_info['name']
        sign = member_info['sign'].replace("'", "\\'")
        rank = member_info['rank']
        level = member_info['level']
        jointime = member_info['jointime']
        moral = member_info['moral']
        silence = member_info['silence']
        birthday = member_info['birthday']
        coins = member_info['coins']
        fans_badge = member_info['fans_badge']
        vip_type = member_info['vip']['type']
        vip_status = member_info['vip']['status']
        try:
            cur.execute(f"INSERT INTO bilibili_member "
                        f"(mid, name, sign, rank, level, jointime, moral, silence, birthday, coins, fans_badge, "
                        f"vip_type, vip_status) "
                        f"VALUES "
                        f"({mid}, '{name}', '{sign}', {rank}, {level}, {jointime}, {moral}, {silence}, '{birthday}', "
                        f"{coins}, {fans_badge}, {vip_type}, {vip_status})"
                        )
        except MySQLdb.ProgrammingError as e:
            print(f'插入用户: {mid} 数据出错:{e}')
        except MySQLdb.IntegrityError:
            print(f'用户: {mid} 数据已存在,不作插入')

    def _get_member_by_mid(self, mid: int) -> Optional[dict]:
        """
        根据用户id获取其信息
        :param mid: B站用户id
        :return: 用户详情 or None
        """
        get_params = {
            'mid': mid,
            'jsonp': 'jsonp'
        }
        try:
            res_json = requests.get(API_MEMBER_INFO, params=get_params, timeout=32, proxies=self.cur_proxy,
                                    headers=self.headers).json()
        except ConnectTimeout:
            print(f'获取用户id: {mid} 详情失败: 请求接口超时, 当前代理:{self.cur_proxy["https"]}')
        except ReadTimeout:
            print(f'获取用户id: {mid} 详情失败: 接口读取超时, 当前代理:{self.cur_proxy["https"]}')
        except ValueError:
            # 解析json失败基本上就是ip被封了
            print(f'获取用户id: {mid} 详情失败: 解析json出错, 当前代理:{self.cur_proxy["https"]}')
        except ProxyError as e:
            print(f'获取用户id: {mid} 详情失败: 连接代理失败, 当前代理:{self.cur_proxy["https"]}, {e}')
        except requests.ConnectionError:
            # 可以断定就是代理IP地址无效
            print(f'获取用户id: {mid} 详情失败: 连接错误, 当前代理:{self.cur_proxy["https"]}')
        else:
            if 'data' in res_json:
                return res_json['data']
            print(f'获取用户id: {mid} 详情失败: data字段不存在!')
        return

    def _update_req_info(self):
        """
        更新请求信息, 主要用于防反爬
        :return:
        """
        self.headers.update({
            'Referer': f'{PAGE_URL}/{random.randint(1, 100000)}',
            'User-Agent': random.choice(USER_AGENTS),
        })
        self.cur_proxy.update({
            'https': f'http://{random.choice(PROXIES)}',
        })
