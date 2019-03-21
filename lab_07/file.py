import os
from time import sleep
from multiprocessing import Process, Queue, Manager
import psutil
import random


def function(number):
    a = 2**number
    return "done"


class ProcessPool:


    def __init__(self, min_workers=2, max_workers=10, mem_usage=1024):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage


    def measure_mem(self, data):
        number = max(data)
        proc = Process(target=function, args=(number, ))
        pid = proc.pid
        mem = psutil.Process(pid).memory_info().rss / 1024 ** 2
        memory = (int(psutil.virtual_memory().available) / 1024 ** 2) * 0.8
        print('RAM in func: ', mem)
        print('available memory: ', memory)
        print('possible amount of processes: ', memory/mem)
        return memory/mem




if __name__ == '__main__':
    data = [random.randint(10000000, 100000000) for i in range(10000)]
