# author = cloudstrife9999

from pool import WorkersPool

w = WorkersPool(True, range(100), 5, [])
w.init_and_start_pool()


w = WorkersPool(False, range(1000, 2000), 5, [])
w.init_and_start_pool()

