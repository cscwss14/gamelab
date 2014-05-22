# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:54:07 2014

@author: ankur
"""

import threading
from time import sleep
index = 0 
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)
 
#keep this lock object always as a global variable
sem = threading.Lock()
# Example usage
def someOtherFunc(data, key):
    global index
    
    for i in range(10):
        sem.acquire()       
        print "index", index
        index +=1
        sem.release()
        sleep(1)
    
 
def otherFunc():
    for i in range(10):
        sem.acquire()
        print "i",i
        sem.release()
        sleep(1)
        
if __name__ == "__main__":
    t1 = FuncThread(someOtherFunc, [1,2], 6)
    t2 = FuncThread(otherFunc)
    t1.start()
    t2.start()
    t1.join()
    t2.join()