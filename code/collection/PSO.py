import random
import math
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA

# 定义一个修饰器函数用来统计函数的运行时间
# 参考我的csdn  https://blog.csdn.net/prinTao/article/details/121800857?spm=1001.2014.3001.5501
import time
def timmer(func):    #传入的参数是一个函数
    def deco(*args, **kwargs): #本应传入运行函数的各种参数
        print('\n函数：{_funcname_}开始运行：'.format(_funcname_=func.__name__))
        start_time = time.time()#调用代运行的函数，并将各种原本的参数传入
        res = func(*args, **kwargs)
        end_time = time.time()
        print('函数:{_funcname_}运行了 {_time_}秒'
              .format(_funcname_=func.__name__, _time_=(end_time - start_time)))
        return res#返回值为函数
    return deco

class PSO(object):
    def __init__(self, num_city, mat):
        self.iter_max = 500  # 迭代数目
        self.num = 200  # 粒子数目
        self.num_city = num_city  # 城市数
        #self.location = data # 城市的位置坐标
        # 计算距离矩阵
        self.dis_mat = np.array(mat)  # 计算城市之间的距离矩阵
        # 初始化所有粒子
        # self.particals = self.random_init(self.num, num_city)
        self.particals = self.greedy_init(self.dis_mat,num_total=self.num,num_city =num_city)
        self.lenths = self.compute_paths(self.particals)
        # 得到初始化群体的最优解
        init_l = min(self.lenths)
        init_index = self.lenths.index(init_l)
        init_path = self.particals[init_index]
        # 画出初始的路径图
        #init_show = self.location[init_path]
        # 记录每个个体的当前最优解
        self.local_best = self.particals
        self.local_best_len = self.lenths
        # 记录当前的全局最优解,长度是iteration
        self.global_best = init_path
        self.global_best_len = init_l
        # 输出解
        self.best_l = self.global_best_len
        self.best_path = self.global_best
        # 存储每次迭代的结果，画出收敛图
        self.iter_x = [0]
        self.iter_y = [init_l]

    def greedy_init(self, dis_mat, num_total, num_city):
        """    贪婪搜索算法
        dis_mat：
            邻接矩阵
        num_total：
            搜索次数
        num_city：
            城市数
        """
        start_index = 0
        result = []
        for i in range(num_total):
            rest = [x for x in range(0, num_city)]
            # 所有起始点都已经生成了
            if start_index >= num_city:
                start_index = np.random.randint(0, num_city)
                result.append(result[start_index].copy())
                continue
            current = start_index
            rest.remove(current)
            # 找到一条最近邻路径
            result_one = [current]
            while len(rest) != 0:
                tmp_min = math.inf
                tmp_choose = -1
                for x in rest:
                    if dis_mat[current][x] < tmp_min:
                        tmp_min = dis_mat[current][x]
                        tmp_choose = x

                current = tmp_choose
                result_one.append(tmp_choose)
                rest.remove(tmp_choose)
            result.append(result_one)
            start_index += 1
        return result

    
    def random_init(self, num_total, num_city):
        """# 随机初始化
        """
        tmp = [x for x in range(num_city)]
        result = []
        for i in range(num_total):
            random.shuffle(tmp)
            result.append(tmp.copy())
        return result

    def compute_pathlen(self, path, dis_mat):
        """# 计算一条路径的长度
        """
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result
    
    def compute_paths(self, paths):
        """
        # 计算一个群体的长度
        """
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result
    
    def eval_particals(self):
        """# 评估当前的群体
        """
        min_lenth = min(self.lenths)
        min_index = self.lenths.index(min_lenth)
        cur_path = self.particals[min_index]
        # 更新当前的全局最优
        if min_lenth < self.global_best_len:
            self.global_best_len = min_lenth
            self.global_best = cur_path
        # 更新当前的个体最优
        for i, l in enumerate(self.lenths):
            if l < self.local_best_len[i]:
                self.local_best_len[i] = l
                self.local_best[i] = self.particals[i]

    
    def cross(self, cur, best):
        """# 粒子交叉
        """
        # 新建一个，防止改了基础版
        one = cur.copy()
        l = [t for t in range(self.num_city)]
        t = np.random.choice(l,2)
        cross_part = best[min(t):max(t)]
        # 检查是不是目标位置的
        tmp = []
        for t in one:
            if t in cross_part:
                continue
            tmp.append(t)
        # 两种交叉方法
        one = tmp + cross_part
        l1 = self.compute_pathlen(one, self.dis_mat)
        one2 = cross_part + tmp
        l2 = self.compute_pathlen(one2, self.dis_mat)
        if l1<l2:
            return one, l1
        else:
            return one, l2

    def mutate(self, one):
        """    # 粒子变异
        """
        # 新建一个，防止改了基础版
        one = one.copy()
        # 正序排列数组
        l = [t for t in range(self.num_city)]
        t = np.random.choice(l, 2)
        x, y = min(t), max(t)
        one[x], one[y] = one[y], one[x]
        l2 = self.compute_pathlen(one,self.dis_mat)
        return one, l2

    def pso(self):
        """    # 迭代操作
        """
        for cnt in range(1, self.iter_max):
            # 更新粒子群
            for i, one in enumerate(self.particals):
                tmp_l = self.lenths[i]
                # 与当前个体局部最优解进行交叉
                new_one, new_l = self.cross(one, self.local_best[i])
                if new_l < self.best_l:
                    self.best_l = tmp_l
                    self.best_path = one
                # 加入随机因素
                if new_l < tmp_l or np.random.rand()<0.1:
                    one = new_one
                    tmp_l = new_l

                # 与当前全局最优解进行交叉
                new_one, new_l = self.cross(one, self.global_best)
                # 是否更新
                if new_l < self.best_l:
                    self.best_l = tmp_l
                    self.best_path = one
                # 加入随机因素
                if new_l < tmp_l or np.random.rand()<0.1:
                    one = new_one
                    tmp_l = new_l
                # 变异
                one, tmp_l = self.mutate(one)
                # 是否更新
                if new_l < self.best_l:
                    self.best_l = tmp_l
                    self.best_path = one
                # 加入随机因素
                if new_l < tmp_l or np.random.rand()<0.1:
                    one = new_one
                    tmp_l = new_l

                # 更新该粒子
                self.particals[i] = one
                self.lenths[i] = tmp_l

            # 评估粒子群，更新个体局部最优和个体当前全局最优
            self.eval_particals()
            # 更新输出解
            if self.global_best_len < self.best_l:
                self.best_l = self.global_best_len
                self.best_path = self.global_best
            print(cnt, self.best_l)
            self.iter_x.append(cnt)
            self.iter_y.append(self.best_l)
        return self.best_l, self.best_path
    @timmer
    def run(self):
        best_length, best_path = self.pso()
        # 画出最终路径
        return best_path, best_length


if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from dataloader.Dataloader_for_TSP_datasets import TSP_DATA
    datapath = r'D:\0latex\System_engineering_programm\TSP_tst_data\bayg29.tsp.gz'
    data = TSP_DATA(datapath)
    model = PSO(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    # 画图
    iterations = model.iter_x
    best_record = model.iter_y
    plt.plot(iterations,best_record)
    plt.show()

