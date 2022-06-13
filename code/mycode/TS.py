# -*- coding: utf-8 -*-
"""禁忌搜索算法解决tsp问题(final).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WkCjeRRS7c865NCn8-WB9OvwsBAs_f8J

# 问题解析
"""

# 从GoogLe Drive获取数据集，更换本地，需要data使用本地路径
from google.colab import drive
drive.mount('/content/drive/')
data = 'drive/MyDrive/现代优化计算方法/ftv47.atsp'

# 自动切换网上平台或者本地路径
import platform
check_sys = platform.system()
if check_sys == 'Linux':   # colab address
  pass
elif check_sys == 'Windows': # local address 
  data = './ftv47.atsp'
else:
  raise EnvironmentError

from numpy import*
import linecache
import itertools
from os import listdir, path
import sys
import math
import random
import matplotlib.pyplot as plt 
from tqdm import tqdm, trange

"""#  数据集"""

"""旅行推销员问题
这是旅行商问题的绘图解决方案的示例

用于产生解决方案的函数是 christofides，在给定一组节点的情况下，它计算旅行者必须遵循的节点的路线，以最小化总成本。

https://networkx.org/documentation/stable/auto_examples/drawing/plot_tsp.html#sphx-glr-auto-examples-drawing-plot-tsp-py
"""

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

def creatematrix_ATSP(sciezka):
    """
    func
        从文件读取距离矩阵
    sciezka 
        文件名 放在atsp文件夹下
    retrun
        atsp的距离矩阵
    """
    # 保证数据格式正确
    assert sciezka.split('.')[-1] == 'atsp'
    # file = path.join('atsp', sciezka)
    file = sciezka
    # file = 'atsp' + sciezka      # + 'ftv70.atsp'
    tekst = open(file).read()
    #print(tekst)
    tekst = tekst.split()
    #print(tekst)
    # 报错原因： 截取位置错误
    tekst = tekst[15:]
    #print(tekst)
    tekst.remove('EOF')
    dl = len(tekst)
    dimension = linecache.getline(file, 4)
    dimension = dimension[11:]
    dimension = int(dimension)
    # 报错原因 第一个数字丢失
    tab = zeros((dimension, dimension), int)
    # print(tab)

    # 计数器初始化
    counter = 0

    infinity = 100000

    for i in range(dimension):
        for j in range(dimension):
            #print(i*dimension+j)
            if tekst[counter] == '100000000': # '9999':100000000
                tekst[counter] = infinity
            # if tekst[counter]
            # 报错 由于这里的eof没有扔掉
            ## print(tekst[counter])
            tab[i][j] = int(tekst[counter])
            counter += 1
    return tab

import numpy as np

thisFile = data
tab = creatematrix_ATSP(thisFile)
tab_np = np.array(tab)


tab_list = list(tab_np)


import warnings
warnings.simplefilter('always')
def getDistance(tab, thisplace , nextplace, asymmetric=True):
    """
    func
        对于二维的非对称距离矩阵进行距离查询
    tab 
        距离矩阵（注意顺序）
    thisplace 
        当前所在的城市
    nexplace 
        目的地城市
    asymmetric
        是否是非对称距离矩阵，对称矩阵查询可优化
    """
    
    # 保证数据类型
    if not isinstance(tab,np.ndarray):
        warnings.warn('input distance matrix type ERROR , using a numpy array instead ', DeprecationWarning)
        tab = np.array(tab)
    # 保证二维矩阵
    assert len(tab.shape) == 2
    # 判断无穷大
    
    #todo
    # 法一： 返回负数就是走不通
    # 法二： 返回很大的数使得距离计算loss很大
    
    #todo
    # 查询使用哈希表应该更快
    
    return tab[thisplace][nextplace]

"""## 数据加载器的实验
使用numpy会慢一倍
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# getDistance(tab_np,1,2)

def getDis_list(tab_list, x, y):
  return tab_list[x][y]

# Commented out IPython magic to ensure Python compatibility.
# %%time
# getDis_list(tab_list,1,2)

"""assert type(tab_np) != 'numpy.ndarray'

