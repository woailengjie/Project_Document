# python 中的并发编程-多线程

​		随着CPU进入多核时代，我们使用的操作系统都是支持“多任务的操作系统”，这使得我们可以同时运行多个程序，也可以将一个程序分解为若干个相对独立的子任务，让多个子任务并发执行，缩短程序的执行时间，获得更高的执行效率，同时也让用户获得更好的体验



**1秒即永恒**
		对人类来说，`1天=24 * 60 * 60 =86400秒`，一天和1秒也就相差4个数量级，`1年=31536000秒`，1年和1秒相差8个数量级

​		在高速处理计算的CPU来说，而`1GHz=10^9Hz`，即我们知道一个程序就是一些代码行，每个代码行又会被翻译成一条条的指令交给计算机执行，如果一个时钟周期就能执行一条指令，那一条指令的执行时间就是1纳秒，一条指令的执行时间一般就`几纳秒~几十纳秒`(*涉及指令周期，不过多介绍*)
CPU执行一条指令的时间在纳秒级,而`1秒=10^9纳秒`，相差9个数量级，这就意味着站在CPU的视角，对我们人类而言转瞬即逝的1秒钟，CPU感觉比1年还要长，由于我们对时间的感知跟高速计算的CPU相比完全不在一个维度，得益于CPU极高的处理速度，想要充分利用CPU的速度，提高效率于是有了下面两个概念
**并发与并行**

- 并发(concurrency)：并发的本质其实是在单核CPU的计算机中，操作系统可以迅速的切换这个处理器所运行的程序，但某一时刻最多只有一个程序在运行，但其实只是因为CPU的速度之快，让我们感觉同时时刻CPU同时做了几件事情

- 并行(parallelism)：对于多核CPU而言，本质是计算机确实能够在同一时间执行多个任务



## 进程与线程
### 进程
`操作系统进行资源分配的最小单位`
		进程是是一个动态的概念，当程序被操作系统调度起来的时候，这个程序文件才有资格被称之为进程，也就是说当你没有打开QQ之前，QQ这个软件只是存储在你磁盘中的一个可执行文件，和你看的电影`.mp4`文件，写的文档文件`.txt`没啥本质区别，当你双击打开之后QQ就是你电脑中的一个进程，你的操作系统就开始为这个进程分配存储空间

### 线程

`CPU进行调度和执行的最小单位`





## python中的多线程

#### 1. 使用Thread类创建线程对象

- 使用`Thread`类构造器创建线程对象，线程对象的`start()`方法启动一个线程，线程启动后（并获得`CPU`的调度）会执行`target`参数指定的函数
- 如果`target`指定的线程要执行的目标函数有参数，需要通过`args`参数进行指定（以元组形式传参），对于关键字参数也可通过`kwargs`参数传入

##### 看不见的主线程

在下面的程序中一共有两个线程，一个主线程，一个子线程

```python
from threading import Thread

num = 0


def add_num(count):
    global num		# num为全局变量
    while num < count:
        num += 1


t = Thread(target=add_num, args=(1000000,))	# 创建子线程
t.start()		

print(num)		# 打印结果,观察每次结果是否一致
```

> 注1：使用Thread类实例化线程对象创建的线程属于子线程，我们运行的这个`.py`程序就是一个进程，一个进程中的任务默认是由这个进程中的 **主线程MainThread** 从上到下去执行代码的
>
> 注2：调用start()方法，线程进入就绪状态，此时线程获得除了CPU之外的一切资源，等待CPU调度，此时线程并未开始执行，CPU调度的时间是不确定的，这是由操作系统决定的
>
> 注3：每次打印输出的结果都是不同的，这是因为子线程被CPU调度的时机是不确定的，主线程和子线程轮流获得CPU资源，所以主线程打印出的结果也是不确定的，可以执行最后一条语句打印的时候子线程还未开始被调度，或者已经调度执行了一会儿，也有可能执行完毕

##### 主线程等待

`.join():主线程阻塞，等待当前线程的任务执行完毕后再继续向下执行`

​		有些场景下我们想要的是所有子线程执行完毕后再接着往后执行，如执行完所有的下载任务再输出整个下载操作的时间

