# author = cloudstrife9999

from multiprocessing.pool import Pool
from multiprocessing import Process, Queue
from multiprocessing.queues import Empty


# Daemonic processes (the default implementation in multiprocessing.pool.Pool) cannot instantiate children processes.
class NoDaemonProcess(Process):
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


# Daemonic processes (the default implementation in multiprocessing.pool.Pool) cannot instantiate children processes.
class NoDaemonPool(Pool):
    def __reduce__(self):
        super(NoDaemonPool, self).__reduce__()

    Process = NoDaemonProcess


# This class wraps the actual pool (which, according to the boolean attribute, may be Pool or NoDaemonPool).
class WorkersPool:
    # Daemonic processes (the default implementation in multiprocessing.pool.Pool) can't instantiate children processes.
    def __init__(self, daemon, queue_elements, queue_reading_timeout, pool_size, parameters):
        self.__pool = None
        self.__daemon = daemon  # boolean
        self.__queue_reading_timeout = queue_reading_timeout
        self.__pool_size = pool_size
        self.__parameters = parameters
        self.__init_queue(queue_elements)

    def get_queue(self):
        return self.__queue

    def get_queue_reading_timeout(self):
        return self.__queue_reading_timeout

    def get_pool_size(self):
        return self.__pool_size

    def is_daemonic(self):
        return self.__daemon

    def get_parameters(self):
        return self.__parameters

    def get_pool(self):
        return self.__pool

    def __init_queue(self, queue_elements):
        size = len(queue_elements)
        self.__queue = Queue(size)

        for elm in queue_elements:
            self.__queue.put(elm)

    def init_and_start_pool(self):
        parameters = tuple([self.__pool_size] + self.__parameters)

        if self.__daemon:
            self.__pool = Pool(self.__pool_size, self.__working_function, parameters)
        else:
            self.__pool = NoDaemonPool(self.__pool_size, self.__working_function, parameters)

        self.__wait_for_completion()

        print "All the workers in the pool have terminated their work."

    def __wait_for_completion(self):
        self.__pool.close()
        self.__pool.join()

    # this is just an example test function.
    def __test_function(self, parameters):
        print "Starting: parameters received: " + str(parameters)

        try:
            p = Process(target=execfile, args=("test.py",))
            p.start()
        except AssertionError as e:  # this is raised if the method __test_function is called by a daemonic process.
            print e.message

        while not self.__queue.empty():
            try:
                print self.__queue.get(timeout=self.__queue_reading_timeout)
            except Empty:
                print "########## TIMEOUT: retrying... ##########"

        print "Empty queue."
        print "Job over for this worker, waiting for the others..."

    def __working_function(self, *parameters):
        self.__test_function(parameters)  # this is just a test, remove it.

        # do whatever needed here.