# 问题转化（变成对称的TSP问题）
"""

# 使用list
def tansposeMatrix(matric):
    return [[matric[j][i] for j in range(len(matric))] for i in range(len(matric[0]))]

def ATSP2TSP(matric):
    """
    将传入的方阵转置 按照转化方法拼接为2m*2
    """
    # 用numpy能快点
    return matric.append(tansposeMatrix(matric))

a=np.array([[1,2,3],[1,5,4]])
b=np.array([[1,2,3],[1,5,4]])
np.concatenate((a, b),axis=0)

np.concatenate((a, b),axis=1)

# 使用numpy
# 为了使算法方便观察，没有使用节省内存和更快的写法，
# 但减少中间变量和新建数组，会显著加快程序运行
def ATSP2TSP_np(matrix):
    # 需要四个矩阵
    # left up
    lu = np.ones_like(matrix)*(10000)
    # ringt up 
    ru = matrix.T
    # right down
    rd = np.ones_like(matrix)*(10000)
    
    # 拼接矩阵
    # 先竖着拼接
    left = np.concatenate((lu,matrix),axis=0)
    right = np.concatenate((ru,rd),axis=0)
    
    # 整体拼接
    return np.concatenate((left, right),axis=1)

# 转换后的TSP问题邻接矩阵转换为list，加速距离读取
TSP_list = list (ATSP2TSP_np(tab_np))

TSP_list

"""# 生成初始解
def generate_first_solution(randomSeed):
    
    # 使用传入的随机数种子生成初始路径，保证可以复现
    
"""

tst  = [i for i in range(10)]
list(range(10))

c = {'value':[1,2,3], 'changed':[[1,2],[1,3],[2,5]]}

"""## 算法超参数"""

# 算法需要的变量

tabLength = 50                   # 禁忌表长
banned_Table = []                # 禁忌表

city_Num = tab_np.shape[0]            # 城市数
cityNum = tab_np.shape[0]

randSeed = 42                   # 随机数种子
random.seed(randSeed)               # 给random库设计随机数生成器

maxIter = 1000                  # 终止准则

neighborNum = 20000               # 生成的邻居数量

solution = list(range(city_Num)) # 解

solution_list = []               # 生成多个解构成的数组

exchange_Num  = 2                # 领域交换量 2-opt
# 当前路径长度（加一个变化的权重，路径长度和value不一样，非线性,比如平方）
# 加大对离谱解的惩罚力度，但要小心震荡
thisLength = 1000000
thisValue = 1000000

"""list(range(city_Num))"""

# 随机接受概率
random_accept= 0.05
random_accept



"""# 初始路径生成算法"""

def random_initial_route(remain_cities):
    '''
    随机生成初始路径
    '''
    initial_route = remain_cities[:]
    random.shuffle(initial_route)
    return initial_route

# 获取对应所有邻域的路径长度
# 给出最好的一个

def get_length_in_list(connection_list, distance_tab=tab_np):
    """获取一个链接的长度
    
    """
    dis=0
    length = len(connection_list)
    #print(connection_list)
    
    for j in range(length-1):
        #dis += getDistance(distance_tab,connection_list[j],connection_list[j+1])
        #print(length,j,getDis_list(tab_list, connection_list[j], connection_list[j+1]))
        #print(connection_list[j],connection_list[j+1])
        dis += getDis_list(tab_list, connection_list[j], connection_list[j+1])
    dis += getDis_list(tab_list, connection_list[length-1], connection_list[0])

    return dis
 