```python
from random import randint
from threading import Thread
from time import time, sleep


def download(filename):
    print(f"开始下载音乐文件:{filename}")
    download_time = randint(5, 10)		# 随机生成一个数
    sleep(download_time)			# 模拟下载过程中等待的时间
    print(f"{filename}下载完成,共花费 {download_time} 秒")
    
start = time()		# 主线程记录起始时间

th1 = Thread(target=download, args=('七里香.mp3', ))
th2 = Thread(target=download, args=('晴天.mp3', ))
th3 = Thread(target=download, args=('最伟大的作品.mp3', ))
th1.start()	
th2.start()
th3.start()

# --------------------join()的位置不能乱放哦--------------
th1.join()		# th1线程执行完毕才能往后走
th2.join()		# th2线程执行完毕才能往后走
th3.join()		# th3线程执行完毕才能往后走
# ------------------------------------------------------


end = time()	# 主线程记录结束时间
print(f"下载三首歌曲一共花费的时间为:{end - start} 秒")
```



> 注：这里非常容易把主线程和子线程的阻塞搞混，执行`th1.join()`后`th2和th3线程`会不会阻塞等待`th1线程`执行完毕呢?
>
> 这三个线程对象分别调用 `join()` 方法是阻塞主线程，让主线程等自己执行完毕后再接着往后执行，而这三个子线程的切换调度执行并不会阻塞，因为三个子线程都已经执行完`start()`方法准备就绪，由操作系统调度分配CPU运行

#### 2. 继承Thread类自定义线程

`继承Thread类并重写run()方法自定义线程`

```python
from random import randint
import time
from threading import Thread


class DownloadThread(Thread):
    def __init__(self, filename):
        self.filename = filename
        super().__init__()  # 使用父类的初始化方法进行初始化

    def run(self):	# 重写父类Thread中的run方法自定义线程执行的函数
        start = time.time()
        print(f"开始下载音乐文件:{self.filename} ...")
        time.sleep(randint(5, 10))
        print(f"{self.filename} 下载完成！")
        end = time.time()
        print(f"下载{self.filename}耗时: {end - start} 秒")


mp4_files = ["七里香.mp4", "简单爱.mp4", "以父之名.mp4"]

# 使用列表推导式生成三个自定义的线程对象
threads = [DownloadThread(mp4_file) for mp4_file in mp4_files]

start = time.time()
for thread in threads:
    thread.start()  # 启动线程准备CPU调度

for thread in threads:
    thread.join()  # 阻塞主线程,等待子线程执行完后才能接着往下执行

end = time.time()
print(f"下载所有音乐一共耗时: {end - start} 秒")
```



#### 3. 使用线程池

> 线程池在程序运行时创建大量空闲的线程，程序只需将一个函数提交给线程池，线程池就会启动一个空闲的线程来执行它，当该函数执行结束后，该线程并不被kill掉，而是再次返回到线程池中变成空闲状态，等待执行下一个函数

在实际开发中，线程的创建和释放都会带来较大的开销，（线程之间的上下文切换）频繁的创建和释放线程通常不是一个很好的选择，所以可以提前准备若干个线程，在使用中不需要自己写代码创建和释放线程，而是直接`复用线程池中的线程`

`python内置的concurrent.future模块提供了对线程池的支持`

>使用线程池可以有效的控制系统中并发线程的数量，无限的创建线程可能会导致Python解释器崩溃
>
>使用线程池管理并发编程，只要将相应的task函数提交给线程池，剩下的事情由线程池搞定

使用线程池来执行线程任务的步骤如下:

- 调用`ThreadPoolExecutor`类的构造器创建一个线程池
- 定义一个普通函数作为线程的任务
- 调用`ThreadPoolExecutor `对象的` submit() `方法来提交线程任务

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor


def task(mp4_url):
    """
    mp4_url:下载歌曲的链接
    """
    print(f"开始下载 {mp4_url} 歌曲")
    time.sleep(5)
    return random.randint(0, 10)

def task_done(response):
    print("任务执行后的返回值:")

# 创建线程池，最多维护5个线程
pool = ThreadPoolExecutor(5)

# 使用列表推导式构造20条虚假的歌曲链接
url_list = [f"https://www.flase-kugou-{i}" for i in range(20)]

for url in url_list:
    pool.submit(task, url)

# 调用 shutdown() 方法后的线程池不再接收新任务,但会将以前所有的已提交任务执行完成
pool.shutdown(True)		# 大家可以注释掉和取消注释这一行看看程序执行效果
# 关闭线程池: 让主线程等待所有任务执行完成再执行,类似于之前的 join() 方法阻塞主线程

