from queue import Queue


class ResManager:

    def __init__(self, max_size=4096) -> None:
        super().__init__()
        self._queue = Queue(max_size)

    def get_task(self):
        return self._queue.get()

    def put_task(self, url):
        self._queue.put(url)


res_manager = ResManager(max_size=4096)