def cal_length_in_tab(connection_tab, distance_tab=tab_np,  p_value=1):
    '''获取一个链接表的长度
    connection_tab
        二维数组
    p_value 
        默认1范数
    dis_list
        一维数组
    '''
    # 一条路径的路径长度
    dis = 0
    
    # 顺序储存多条路径的总长度
    dis_list = []
    
    # 最优值
    bestPosition = 0
    
    # 有没有必要用二维数组索引来保存一个字典？？
    '''
    a = {(1,2):'r',(1,3):'b'}
    a[(2,3)]='s'
    '''
    thisdict = dict()
    
    # 1范数不需要计算，加速
    if p_value==1:
        for i in connection_tab:
            dis = 0
            for j in range(cityNum-1):
                #dis += getDistance(distance_tab,i[j],i[j+1])
                dis += getDis_list(tab_list,i[j],i[j+1])
            dis += getDis_list(tab_list,i[cityNum-1],i[0])
            dis_list.append(dis)
    else: 
        for i in connection_tab:
            for j in range(cityNum-1):
                dis = getDis_list(tab_list,i[j],i[j+1])
                # numpy范数计算需要float类型，那不然是错的
                dis = pow(dis,p_value)
            dis_list.append(dis)
        
    return dis_list

def get_best_index(dis_list):
    """返回最优距离的索引和最优值
    # todo：返回不是最优的几个，防止局部最优过拟合
    
    """
    return [dis_list.index(min(dis_list)),min(dis_list)]

improve_count = 60 #改良次数
route_mile_cost = get_length_in_list
@timmer
def improve_circle(remain_cities,improve_count=70):
    '''
    改良算法生成初始路径
    '''
    # get_length_in_list
    initial_route = remain_cities[:]
    random.shuffle(initial_route)
    cost0 = route_mile_cost(initial_route)
    route = [1] + initial_route + [1]
    label = list(i for i in range(1,len(remain_cities)))
    j = 0
    while j < improve_count:
        new_route = route[:]
        index0,index1 = random.sample(label,2)
        new_route[index0],new_route[index1]= new_route[index1],new_route[index0]
        cost1 = route_mile_cost(new_route[1:-1])
        improve = cost1 - cost0
        #交换两点后有改进
        if improve < 0: 
            route = new_route[:]
            cost0 = cost1
            j += 1
        else:
            continue
    initial_route = route[1:-1]
    return initial_route,cost0

solution = list(range(city_Num))
origin = 1 # 起点和终点城市
remain_cities = solution[:]
remain_cities.remove(origin) #迭代过程中变动的城市

tab_list[44][41]

def nearest_city(current_city,cand_cities):
    '''
    找寻离当前城市最近的城市
    '''
    temp_min = float('inf')
    next_city = None
    for i in range(len(cand_cities)):
        # 遍历候选城市
        distance = tab_list[current_city][cand_cities[i]]
        if distance < temp_min:
            # 更新当前最小
            temp_min = distance
            next_city = cand_cities[i]
    #print(current_city,next_city, temp_min)
    return next_city,temp_min

origin = 1          # 起点和终点城市
remain_cities = solution[:] # 起始list
remain_cities.remove(origin) # 迭代过程中变动的城市

def greedy_initial_route(all_cities):
    '''寻找每次最近的城市
    '''
    current_city = random.randint(1,city_Num)
    #print(current_city)
    all_cities = all_cities.copy()
    try:
      all_cities.remove(current_city)
    except:
      all_cities = list(range(city_Num))
      random.shuffle(all_cities)
    cand_cities = all_cities[:]
    
    mile_cost = 0
    initial_route = []
    initial_route.append(current_city)
    cnt = 0 
    while len(cand_cities) > 0:
        cnt = cnt +1
        # print(cnt)
        # 找寻最近的城市及其距离
        next_city,distance = nearest_city(current_city,cand_cities) 
        mile_cost += distance
        initial_route.append(next_city)  # 将下一个城市添加到路径列表中
        current_city = next_city     # 更新当前城市
        cand_cities.remove(next_city)   # 更新未定序的城市
    # 计算初始到结束
    mile_cost += tab_list[initial_route[-1]][initial_route[0]] 
    return initial_route,mile_cost

