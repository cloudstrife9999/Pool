# Pool
A Python multiprocessing.pool.Pool wrapper, allowing to create non daemonic pools (which is a requirement for the processes in the pool to be able to spawn subprocesses).

The use scenario is the spawning of many parallel workers which perform the same task over and over, while continuously and concurrently reading data from a queue, until it is empty.
It is easy to customize the code to make the "reads" popping the elements from the queue or just passing onto the next one.