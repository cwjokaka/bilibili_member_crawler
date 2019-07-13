from threading import Thread
from res_manager import res_manager


class Distributor(Thread):
    """
    任务分发线程,负责下发任务(用户mid)到队列
    """
    def __init__(self, start: int, end: int):
        super().__init__()
        self._start = start
        self._end = end

    def run(self) -> None:
        print('Distributor开始执行...')
        for mid in range(self._start, self._end):
            res_manager.put_task(mid)
        print('Distributor执行完毕')
