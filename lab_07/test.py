import os
from time import sleep
from multiprocessing import Process, Queue, Manager
import psutil
import random


def measure_mem(num):
    proc = Process(target=function, args=(num, ))
    pid = proc.pid
    mem = psutil.Process(pid).memory_info().rss / 1024 ** 2
    memory = (int(psutil.virtual_memory().available) / 1024 ** 2) * 0.8
    print('RAM in func: ', mem)
    print('available memory: ', memory)
    print('possible amount of processes: ', memory/mem)

    return memory/mem

def function(num):
    array = [random.randint(0, 100) for _ in range(num)]
    array.sort()


print(measure_mem(1000000000))
