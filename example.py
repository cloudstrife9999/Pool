# author = cloudstrife9999

from pool import WorkersPool


def main():
    print "@@@@@@@@@@ Starting pool made by daemonic processes... @@@@@@@@@@"

    w = WorkersPool(True, range(1000), 2, 5, ["initial message", ": ", "random string."])
    w.init_and_start_pool()

    print "@@@@@@@@@@ End of pool made by daemonic processes. @@@@@@@@@@"
    print "@@@@@@@@@@ Starting pool made by non-daemonic processes... @@@@@@@@@@"

    w = WorkersPool(False, range(1000, 2000), 2, 5, ["initial message", ": ", "random string."])
    w.init_and_start_pool()

    print "@@@@@@@@@@ End of pool made by non-daemonic processes... @@@@@@@@@@"


if __name__ == '__main__':
    main()