print("继续往下走~")
print("所有歌曲下载完毕!")
    
```

`submit(fn, *args):将fn函数提交给线程池,*args代表传给fn函数的参数`

> 程序将 `task` 函数 `submit` 给线程池后，`submit` 方法返回一个Future对象，Future类主要用于获取线程任务函数的返回值

多说无益，上代码看效果

`应用场景1: 分工合作，task专门负责下载，done专门负责将下载的数据写入本地文件`

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor


def task(mp4_url):
    """
    mp4_url:下载歌曲的链接
    """
    print(f"开始下载 {mp4_url} 歌曲")
    time.sleep(5)
    return random.randint(0, 10)


def task_done(response):
    print(f"任务执行后的返回值: {response.result()}")


# 创建线程池，最多维护10个线程
pool = ThreadPoolExecutor(5)

# 使用列表推导式构造20条虚假的歌曲链接
url_list = [f"https://www.flase-kugounusic-{i}" for i in range(20)]

for url in url_list:
    future = pool.submit(task, url)		# 
    future.add_done_callback(task_done)

pool.shutdown(True)
print("继续往下走~")
print("所有歌曲下载完毕!")
```

#### 4. 资源竞争与线程安全

`一个进程中可以有多个线程, 且线程共享所有进程中的资源`

> 在多个线程竞争同一个资源的情况下，如果没有合理的机制来保护被竞争的资源，可能会出现数据紊乱，程序达不到我们预期的效果

资源竞争示例如下：

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor


class Account(object):
    """银行账户"""

    def __init__(self):
        self.balance = 0.0  # 表示现有余额

    def deposit(self, save_money):
        new_balance = self.balance + save_money  # 新的余额等于旧的余额+存进去的money
        time.sleep(random.uniform(0.01, 0.9))   # 模拟一个0.01~0.9s的随机延时
        self.balance = new_balance			# 更新现有余额

        
account = Account()  # 实例化一个银行账户类

pool = ThreadPoolExecutor(5)
for _ in range(20):
    pool.submit(account.deposit, 100)

pool.shutdown(True)
print(account.balance)	# 请大家多运行几次看看每次输出结果是否一致
```

> 这里通过线程池的方式启动了20个线程向同一个账户转账100元，按理来说最后的账户余额应该是20000元才对，大家运行之后可以看到每次的结果并不一致，这是因为程序的执行是并发+异步，每个线程的执行顺序是由操作系统调度的，**不可预知**，假设当001号线程执行到第12行刚把money存进去，还未执行第14行更新现有余额的时候，此时002号线程也开始执行到第12行，但此时002号线程取出的钱是旧的余额，基于旧余额加100元，两个线程都执行完第14行后本来应该存进去的200元结果变成100元
>
> 即“丢失更新”现象，之前线程修改数据的结果被后序线程修改的结果给覆盖掉了，得不到正确的结果

上面的代码中由于存在资源竞争导致数据达不到预期，这样的线程是不安全的，故`python`的`threading`模块提供了两种锁，`Lock和RLock锁`，*关于这两种锁的区别在这里不做介绍*，感兴趣的朋友可以自行搜索

##### 线程加锁

线程安全代码示例: `相较于上个示例一共就多了四行代码，大家不要偷懒，赶紧CV过去多运行几次看看效果`

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor
from threading import RLock


class Account(object):
    """银行账户"""

    def __init__(self):
        self.balance = 0.0  # 表示现有余额
        self.lock = RLock()

    def deposit(self, save_money):
        self.lock.acquire()        # 获得锁
        
        new_balance = self.balance + save_money  # 新的余额等于旧的余额+存进去的money
        time.sleep(random.uniform(0.01, 0.9))   # 模拟一个0.01~0.9s的随机延时
        self.balance = new_balance			# 更新现有余额
        
		self.lock.release()		# 释放锁
        
account = Account()  # 实例化一个银行账户类

pool = ThreadPoolExecutor(5)
for _ in range(20):
    pool.submit(account.deposit, 100)

pool.shutdown(True)
print(account.balance)
```



#### 5. GIL锁问题

**GIL锁**：`Global Interpreter Lock:全局解释器锁(Cpython解释器独有)` 是一个`防止多线程并发执行的互斥锁 `，在同一时间,python解释器只能运行一个线程的代码, 保证进程中同一时刻只有一个线程在执行

`问1:为什么要设置 GIL 锁, 又要并发(当婊子)，又要加锁(立牌坊)？`

