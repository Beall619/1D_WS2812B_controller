import control
from multiprocessing import Queue

b = Queue()
a = control.control(b)
a.thread.join()