# Python多进程

python中的多线程其实并不是真正的多线程，如果想要充分地使用多核CPU的资源，在python中大部分情况需要使用多进程。Python提供了非常好用的多进程包multiprocessing，只需要定义一个函数，Python会完成其他所有事情。借助这个包，可以轻松完成从单进程到并发执行的转换。multiprocessing支持子进程、通信和共享数据、执行不同形式的同步，提供了Process、Queue、Pipe、Lock等组件。

## 1. Process

**创建进程的类：** Process([group [, target [, name [, args [, kwargs]]]]])，target表示调用对象，args表示调用对象的位置参数元组。kwargs表示调用对象的字典。name为别名。group实质上不使用。  
**方法：** is_alive()、join([timeout])、run()、start()、terminate()。其中，Process以start()启动某个进程。  
**属性：** authkey、daemon（要通过start()设置）、exitcode(进程在运行时为None、如果为–N，表示被信号N结束）、name、pid。其中daemon是父进程终止后自动终止，且自己不能产生新进程，必须在start()之前设置。

### 1.1 创建函数并将其作为单个进程
$ ./test1.py
```youtrack
import multiprocessing
import time
 
def worker(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))
        time.sleep(interval)
        n -= 1
 
if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.start()
    print "p.pid:", p.pid
    print "p.name:", p.name
    print "p.is_alive:", p.is_alive()
```

运行结果
```youtrack
p.pid: 11336
p.name: Process-1
p.is_alive: True
The time is Mon Jul 24 11:43:45 2017
The time is Mon Jul 24 11:43:48 2017
The time is Mon Jul 24 11:43:51 2017
The time is Mon Jul 24 11:43:54 2017
The time is Mon Jul 24 11:43:57 2017

```

### 1.2 创建函数并将其作为多个进程

$ ./test2.py
```youtrack
import multiprocessing
import time
 
def worker_1(interval):
    print "worker_1"
    time.sleep(interval)
    print "end worker_1"
 
def worker_2(interval):
    print "worker_2"
    time.sleep(interval)
    print "end worker_2"
 
def worker_3(interval):
    print "worker_3"
    time.sleep(interval)
    print "end worker_3"
 
if __name__ == "__main__":
    p1 = multiprocessing.Process(target = worker_1, args = (2,))
    p2 = multiprocessing.Process(target = worker_2, args = (3,))
    p3 = multiprocessing.Process(target = worker_3, args = (4,))
 
    p1.start()
    p2.start()
    p3.start()
 
    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
    print "END!!!!!!!!!!!!!!!!!"

```

运行结果
```youtrack
The number of CPU is:4
child   p.name:Process-1	p.id11784
child   p.name:Process-3	p.id11392
child   p.name:Process-2	p.id11424
END!!!!!!!!!!!!!!!!!
worker_2
worker_1
worker_3
end worker_1
end worker_2
end worker_3

```

### 1.3 将进程定义为类

$ ./test3.py
```python
import multiprocessing
import time
 
class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval
 
    def run(self):
        n = 5
        while n > 0:
            print("the time is {0}".format(time.ctime()))
            time.sleep(self.interval)
            n -= 1
 
if __name__ == '__main__':
    p = ClockProcess(3)
    p.start()
```

注：进程p调用start()时，自动调用run()

运行结果：
```youtrack
the time is Mon Jul 24 11:51:53 2017
the time is Mon Jul 24 11:51:56 2017
the time is Mon Jul 24 11:51:59 2017
the time is Mon Jul 24 11:52:02 2017
the time is Mon Jul 24 11:52:05 2017

```

### 1.4 daemon程序对比结果

#### 1.4.1 不加daemon属性

$ ./test4.py
```python
import multiprocessing
import time
 
def worker(interval):
    print("work start:{0}".format(time.ctime()));
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()));
 
if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.start()
    print "end!"
```

运行结果
```youtrack
end!
work start:Mon Jul 24 11:55:46 2017
work end:Mon Jul 24 11:55:49 2017

```

#### 1.4.2 加上daemon属性

$ ./test5.py
```python
import multiprocessing
import time
 
def worker(interval):
    print("work start:{0}".format(time.ctime()));
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()));
 
if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.daemon = True
    p.start()
    print "end!"
```

运行结果
```youtrack
end!

```
注：因子进程设置了daemon属性，主进程结束，它们就随着结束了。

#### 1.4.3 设置daemon执行完结束的方法

$ ./test6.py

```python
import multiprocessing
import time
 
def worker(interval):
    print("work start:{0}".format(time.ctime()));
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()));
 
if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.daemon = True
    p.start()
    p.join()
    print "end!"
```
运行结果
```youtrack
work start:Mon Jul 24 12:00:17 2017
work end:Mon Jul 24 12:00:20 2017
end!

```

## 2. Lock

当多个进程需要访问共享资源的时候，Lock可以用来避免访问的冲突。

$ ./test7.py
```python
import multiprocessing
import sys
 
def worker_with(lock, f):
    with lock:
        fs = open(f, 'a+')
        n = 10
        while n > 1:
            fs.write("Lockd acquired via with\n")
            n -= 1
        fs.close()
 
def worker_no_with(lock, f):
    lock.acquire()
    try:
        fs = open(f, 'a+')
        n = 10
        while n > 1:
            fs.write("Lock acquired directly\n")
            n -= 1
        fs.close()
    finally:
        lock.release()
 
if __name__ == "__main__":
    lock = multiprocessing.Lock()
    f = "file.txt"
    w = multiprocessing.Process(target = worker_with, args=(lock, f))
    nw = multiprocessing.Process(target = worker_no_with, args=(lock, f))
    w.start()
    nw.start()
    print "end"
```
结果（输出文件）
```youtrack
Lockd acquired via with
Lockd acquired via with
Lockd acquired via with
Lockd acquired via with
Lockd acquired via with
Lockd acquired via with
Lockd acquired via with
Lockd acquired via with
Lockd acquired via with
Lock acquired directly
Lock acquired directly
Lock acquired directly
Lock acquired directly
Lock acquired directly
Lock acquired directly
Lock acquired directly
Lock acquired directly
Lock acquired directly

```

## 3. Semaphore
Semaphore用来控制对共享资源的访问数量，例如池的最大连接数。

$ ./test8.py
```python
import multiprocessing
import time
 
def worker(s, i):
    s.acquire()
    print(multiprocessing.current_process().name + "acquire");
    time.sleep(i)
    print(multiprocessing.current_process().name + "release\n");
    s.release()
 
if __name__ == "__main__":
    s = multiprocessing.Semaphore(2)
    for i in range(5):
        p = multiprocessing.Process(target = worker, args=(s, i*2))
        p.start()
```