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


class SA(object):
    def __init__(self, num_city, mat):
        self.T0 = 4000
        self.Tend = 1e-3
        self.rate = 0.9995
        self.num_city = num_city
        self.scores = []
        #self.location = data
        # fruits中存每一个个体是下标的list
        self.fires = []
        #self.dis_mat = self.compute_dis_mat(num_city, data)
        self.dis_mat = np.array(mat)
        self.fire = self.greedy_init(self.dis_mat,100,num_city)
        # 显示初始化后的路径
        init_pathlen = 1. / self.compute_pathlen(self.fire, self.dis_mat)
        #init_best = self.location[self.fire]
        # 存储存储每个温度下的最终路径，画出收敛图
        self.iter_x = [0]
        self.iter_y = [1. / init_pathlen]
        
    def greedy_init(self, dis_mat, num_total, num_city):
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
        pathlens = self.compute_paths(result)
        sortindex = np.argsort(pathlens)
        index = sortindex[0]
        return result[index]

    # 初始化一条随机路径
    def random_init(self, num_city):
        tmp = [x for x in range(num_city)]
        random.shuffle(tmp)
        return tmp

    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算路径长度
    def compute_pathlen(self, path, dis_mat):
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    # 计算一个温度下产生的一个群体的长度
    def compute_paths(self, paths):
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result

    # 产生一个新的解：随机交换两个元素的位置
    def get_new_fire(self, fire):
        fire = fire.copy()
        t = [x for x in range(len(fire))]
        a, b = np.random.choice(t, 2)
        fire[a:b] = fire[a:b][::-1]
        return fire

    # 退火策略，根据温度变化有一定概率接受差的解
    def eval_fire(self, raw, get, temp):
        len1 = self.compute_pathlen(raw, self.dis_mat)
        len2 = self.compute_pathlen(get, self.dis_mat)
        dc = len2 - len1
        p = max(1e-1, np.exp(-dc / temp))
        if len2 < len1:
            return get, len2
        elif np.random.rand() <= p:
            return get, len2
        else:
            return raw, len1

    # 模拟退火总流程
    def sa(self):
        count = 0
        # 记录最优解
        best_path = self.fire
        best_length = self.compute_pathlen(self.fire, self.dis_mat)

        while self.T0 > self.Tend:
            count += 1
            # 产生在这个温度下的随机解
            tmp_new = self.get_new_fire(self.fire.copy())
            # 根据温度判断是否选择这个解
            self.fire, file_len = self.eval_fire(best_path, tmp_new, self.T0)
            # 更新最优解
            if file_len < best_length:
                best_length = file_len
                best_path = self.fire
            # 降低温度
            self.T0 *= self.rate
            # 记录路径收敛曲线
            self.iter_x.append(count)
            self.iter_y.append(best_length)
            print(count, best_length)
        return best_length, best_path
    
    @timmer
    def run(self):
        best_length, best_path = self.sa()
        return best_path, best_length


# 读取数据
def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from dataloader.Dataloader_for_TSP_datasets import TSP_DATA
    datapath = r'D:\0latex\System_engineering_programm\TSP_tst_data\bayg29.tsp.gz'
    # 获取数据加载类
    data = TSP_DATA(datapath)
    model = SA(num_city = data.DIMENSION , mat = data.matrix)
    # 运行算法
    path, path_len = model.run()
    # 画图
    iterations = model.iter_x
    best_record = model.iter_y
    plt.plot(iterations,best_record)
    plt.show()