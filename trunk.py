import time
import MySQLdb
import random
import requests

from requests import ConnectTimeout, ReadTimeout
from typing import Optional

from requests.exceptions import ProxyError

from base_worker import BaseWorker
from res_manager import res_manager
from variable import *


class Trunk(BaseWorker):

    def __init__(self, name) -> None:
        super().__init__(name=name)

    def run(self) -> None:
        print(f'trunk线程:{self.name}开始执行...')
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, charset='utf8')
        cur = conn.cursor()
        while True:
            task_url = res_manager.get_task()
            self._update_req_info()
            self._crawl(task_url, cur)
            conn.commit()
            time.sleep(random.uniform(FETCH_INTERVAL_MIN, FETCH_INTERVAL_MAX))

