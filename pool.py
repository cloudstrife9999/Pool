# author = cloudstrife9999

from multiprocessing.pool import Pool
from multiprocessing import Process, Queue


# Daemonic processes (the default implementation in multiprocessing.pool.Pool) cannot instantiate subprocesses.
class NoDaemonProcess(Process):
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


# Daemonic processes (the default implementation in multiprocessing.pool.Pool) cannot instantiate subprocesses.
class NoDaemonPool(Pool):
    def __reduce__(self):
        super(NoDaemonPool, self).__reduce__()

    Process = NoDaemonProcess


# This class wraps the actual pool (which, according to the boolean attribute, may be Pool or NoDaemonPool).
class WorkersPool:
    # Daemonic processes (the default implementation in multiprocessing.pool.Pool) cannot instantiate subprocesses.
    def __init__(self, daemon, queue_elements, pool_size, parameters):
        self.pool = None
        self.__daemon = daemon  # boolean
        self.__pool_size = pool_size
        self.__parameters = parameters
        self.__init_queue(queue_elements)

    def get_queue(self):
        return self.__queue

    def get_pool_size(self):
        return self.__pool_size

    def is_daemonic(self):
        return self.__daemon

    def get_parameters(self):
        return self.__parameters

    def __init_queue(self, queue_elements):
        size = len(queue_elements)
        self.__queue = Queue(size)

        for elm in queue_elements:
            self.__queue.put(elm)

    def init_and_start_pool(self):
        parameters = tuple([self.__pool_size] + self.__parameters)

        if self.__daemon:
            self.pool = Pool(self.__pool_size, self.__working_function, parameters)
        else:
            self.pool = NoDaemonPool(self.__pool_size, self.__working_function, parameters)

        self.__wait_for_completion()

        print "All the workers in the pool have terminated their work."

    def __wait_for_completion(self):
        self.pool.close()
        self.pool.join()

    def __test_function(self, parameters):
        print "Starting: parameters received: " + str(parameters)

        while not self.__queue.empty():
            print self.__queue.get()

        print "Empty queue."
        print "Job over for this worker, waiting for the others..."

    def __working_function(self, parameters):
        self.__test_function(parameters)

        # do whatever needed here