答: 在没有**GIL**锁的情况下，若多个线程同时执行某个任务，当**该任务中某个对象的引用计数为0，垃圾回收机制对改对象进行回收，其他线程再次引用改对象则会报错**

`问2: 有GIL锁线程就一定安全了吗？`

答: 并没有**,GIL**锁在以下情况下会自动释放(如果某个线程获得锁不释放, 那其他线程永远没有运行的机会),由于存在强制释放这种情况, 还是会存在上面的那种竞争资源导致数据紊乱的情况, **故要保证线程安全还是得手动加锁 !**

> GIL锁的释放：
>
> - CPython解释器计算当前执行的字节数量，达到一定阈值后强制释放GIL
> - 操作系统分配的时间片用完后释放GIL
> - 遇到IO操作时释放

`问3:由于GIL锁存在,即使多线程并发处理任务,但是最终只有一个线程在工作,那python中的多线程还有啥用?  `

答:在多线程中,只有当线程获得一个GIL,该线程的代码才能运行,**而一个进程中只有一个GIL锁**,故在一个进程中即使使用python多线程编程,在同一时刻也只有一个线程在运行,因此即使在多核情况下也只能发挥出单核的性能~

`注: 即使有多个处理器,由于GIL锁的存在同一时刻也只有一个线程在运行,故python中的多线程没有真正的并行`

作用:

对 `IO密集型任务` , 即便有GIL, 但是IO操作会导致GIL释放,其他线程得以获得执行权限,所以对IO密集型任务,多线程对提升效率还是有点作用的

对 `计算密集型任务` , 由于CPU一直处于被占用状态,GIL锁直到时间片用完后才会切换状态,使用多线程没有意义,反而还要切换线程降低效率,此时可以使用多进程来处理

> 计算密集型任务和IO密集型任务:
>
> 计算密集型任务: 顾名思义,对于涉及大量数值计算,或者对视频进行高清解码,大型文件的压缩和解压缩都涉及到大量计算, CPU在处理密集型任务是是全程在忙碌的
>
> IO密集型任务: 发起网络请求等待响应, 进行磁盘IO读写文件, CPU只要执行发起任务的指令,任务的大部分时间CPU都是处于空闲状态,等待IO操作完成



`问4:由于GIL锁的存在,如何发挥CPU的多核优势 ?`

> 如果希望发挥CPU的多核优势,可以使用多进程, 因为每个进程对应一个Python解释器, 因此每个进程都有自己独立的GIL,这样就可以突破GIL的限制



演示:计算密集型任务用多线程和多进程演示程序执行时间

`实在想不出好的案例，下面这个案例是从网上借鉴的`

```python
import concurrent.futures
import math
import time

PRIMES = [
    1116281,
    1297337,
    104395303,
    472882027,
    533000389,
    817504243,
    982451653,
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419
] * 5


# 判断素数逻辑不明白没关系，涉及到一定的算法，你只需要知道这是一个计算密集型的任务
def is_prime(n):
    """判断素数"""
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))      # 将 n 开根号向下取整再转换为 int
    for i in range(3, sqrt_n + 1, 2):       # 判断一个数为素数
        if n % i == 0:
            return False
    return True


def main():
    """主函数"""
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # 关于zip函数和map函数的用法不熟悉的请自行了解
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))
    end = time.time()
    print(f"总的执行时间{end - start}秒")


if __name__ == '__main__':
    main()
```

> 从上面案例中我们可以看到：
>
> 当你把37行的`concurrent.futures.ProcessPoolExecutor()` 换成 `concurrent.futures.ThreadPoolExecutor()` 后打印执行时间可以看到对计算密集型的任务只能使用多进程来提高速度，多线程无法提升计算密集型任务的效率，当然你得根据你的电脑是几核的来决定进程池中进程的数量，一个进程占用一个CPU内核做到真正的并行
>
> 

#### 6.死锁问题

> 简单来讲，程序需要获得①号资源和②号资源才能往下运行，而在并发执行的线程中，由于`异步性即程序向前推进的顺序是不确定的`，线程A获得①号资源，线程B获得②号资源，两个线程各自等待对方手里的资源，并且均不释放自己手中已有的资源导致程序无法往下推进导致死锁



## 总结

到这里,python中的多线程编程最基础的部分就到此为止啦，码字不易，如果你觉得对你有用的话还请点个赞啦！！！













