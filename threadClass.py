import threading
from time import sleep

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)
 
# Example usage
def someOtherFunc(data, key):
    print "someOtherFunc was called : data=%s; key=%s" % (str(data), str(key))
    sleep(1)
 
def otherFunc():
    for i in range(10):
        print i
        sleep(1)
        
if __name__ == "__main__":
    t1 = FuncThread(someOtherFunc, [1,2], 6)
    t2 = FuncThread(otherFunc)
    t1.start()
    t2.start()
    t1.join()
    t2.join()