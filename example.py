# author = cloudstrife9999

from pool import WorkersPool


w = WorkersPool(True, range(1000), 2, 5, ["initial message", ": ", "random string."])
w.init_and_start_pool()


w = WorkersPool(False, range(1000, 2000), 2, 5, ["initial message", ": ", "random string."])
w.init_and_start_pool()