"""测试初始化城市的时间、初次优化位置
贪婪算法最好
"""

newlist = list(range(city_Num))
random.shuffle(newlist)


"""bremain_cities"""

# 生成初始化解（以何种方式打乱数组）
def  generate_first_solution(method = 'greedy',interCnt=75):
    newlist = list(range(city_Num))
    random.shuffle(newlist)
    if method == 'random_shuffle':
        remain_cities = newlist
        initial_route = remain_cities[:]
        random.shuffle(initial_route)
        
    elif method == 'improved_circle':
        initial_route = improve_circle(newlist,interCnt)
        
    elif method == 'greedy':
        initial_route = greedy_initial_route(newlist)
        
    else:
        raise Exception("初始化方法不存在")
    
    return initial_route

"""# 生成邻居
散度可不可以用？？

"""

'''
# 按照规则寻找所有邻域，生成二维数组
# axis0为一种方法 axis1为对应的交换
# 需要交换被记录
'''

# 注意交换方式不同，如果使用的是非对称问题，那么交换就要多出非对称的一半
def generate_neighborhood(nowSolution, method = '2-opt', asymmetry=True):
    '''
    nowSolution
        一维数组，表示当前的解状态
    func
        注意 
            由于禁止表、破禁准则，因此这里返回的是全部可能交换方式
        2-OPT 邻域生成
            不和自己交换
            list的索引和城市序号不同，交换表需要用城市序号
    return 
        （要不要用字典？？实现方法有点多）
        交换的结果
        交换的是哪两个 ：用真实的城市编号来表示
    '''
    # 对list第一层实现深拷贝
    #exchange_tmp = nowSolution.copy()
    # 交换结果表
    exchange_Tab = []
    # 交换的对应是哪个
    exchange_State = []
    lenth = len(nowSolution)
    
    if asymmetry:
        for i in range(lenth):
            for j in range(lenth):
                if i!= j: # 不用反倒更快??
                    exchange_tmp = nowSolution.copy()
                    exchange_tmp[i] = nowSolution[j]
                    exchange_tmp[j] = nowSolution[i]
                    exchange_Tab.append(exchange_tmp)
                    exchange_State.append([nowSolution[i],nowSolution[j]])
    
    elif not asymmetry:
        # 对称问题只需要生成一半
        for i in range(lenth):
            for j in range(round(lenth/2)-1):
                if i!= j: # 不用反倒更快??
                    exchange_tmp = nowSolution.copy()
                    exchange_tmp[i] = nowSolution[j]
                    exchange_tmp[j] = nowSolution[i]
                    exchange_Tab.append(exchange_tmp)
                    exchange_State.append([nowSolution[i],nowSolution[j]])
    
    # 随机打乱，并选择其中的一部分
    c = list(zip(exchange_Tab,exchange_State))  # 将a,b整体作为一个zip,每个元素一一对应后打乱
    random.shuffle(c)                           # 打乱c
    c = c[0:neighborNum]
    exchange_Tab[:],exchange_State[:] = zip(*c) # 将打乱的c解开

    # 检查长度是否匹配
    assert len(exchange_Tab)==len(exchange_State)
    
    # 包装字典，防止更新不同步
    result = {'tab':exchange_Tab, 'state':exchange_State}
    
    return result

min([6,1,3])

"""# 操作禁忌表

禁忌表设计为三层数组
【【【城市1，城市2】，【总距离】】，  【【城市1，城市2】，【总距离】】，  ......】
"""

# t.insert(0,[[7,8],100])
# t

# t = [[[1,2],32],[[3,2],51],[[6,8],12]]
# t.insert(0,[[7,8],100])
# t.sort(key = lambda x:x[:][1])
# t

# min([x[1] for x in t])

"""t = list(range(5))
t[0:5]
"""

