import MySQLdb
import random
from threading import Thread
from variable import *
from abc import ABCMeta, abstractmethod, abstractproperty


class BaseWorker(Thread, metaclass=ABCMeta):

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

