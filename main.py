import collections
import time
import threading
import random


file_lock = threading.Lock()

global barrier


class CoolThread:

    def __init__(self, p, t):
        self.p = p
        self.t = t

    def f(self):
        start_time = time.monotonic()
        while True:
            with file_lock:
                print(self.p, threading.current_thread().name)
            time.sleep(0.1)
            if time.monotonic() - start_time >= self.t:
                break
        print(self.p, 'thread is ended')
        barrier.wait()

    def change_timeout(self):
        pass

    def run(self):
        t = threading.Thread(target=self.f)
        t.start()


if __name__ == '__main__':

    iteration = 0

    while True:

        priority = [random.randint(1, 10) for i in range(10)]
        priority.sort()
        b = collections.Counter(priority)  # группируем по приоритетам (количество)
        print(b.items())

        mx = max(b.keys())
        print(mx)
        input()
        t_list = []

        for key, val in b.items():
            for i in range(val):
                t_list.append(CoolThread(key, 3 / val))

        for i in range(1, mx if iteration == 0 else mx + 1):

            buff = list(filter(lambda t: t.p == i and i != mx, t_list))
            barrier = threading.Barrier(len(buff) + 1)

            for t in buff:
                t.run()
            barrier.wait()

