# author = cloudstrife9999

import pool

w = pool.Worker(True, range(100), 5, [])
w.init_and_start_pool()


w = pool.Worker(False, range(1000, 2000), 5, [])
w.init_and_start_pool()

