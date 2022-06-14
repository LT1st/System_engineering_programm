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

class TS(object):
    def __init__(self, num_city, mat):
        self.taboo_size = 5
        self.iteration = 500
        self.num_city = num_city
        #self.location = data
        self.taboo = []

        self.dis_mat = np.array(mat)
        self.path = self.greedy_init(self.dis_mat,100,num_city)
        self.best_path = self.path
        self.cur_path = self.path
        self.best_length = self.compute_pathlen(self.path, self.dis_mat)

        # 显示初始化后的路径
        init_pathlen = 1. / self.compute_pathlen(self.path, self.dis_mat)
        # 存储结果，画出收敛图
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
        # return result[0]

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

    # 计算一个群体的长度
    def compute_paths(self, paths):
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result

    # 产生随机解
    def ts_search(self, x):
        moves = []
        new_paths = []
        while len(new_paths)<400:
            i = np.random.randint(len(x))
            j = np.random.randint(len(x))
            tmp = x.copy()
            tmp[i:j] = tmp[i:j][::-1]
            new_paths.append(tmp)
            moves.append([i, j])
        return new_paths, moves

    # 禁忌搜索
    def ts(self):
        for cnt in range(self.iteration):
            new_paths, moves = self.ts_search(self.cur_path)
            new_lengths = self.compute_paths(new_paths)
            sort_index = np.argsort(new_lengths)
            min_l = new_lengths[sort_index[0]]
            min_path = new_paths[sort_index[0]]
            min_move = moves[sort_index[0]]

            # 更新当前的最优路径
            if min_l < self.best_length:
                self.best_length = min_l
                self.best_path = min_path
                self.cur_path = min_path
                # 更新禁忌表
                if min_move in self.taboo:
                    self.taboo.remove(min_move)

                self.taboo.append(min_move)
            else:
                # 找到不在禁忌表中的操作
                while min_move in self.taboo:
                    sort_index = sort_index[1:]
                    min_path = new_paths[sort_index[0]]
                    min_move = moves[sort_index[0]]
                self.cur_path = min_path
                self.taboo.append(min_move)
            # 禁忌表超长了
            if len(self.taboo) > self.taboo_size:
                self.taboo = self.taboo[1:]
            self.iter_x.append(cnt)
            self.iter_y.append(self.best_length)
            print(cnt, self.best_length)
        print(self.best_length)

    @timmer
    def run(self):
        self.ts()
        return self.best_path, self.best_length


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
    data = TSP_DATA(datapath)
    model = TS(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    # 画图
    iterations = model.iter_x
    best_record = model.iter_y
    plt.plot(iterations,best_record)
    plt.show()