def append_table(table, best_value_now, exchanged_couple, length):
    
    # 在开头插入
    table.insert(0, [exchanged_couple,best_value_now])
    
    # 保持禁忌表长度
    if len(table) > length:
        # 不能直接扔掉最后，应该是按规则踢出
        return table[0:length]
    else:
        return table

def renew_table(banned_Table, best_value_now,exchanged_couple, tabLength):
    """更新表
    将当前最优值放在最前面，防止被扔掉
    删除掉超出的部分
    """
    banned_Table.sort(key = lambda x:x[:][1])
    
def random_add(banned_Table, best_value_now,exchanged_couple, tabLength):
    banned_Table = append_table(banned_Table, best_value_now,exchanged_couple, tabLength)
    #banned_Table.sort(key = lambda x:x[:][1])
    
    # 保持禁忌表长度
    if len(banned_Table) > tabLength:
        # 不能直接扔掉最后，应该是按规则踢出
        return banned_Table[0:tabLength]
    else:
        return banned_Table

def check_state_in_banned_table(exchanged_list):
  """
    检查次状态是不是在禁止表
  """
  state = False
  for i in range(len(banned_Table)):
    if banned_Table[i][0][0] == exchanged_list[0] and banned_Table[i][0][1] == exchanged_list[1] :
      state = True
      print("true=-------------")
      break
    if banned_Table[i][0][0] == exchanged_list[1] and banned_Table[i][0][1] == exchanged_list[0] :
      state = True
      print("true=-------------")
      break
  
  return state

def is_same(lista,listb):
  # 检查两数组是否完全相同
  state = False
  if lista[0] == listb[0] and lista[1] == listb[1] :
    state = True
  if lista[0] == listb[1] and lista[1] == listb[0] :
    state = True
  return state

def check_banned_table(table):
  """
    检查禁忌表，防止重复
    [[19, 44], 2344], [[44, 19], 2344], [[19, 44], 2344]]
    也得防止删除多了
  """
  delindex = []
  for k in range(len(table)):
    exchanged_list = table[k][0]

    delstate = False # 要不要删除 重复计数器
    which = 0
    
    for i in range(len(table)):
      # 执行删除
      if is_same(exchanged_list,table[i][0]) and delstate:
        #del table[i][0]
        delindex.append(i)
        #print(exchanged_list,table[i][0],i,k)
      # if table[i][0][0] == exchanged_list[0] and table[i][0][1] == exchanged_list[1] and delstate :
      #   if table[which][0][0]
      #   delstate = True
      # if table[i][0][0] == exchanged_list[1] and table[i][0][1] == exchanged_list[0] and delstate:
      #   delstate = True
      # 检测首个
      if is_same(exchanged_list,table[i][0]):
        which = i
        delstate = True
      # if table[i][0][0] == exchanged_list[0] and table[i][0][1] == exchanged_list[1] :
      #   which = i
      #   delstate = True
      # if table[i][0][0] == exchanged_list[1] and table[i][0][1] == exchanged_list[0] :
      #   delstate = True
  delindex = list(set(delindex))
  delindex.sort()
  if delindex:
    cnt=0
    for i in delindex:
      #print(i,cnt)
      del table[i-cnt]
      cnt= cnt+1

  return table

"""# 整体算法综合

"""

thisSolution,initlength = generate_first_solution(interCnt=70)
initlength

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

def LR_schlar(nowIter,maxIter,maxLR,method='sqrt'):
  """学习率维护函数
  nowIter
    当前迭代轮数
  maxIter
    预计总迭代次数
  maxLR
    学习率
  method
    梯度下降策略，比如余弦退火、平方、线性等
  """
  LR = maxLR
  minLR = 3 # 最低返回学习率，截断

  if method == 'sqrt':
    LR = int( (1 - nowIter/maxIter*nowIter/maxIter)*maxLR )
    if LR<minLR:
      LR=minLR
  
  elif method == 'linear':
    LR = int( (1 - nowIter/maxIter)*maxLR )
    if LR<minLR:
      LR=minLR

  return LR

