#!/usr/bin/python
# encoding: utf-8

import time
import threadpool
def sayhello(str):
    print "Hello ",str
    time.sleep(2)

name_list =['xiaozi','aa','bb','cc']
start_time = time.time()
pool = threadpool.ThreadPool(10)
requests = threadpool.makeRequests(sayhello, name_list)
[pool.putRequest(req) for req in requests]
pool.wait()
print '%d second'% (time.time()-start_time)