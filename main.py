import collections
import time
import threading
import random

file_lock = threading.Lock()

global barrier

'''
    def fun(total_time):
    
        k = [ti.timeout/total_time for ti in thread_list]
    
        a = [1 - ki for ki in k]
        a_sum = sum(a)
    
        r = [a_sum - ai for ai in a]
        r_sum = sum(r)
    
        new_time_lst = [60*ri/r_sum for ri in r]
    
        print('[NEW TIME-LIST]', new_time_lst)
    
        for obj, ti in zip(thread_list, new_time_lst):
            obj.timeout = ti
'''


class TimeThread:

    def __init__(self, file_path, priority):
        self.timeout = 0
        self.priority = priority
        self.file_path = file_path

    def set_timeout(self, timeout_):
        self.timeout = timeout_

    def write_in_file(self):
        start = time.monotonic()
        while True:
            with open(self.file_path, 'w') as file:
                file.write(str(self.priority))
            if time.monotonic() - start >= self.timeout:
                break
        print(f'{self.file_path} {self.priority} Ended')
        barrier.wait()

    def start(self):
        t = threading.Thread(target=self.write_in_file)
        t.start()


def get_threads_by_priority(thread_lst, priority):
    return list(filter(lambda x: x.priority == priority, thread_lst))


def check_condition(time_list):
    for ti in time_list:
        if not 5 <= ti <= 7:
            return True
    return False


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

    time_for_each_group = 2

    # список из 10 чисел
    priority_list = [random.randint(1, 10) for i in range(10)]
    priority_list.sort()

    thread_list = []

    # Формируем потоки - назначаем каждому файл и приоритет
    for key, pr in enumerate(priority_list):
        thread_list.append(TimeThread(f'{key}.txt', pr))

    # Словраь (приоритет : кол-во потоков с этим приоритетом)
    # Количество вхождений каждого приоритета
    priority_dict = collections.Counter(priority_list)
    print(priority_dict)
    # Пробегаемся по каждому приоритету кроме последнего
    for pr in list(priority_dict.keys())[:-1]:
        # Инициализируем барьер на n+1 потоков
        barrier = threading.Barrier(priority_dict.get(pr) + 1)
        # Определили время для текущего приоритета
        timeout = time_for_each_group / priority_dict.get(pr)

        # Запускаем все потоки с этим приоритетом
        for thread in get_threads_by_priority(thread_list, pr):
            thread.set_timeout(timeout)
            thread.start()
        barrier.wait()

        # Закидываем текущую группу потоков в минимальный приоритет
        for thread in get_threads_by_priority(thread_list, pr):
            thread.priority = list(priority_dict.keys())[-1]

    print('--------------------------------------------------------------')

    # 9-ый пункт ---------------------------------------------------------
    # Теперь у нас все потоки одного приоритета

    CONDITION = True

    while CONDITION:

        # Суммарное время всех потоков
        total_time = sum([obj.timeout for obj in thread_list])

        # Нахождение новых коэффициентов

        t = [obj.timeout for obj in thread_list]

        a = [(total_time if ti == 0 else ti) / total_time for ti in t]

        b = [1 - ai for ai in a]

        b_sum = sum(b)

        c = [b_sum if bi == 0 else bi/b_sum for bi in b]

        X = sum(c)

        # Новое время
        new_time_list = [ci/X * 60 for ci in c]
        print(new_time_list)

        barrier = threading.Barrier(10 + 1)

        for thread, ti in zip(thread_list, new_time_list):
            thread.set_timeout(ti)
            thread.start()
        barrier.wait()

        CONDITION = check_condition(new_time_list)









