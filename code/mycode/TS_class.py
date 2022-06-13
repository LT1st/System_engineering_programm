# -*- coding: utf-8 -*-
from numpy import*
import linecache
import itertools
from os import listdir, path
import sys
import math
import random
import matplotlib.pyplot as plt 
from tqdm import tqdm, trange

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



""" 整体算法综合

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