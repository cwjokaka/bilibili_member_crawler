import time
from threading import Thread

import MySQLdb
import random
import requests

from requests import ConnectTimeout, ReadTimeout
from typing import Optional

from requests.exceptions import ProxyError, ChunkedEncodingError

from exception.request_exception import RequestException
from exception.sql_already_exists_exception import SqlAlreadyExistsException
from exception.sql_insert_exception import SqlInsertException
from exception.user_not_found_exception import UserNotFoundException
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
        self.cur_proxy = {'https': f'https://{random.choice(PROXIES)}'}

    def run(self) -> None:
        print(f'爬虫线程:{self.name}开始执行...')
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, charset='utf8')
        cur = conn.cursor()
        while True:
            mid = res_manager.get_task()
            while True:
                self._update_req_info()
                try:
                    self._crawl(mid, cur)
                    break
                except RequestException:
                    # 如果是请求上的异常，则重试
                    # print(f'重新爬取用户:{mid}')
                    continue
                except SqlInsertException as e:
                    # 数据插入异常, 则插入异常记录
                    self._insert_failure_record(cur, mid, 0, e.msg)
                    break
                except UserNotFoundException as e:
                    self._insert_failure_record(cur, mid, 0, e.msg)
                    break
                except SqlAlreadyExistsException:
                    break
            conn.commit()
            time.sleep(random.uniform(FETCH_INTERVAL_MIN, FETCH_INTERVAL_MAX))

    def _crawl(self, mid, cur):
        """
        抓取并持久化用户信息
        :param mid: B站用户id
        :param cur: mysql游标
        :return: None
        """
        if self._is_member_exist(cur, mid):
            print(f'数据库中已存在此用户mid:{mid}, 忽略')
            return
        member_info = self._get_member_by_mid(mid)
        if member_info is None:
            return
        mid = member_info['mid']
        name = member_info['name']
        sign = member_info['sign'].replace("'", "\\\'")
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
            print(f'成功插入用户数据: {mid}, 当前代理:{self.cur_proxy["https"]}')
        except MySQLdb.ProgrammingError as e:
            print(f'插入用户: {mid} 数据出错:{e}')
            raise SqlInsertException(str(e))
        except MySQLdb.IntegrityError:
            print(f'用户: {mid} 数据已存在,不作插入')
            raise SqlAlreadyExistsException('数据已存在')

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
            res_json = requests.get(API_MEMBER_INFO, params=get_params, timeout=WAIT_MAX, proxies=self.cur_proxy,
                                    headers=self.headers).json()
        except ConnectTimeout as e:
            print(f'获取用户id: {mid} 详情失败: 请求接口超时, 当前代理:{self.cur_proxy["https"]}')
            raise RequestException(str(e))
        except ReadTimeout as e:
            print(f'获取用户id: {mid} 详情失败: 接口读取超时, 当前代理:{self.cur_proxy["https"]}')
            raise RequestException(str(e))
        except ValueError as e:
            # 解析json失败基本上就是ip被封了
            print(f'获取用户id: {mid} 详情失败: 解析json出错, 当前代理:{self.cur_proxy["https"]}')
            raise RequestException(str(e))
        except ProxyError as e:
            print(f'获取用户id: {mid} 详情失败: 连接代理失败, 当前代理:{self.cur_proxy["https"]}')
            raise RequestException(str(e))
        except requests.ConnectionError as e:
            # 可以断定就是代理IP地址无效
            print(f'获取用户id: {mid} 详情失败: 连接错误, 当前代理:{self.cur_proxy["https"]}')
            raise RequestException(str(e))
        except ChunkedEncodingError as e:
            print(f'获取用户id: {mid} 详情失败: 远程主机强迫关闭了一个现有的连接, 当前代理:{self.cur_proxy["https"]}')
            raise RequestException(str(e))
        else:
            if res_json['code'] == -404:
                print(f'找不到用户mid:{mid}')
                raise UserNotFoundException(f'找不到用户mid:{mid}')
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
            'https': f'https://{random.choice(PROXIES)}',
            'http': f'http://{random.choice(PROXIES)}',
        })

    @staticmethod
    def _insert_failure_record(cur, mid, state, remark):
        remark = remark.replace("'", "\\\'")
        try:
            cur.execute(
                "INSERT INTO failure_record (mid, remark, state) "
                f"VALUES ({mid}, '{remark}', '{state}')"
            )
        except MySQLdb.ProgrammingError as e:
            print(f'插入失败日志: {mid} 数据出错:{e}')
        except MySQLdb.IntegrityError:
            print(f'失败日志: {mid} 数据已存在,不作插入')

    @staticmethod
    def _is_member_exist(cur, mid):
        cur.execute(
            "SELECT COUNT(*) FROM bilibili_member "
            f"WHERE mid={mid}"
        )
        return cur.fetchone()[0] == 1

