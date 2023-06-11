# python 中的并发编程

​		随着CPU进入多核时代，我们使用的操作系统都是支持“多任务的操作系统”，这使得我们可以同时运行多个程序，也可以将一个程序分解为若干个相对独立的子任务，让多个子任务并发执行，缩短程序的执行时间，获得更高的执行效率，同时也让用户获得更好的体验



**1秒即永恒**
		对人类来说，`1天=24 * 60 * 60 =86400秒`，一天和1秒也就相差4个数量级，`1年=31536000秒`，1年和1秒相差8个数量级

​		在高速处理计算的CPU来说，而`1GHz=10^9Hz`，即我们知道一个程序就是一些代码行，每个代码行又会被翻译成一条条的指令交给计算机执行，一条指令的执行时间一般就`几纳秒~几十纳秒`(*涉及指令周期，不过多介绍*)
CPU执行一条指令的时间在纳秒级， 一般一个3.6GHz频率的CPU
`1秒=10^9纳秒`，相差9个数量级，这就意味着站在CPU的视角，对我们人类而言转瞬即逝的1秒钟，CPU感觉比1年还要长

由于我们对时间的感知跟高速计算的CPU相比完全不在一个维度，得益于CPU极高的处理速度，想要充分利用CPU的速度，提高效率于是有了下面两个概念
**并发与并行**

- 并发(concurrency)：并发的本质其实是在单核CPU的计算机中，操作系统可以迅速的切换这个处理器所运行的程序，但某一时刻最多只有一个程序在运行，但其实只是因为CPU的

- 并行(parallelism)：对于多核CPU而言，本质是计算机确实能够在同一时间执行多个任务



## 进程与线程
### 进程
`操作系统进行资源分配的最小单位`
		进程是是一个动态的概念，当程序被操作系统调度起来的时候，这个程序文件才有资格被称之为进程，也就是说当你没有打开QQ之前，QQ这个软件只是存储在你磁盘中的一个可执行文件，和你看的电影`.mp4`文件，写的文档文件`.txt`没啥本质区别，当你双击打开之后QQ就是你电脑中的一个进程，你的操作系统就开始为这个进程分配存储空间

### 线程

#### 

待完善







## python中的多进程

待完善









## python中的多线程

#### 使用Thread类创建线程对象

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

> 注1：使用Thread类实例化线程对象创建的线程属于子线程，我们运行的这个`.py`程序就是一个进程，一个进程中的任务默认是由这个进程中的主线程（MainThread）从上到下去执行代码的
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

#### 继承Thread类自定义线程

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



#### 使用线程池

> 线程池在程序运行时创建大量空闲的线程，程序只需将一个函数提交给线程池，线程池就会启动一个空闲的线程来执行它，当该函数执行结束后，该线程并不被kill掉，而是再次返回到线程池中变成空闲状态，等待执行下一个函数

在实际开发中，线程的创建和释放都会带来较大的开销，（线程之间的上下文切换）频繁的创建和释放线程通常不是一个很好的选择，所以可以提前准备若干个线程，在使用中不需要自己写代码创建和释放线程，而是直接复用线程池中的线程

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
# pool.shutdown(True)		# 大家可以注释掉和取消注释这一行看看程序执行效果
# 关闭线程池: 让主线程等待所有任务执行完成再执行,类似于之前的 join() 方法阻塞主线程

print("继续往下走~")
print("所有歌曲下载完毕!")
    
```

`submit(fn, *args):将fn函数提交给线程池,*args代表传给fn函数的参数`

> 程序将 `task` 函数 `submit` 给线程池后，`submit` 方法返回一个Future对象，Future类主要用于获取线程任务函数的返回值

多说无益，上代码看效果

`应用场景：分工合作，task专门负责下载，done专门负责将下载的数据写入本地文件`

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
url_list = [f"https://www.flase-kugou-{i}" for i in range(20)]

for url in url_list:
    future = pool.submit(task, url)
    future.add_done_callback(task_done)

pool.shutdown(True)
print("继续往下走~")
print("所有歌曲下载完毕!")
```

