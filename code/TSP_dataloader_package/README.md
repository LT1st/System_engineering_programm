This is an implementation of TSP dataloader. 

# Features
- All test samples available.
- Download sample automatically.
- Get best solution on web.
- Convert to adjacence matrix, adjacence table, coordinate table.
- Easily visualizing for all kinks of data.
- DEMO for SOM, GA, TS, etc.

# Attention
- Larage DIMENSION will cause memory leak.

# How to use

## 1. Get a TSP_DATA class
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
## 2. What TSP_DATA class offers
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

## 3. Tst some alogrithm
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
## 4. Try some ADVANCED method
check if the matrix is summetry.
```python
check_if_summetry(matrix_to_be_checked)
```
Get best result from web. Return a dict indexed by NAME.
```python
dict_best_result = get_best_result_from_web()
```

# TODO
- [ ] Add timmer across files. Using another func?
- [ ] 画图
- [ ] 注意线上版本和给老师的不一样