'''
执行一次搜索算法
''' 
@timmer
def run(thisSolution=thisSolution, initlength=initlength, tablueLenth=10, iterTimes =1000,
        neighborNumber=20000, shake=False, lr_decay=False, start_accept = 1,
        shake_round = 40):
  """
  thisSolution、initlength
    此次迭代的开始位置、解的value
  tablueLenth
    表长
  iterTimes
    迭代轮数
  neighborNumber
    邻居数
  shake
    加入抖动
  lr_decay
    学习率衰减
  start_accept
    开始接受判断的第一个解的位置
  shake_round
    抖间隔
  """
  # 优化过程的中间变量
  tabLength = tablueLenth
  maxIter = iterTimes
  neighborNum = neighborNumber
  banned_Table = []       #禁忌表
  interate_procedure = []    #最终每次接受解的值
  mid_procedure = []      #中间过程产生的解的值
  saveInit = []         #保存抖动产生的初始解
  round = shake_round      #每round次就产生一次抖动 
     

  for cnt in tqdm(range(maxIter), desc='Searching'):
      # 学习率下降
      tabLength = LR_schlar(cnt%round,round,tablueLenth)
      if shake and cnt%round==0 and cnt!= 0 :
        # 保存一下上次（抖动前）的最优结果
        saveInit.append([thisSolution, best_value_now])
        thisSolution,initlength = generate_first_solution(interCnt=60)
        
        banned_Table = [] # 清空禁忌表
        # 本次的加进去，1，2是随机的
        #append_table(banned_Table, initlength, [1,2], tabLength)

      if not banned_Table: # 判断禁忌表是不是空的
      # 初始化禁忌表
        append_table(banned_Table, initlength, [1,2], tabLength)
        #continue
      # 接受解？
      isAccept = False

      '''
      # 按照规则寻找所有邻域，生成二维数组
      # 应该是随机选取
      # axis0为一种方法 axis1为对应的交换
      # 需要交换被记录
      '''
      gen = generate_neighborhood(thisSolution) # 产生邻居们
      exchanged_list = gen['state']       # 哪两个交换
      after_exchange_list = gen['tab']      # 交换的结果
      
      # 获取对应所有领域的路径长度
      len_list = cal_length_in_tab(gen['tab'])

      '''c的结构
      [0]:交换的结果 交换后的所有list
      [1]:哪两个交换 exchanged_list
      [2]:路径长度  对应交换的路径长度
      '''
      c = list(zip(after_exchange_list,exchanged_list,len_list))  # 将a,b整体作为一个zip,每个元素一一对应
      c.sort(key=lambda x: x[:][2]) # 对第三个元素（既长度排序） 
  
      # 相当于 排第一的是最优值 
      k = 0
      
      # 读取当前最优解
      # best_index_now, best_value_now = get_best_index(len_list)
      best_index_now, best_value_now = k, c[k][2]
      mid_procedure.append(best_value_now)

      # 最优解对应的交换方式
      #exchanged_couple = exchanged_list[best_index_now]
      exchanged_couple = c[k][1]

      #print('best_value_now:', best_value_now, get_best_index(len_list))

      # 最优破禁
      if min([x[1] for x in banned_Table]) > best_value_now :
          isAccept = True
      # 本轮最好解都没达到以前的
      else:
        # 判断并且更新最优解
        # 破禁检查 
        # 按道理是0 但是1更好 start_accept
        for j in range(start_accept,len(exchanged_list)):
          isExist = check_state_in_banned_table(c[j][1])
          if not isExist:
            # 接受解为当前的k
            isAccept = True
            k=j
            break

          elif isExist:
            # 寻找次优解
            # total
            if random.random() < random_accept:
              isAccept = True
              k=j
              break

      #banned_Table.sort(key = lambda x:x[:][1])

      if isAccept:
        # thisSolution = gen['tab'][best_index_now]
        thisSolution = c[k][0]
        #print(k)
        #print('best_value_accept:', thisSolution)
        #print('table:',banned_Table)
        banned_Table = append_table(banned_Table, c[k][2], c[k][1], tabLength)
        # 去重复
        banned_Table = check_banned_table(banned_Table)
        interate_procedure.append(c[k][2])  # 记录迭代过程        

  print('best_value_final:', get_length_in_list(thisSolution))
  #get_length_in_list(thisSolution)
  print(banned_Table)
  print(thisSolution)

  saveInit.sort(key=lambda x: x[:][1])

  # 绘图 interate_procedure  mid_procedure
  x1=range(0,len(interate_procedure)) 
  x2=range(0,len(mid_procedure))
  plt.plot(x1,interate_procedure,label='accepted',linewidth=1,color='r',marker='o',markerfacecolor='blue',markersize=12) 
  plt.plot(x2,mid_procedure,label='best in iter') 
  plt.xlabel('iter times')
  plt.ylabel('value')
  plt.title('iter')
  plt.legend()
  plt.show() 
  
  return thisSolution, get_length_in_list(thisSolution), saveInit
      #banned_Table

