import time
import psutil
from multiprocessing import Process, Queue, current_process


def heavy_computation(data_chunk):
    print(current_process().name)
    for n in range(30000000):
        k = data_chunk * n ^ n


class ProcessPool:

    def __init__(self, min_workers: int, max_workers: int, mem_usage: int):  # Мегабайты
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.process_time = 0
        self.pick_mem_usage = 0

    def check(self, func, data):
        memory_list = []
        mem = int(psutil.virtual_memory().available)
        memory_list.append(mem)
        check = Process(target=func, args=(data,), name='check_time')
        start = time.time()
        check.start()

        check.join()
        end = time.time()
        self.process_time = int(end - start)
        check = Process(target=func, args=(data,), name='check_pick_memory')
        check.start()
        for i in range(self.process_time * 100):
            mem = int(psutil.virtual_memory().available)
            memory_list.append(mem)
            time.sleep(0.01)
        check.join()
        self.pick_mem_usage = int((memory_list[0] - min(memory_list)) / 1024 / 1024)
        print('Пиковая занимаемая память:', self.pick_mem_usage, 'Мб')
        print('Время затраченное на один чанк данных:', self.process_time)

    def map(self, func, data):
        process_list = []
        possible_count_of_workers = int(self.mem_usage / self.pick_mem_usage)
        if possible_count_of_workers < self.min_workers:
            print(f'Максимальное число воркеров: {possible_count_of_workers}')
            return None
        if possible_count_of_workers > self.max_workers:
            count_of_workers = self.max_workers
        else:
            count_of_workers = possible_count_of_workers
        for chunk in data:
            q.put(chunk)
        start = time.time()
        while not q.empty():
            for _ in range(count_of_workers):
                data = q.get()
                process = Process(target=func, args=(data,))
                process_list.append(process)
                process.start()
                if q.empty(): break
            for proces in process_list:
                proces.join()
        end = time.time()
        print('Время обработки всех данных:', int(end - start))


if __name__ == '__main__':
    q = Queue()
    big_data = [6, 2, 3, 4, 5, 6, 2, 1, 3, 2, 1, 2, 3, 1, 3, 2, 1, 3, 1, 2]
    pool = ProcessPool(min_workers=3, max_workers=13, mem_usage=100)
    check = pool.check(heavy_computation, max(big_data))
    result = pool.map(heavy_computation, big_data)
