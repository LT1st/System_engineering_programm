# == 本项目用于2022春季学期课程设计 ==

- 算法实现语言：*Python*
- 写作：LaTex
- 论文编译器：Overleaf
- 思维导图笔记：Xmind
- 文献管理：Zeotero
- 开源项目地址：[@Github](https://github.com/LT1st/System_engineering_programm/tree/master)
- 开源库地址：[@Pypi](https://test.pypi.org/project/TSP-dataloader/)

# 文件结构

- final_report	最终报告latex文档代码
- mid_term	    中期文档latex代码

- proposal        开题latex代码
- code            代码
- TSP_tst_data    TSP测试数据
- 读取失败的测试样例 由于维度太大导致加载不出来的失败情况
- 20220421-TSP    任务要求

# BUG

- [x]  i=j时候计算距离应该是 inf 需要定义一个很大值
- [ ]  加入直接可视化 networkx
- [ ]  ATSP转换TSP后，需要内部状态改变
# 代码说明
- 算法设计阶段使用了jupyter notenook，请开启服务后打开文件。同时也提供线上运行环境，论文中会给出colab连接。
- 工程化实现使用python类和包结构
- 🚀 所有代码存放在 code 文件夹下
## 🌟dataloader 
### Dataloader_for_TSP(ATSP)_datasets 好用的数据集的加载器
- 提供了用于TSP数据集的加载器*TSP_DATA*，能适用于大多数TSP测试样例。  
- 目前网络上代码仅能适用于固定长度的测试样例，非常原始。本项目中的TSP_DATA类能根据数据表头自动获取数据类型、计算方式等信息。  
- 可同时根据数据集变化，动态需求计算*邻接矩阵和邻接表*，保存在类内变量中
- 可自动访问网络，获取各测试样例当前最优值，比较算法精度
- 通过全局变量和修饰器获取数据加载、计算耗时
- 自动数据集下载脚本，运行既获取

## 🌟Visualization 提供了数据可视化

- 利用networkx库，解决了大多数TSP测试样例未提供坐标，无法可视化的问题
- 根据加载器类*TSP_DATA*返回可视化数据，数据接口无需调整

## 🌟collection 算法合集
- TSP求解算法。由于时间有限，又想测试尽可能多的算法，因此使用了部分网络开源代码

## 🌟my_algorithm 算法合集
- 存放我写的算法代码，无法直接用在工程中，用于验证
## 🌟[TSP_dataloader_package 开源的py-pi库](https://test.pypi.org/project/TSP-dataloader/)
存放我的开源pip库：[官方网站](https://test.pypi.org/project/TSP-dataloader/)

## 🌟测试函数时间跨文件测量

测量函数运行时间，用于后续训练

### 使用方法
```bash
::在控制台输入安装
pip install -i https://test.pypi.org/simple/ TSP-dataloader
```

### 维护方法
0. 改版本号，维护setup.py
1. 打包
```bash
::在控制台输入
python setup.py sdist bdist_wheel
```
2. 上传到测试环境
```bash
::在控制台输入 当前文件夹路径与setpy.py一致
python -m twine upload --repository testpypi dist/*

::使用测试环境
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME #其中 example-pkg-YOUR-USERNAME 即自己指定的包名
```
3. 发布正式包
```bashh
python -m twine upload --repository testpypi dist/* -u __token__  -p pypi-密码在qq收藏备份 --verbose
```
﻿This is an implementation of TSP dataloader. 

### Features
- All test samples available.
- Download sample automatically.
- Get best solution on web.
- Convert to adjacence matrix, adjacence table, coordinate table.
- Easily visualizing for all kinks of data.
- DEMO for SOM, GA, TS, etc.

### Attention
- Larage DIMENSION will cause memory leak.

### How to use

#### 1. Get a TSP_DATA class
Chose a method to get a $TSP_DATA class $ at first.    
Use $get_all_TSP_and_ATSP_in_floder()$ to get all atsp and tsp file path in a floder.   
```python
import TSP_dataloader as DL
# get all paths of all files in floder
tsp_files , atsp_files = get_all_TSP_and_ATSP_in_floder("Your dataset floder here")
# go throuht all samples
for tsp_file in tsp_files:
    data_class = DL.TSP_load("Your simgle TSP file path here")

```

Use $TSP_load()$ to get a single $TSP_DATA$ class.
```python
import TSP_dataloader as DL
data_class = DL.TSP_load("Your simgle TSP file path here")
```

Use  $TSP_DATA class $  directly.
```python
import TSP_dataloader as TSP_DATA
data_class = TSP_DATA("Your simgle TSP file path here")
```
#### 2. What TSP_DATA class offers
Get adjacency matrix.
```python
data_class.get_matrix()
```
Get adjacency table.
```python
data_class.get_table()
```
Get coorodinate list.
```python
data_class.get_coorodinate_list()
```
Basic elements.
```python
类内变量：
必有：
    self.NAME         测试样例名称
    self.TYPE         测试样例类型  TSP ATSP
    self.DIMENSION.      维度
    self.EDGE_WEIGHT_TYPE   边权值计算方式 决定读取方式 
    self.matrix        矩阵形式数据
    self.table .       邻接表形式数据

可能有：
    self.EDGE_WEIGHT_FORMAT
    self.EDGE_DATA_FORMAT
    self.NODE_COORD_TYPE required if EDGE_WEIGHT_TYPE is not WeightKind::Explicit
```

#### 3. Tst some alogrithm
```
from TSP_dataloader import SOM,DP,SA

samples = get_all_TSP_and_ATSP_in_floder()

samples_name_list = []
SOM_dict = {}
SA_dict = {}
DP_dict = {}

# go through
for sample in samples:
    data = TSP_DATA(sample)
    samples_name_list.append(data.NAME)

    model = SOM(num_city=data.DIMENSION, data=data.matrix)
    path, path_len = model.run()
    SOM_dict[data.NAME] = path_len

    model = SA(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    SA_dict[data.NAME] = path_len

    model = DP(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    DP_dict[data.NAME] = path_len
```
#### 4. Try some ADVANCED method
alternative input to make load quicker
```python
def TSP_load(path, requireTable=True, requireMatrix=True, load_now =True):
  """传入单个数据地址，读取并且加载数据的表头
  path:
    单个测试样例的数据地址
  requireTable:
    需要邻接表？
  requireMatrix：
    需要邻接矩阵？  
  """
```
check if the matrix is summetry.
```python
data_class.check_if_summetry(matrix_to_be_checked)
```
Get best result from web. Return a dict indexed by NAME.
```python
data_class.dict_best_result = get_best_result_from_web()
```
Convert ATSP to TSP.
```python
data_class.ATSP2TSP_np()
```
check if any inner-class variable wrong 
```python
data_class.check_if_reasonable()
```
### TODO
- [ ] Add timmer across files. Using another func?
- [x] 画图
- [x] 注意线上版本和给老师的不一样
- [ ] if '3D' in self.评估 使用三维数据加载器，坐标表间隔设成4


# 其他文件夹
- 记录课程的开题、中期、答辩。使用$Latex$编写。
- 存放数据集
- 记录加载报错的测试样例（主要是由于维度过高，内存溢出）