[x[1] for x in banned_Table]
banned_Table

"""# 实验过程"""

thisSolution,initlength = generate_first_solution(interCnt=70)
get_length_in_list(thisSolution)

thisSolution,initlength = generate_first_solution(interCnt=65)
thisSolution,thisLength,saveInit = run(thisSolution, thisLength, 20, 40, 20000, True, True)

thisSolution,initlength = generate_first_solution(interCnt=70)
thisSolution,thisLength,saveInit = run(thisSolution, thisLength, 20, 400, 8000, True, True)

"""### 对比接受起始位置的实验
随着**接受位置从第i个值开始**的 的i增加 抖动变大， 但总体在最优值
``` python  
[2169, 2169, 2169, 2169, 2182, 2182, 2182, 2182, 2197, 2169]
```

某次试验采取了大规模的i，但是最终发现开始一段时间最优值的差距不大，也就是说这样接受次优解的行为反倒没有明显性能下降。这可能是由于问题的解空间随机性过强，不具有明显的邻域特性来执行类似于梯度下降的接近策略。

(0.40928745595510807, 2.355980352919042e-05)
判断为低度线性相关
"""

t=[]
for j in range(1):
  thisSolution,initlength = generate_first_solution(interCnt=65)
  value = []
  for i in range(0,100):
    _,a,_ = run(thisSolution, thisLength, 10, 30, 8000, True, True,i)
    value.append(a)
  t.append(value)
  x1=range(0,len(value)) 
  plt.plot(x1,value,label='accepted',linewidth=1,color='r',marker='o',markerfacecolor='blue',markersize=12) 
  plt.xlabel('iter times')
  plt.ylabel('value')
  plt.title('iter')
  plt.legend()
  plt.show() 
t



this_t =t[0]
series = list(range(len(this_t)))

import scipy.stats as stats
# -----------------------------
# 当p<0.05(或者0.01)的前提下，才可以参考r值
# |r|<0.3 不存在线性关系
# 0.3<|r|<0.5  低度线性关系
# 0.5<|r|<0.8  显著线性关系
# |r|>0.8  高度线性关系
# ------------------------------
stats.pearsonr(this_t,series)

thisSolution,thisLength,saveInit = run(thisSolution, thisLength, 20, 1000, 250)

"""thisSolution,thisLength = run(thisSolution, thisLength, 3, 100, 25000)

### 消融实验 学习率衰减的**作用**
"""

a=[]
b=[]
for i in range(50):
  thisSolution,initlength = generate_first_solution(interCnt=70)
  _,res,_ = run(thisSolution, thisLength, 20, 40, 8000, True, True)
  a.append(res)
  _,res,_ = run(thisSolution, thisLength, 20, 40, 8000, True, False)
  b.append(res)
a,b
