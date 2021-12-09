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
            if time.monotonic() - start_time >= self.t:
                break
        print(self.p, 'thread is ended')
        barrier.wait()

    def change_timeout(self):
        pass

    def run(self):
        t = threading.Thread(target=self.f)
        t.start()


def get_thread_pool():
    priority = [random.randint(1, 10) for i in range(10)]
    priority.sort()
    return priority


if __name__ == '__main__':

    '''
        
        b = { (k, v), ... }  (k, v) = (priority, number) 
                                        * priority - приоритет потока
                                        * number - количество потоков с этим приоритетом
    
        [g1, g2, ... , gk] - P (Приоритеты)
    
        [p1, p2, ... , pn ] - приоритет для i-го потока
        
        while CONDITION:
        
            total_time{ 
                1-ая итерация: (P.size() - 1) * 60
                any  итерация: P.size() * 60
            }
            
            [t1, t2, ... , total_time ] - время на i-ый поток : ti = 60 / кол-во потоков в группе
            
            
            [ k1, k2, ... , kn ] : ki = ti / total_time
            
            [ a1, a2, ... , an ] : ai = 1 - ki 
                                        [1 - ti / total_time]
            
            sum = S(ai)   
                  S[ 1 - ti / total_time ]
            
            [ r1, r2, ... , rn] : ri = sum - ai
                                       { S[ total_time - ti ] - total_time - ti } / total_time
    
            Новое время: 
                Rsum = S(ri)
                     = S < { S[ total_time - ti ] - total_time - ti } / total_time >
                     = S < { S[ total_time - ti ] - total_time - ti } > / total_time
                
                [ q1, q2, ... , qn] : qi = ri/Rsum * 60
                
                +---------------------------------------------------------------------------------------+
                |                                                                                       |
                |                                S[ total_time - ti ] - total_time - ti                 |
                |  [ q1, q2, ... , qn] : qi = --------------------------------------------------- * 60  |
                |                             S { S[ total_time - ti ] - total_time - ti }              |
                |                                                                                       |
                +---------------------------------------------------------------------------------------+  
                
        
                
    '''

    iteration = 0
    s = 0

    priority = get_thread_pool()

    for i in range(1):

        b = collections.Counter(priority)  # группируем по приоритетам (количество)
        print(b.items())

        group_count = len(b.items())

        mx = max(b.keys())
        print(mx)
        input()
        t_list = []

        for key, val in b.items():
            for i in range(val):
                t_list.append(CoolThread(key, 2 / val))

        for i in range(1, mx if iteration == 0 else mx + 1):

            buff = list(filter(lambda t: t.p == i and i != mx, t_list))
            barrier = threading.Barrier(len(buff) + 1)
            for t in buff:
                t.run()
            barrier.wait()
