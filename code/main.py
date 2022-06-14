# -*- coding: utf-8 -*-
# 数据加载
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA
from dataloader.load_TSP_from_floder import get_all_TSP_and_ATSP_in_floder
# 算法加载
from collection.SA import SA
from collection.PSO import PSO
from collection.TS import TS
from dataloader.DP import DP
# 可视化加载
from visualization.from_matrix import from_matrix,root_from_list
# 加载数据
samples,samples_atsp = get_all_TSP_and_ATSP_in_floder()
# 从网页爬取最佳数据
from dataloader.get_best_solution import get_best_result_from_web

samples_name_list = []
# 构建字典，储存各个算法结果
SA_dict = {}
DP_dict = {}
PSO_dict = {}
TS_dict = {}


#data = TSP_DATA('D:\\0latex\\System_engineering_programm\\TSP_tst_data\\lin318.tsp.gz',debug=True)

# 遍历测试样例
for sample in samples:
    data = TSP_DATA(sample)
    print(data.NAME,"successful",data.EDGE_WEIGHT_TYPE)
    samples_name_list.append(data.NAME)

    model = SA(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    SA_dict[data.NAME] = path_len
    # 路径可视化
    #root_from_list(path,data.matrix)
    
    model = DP(num_city=data.DIMENSION, num_total=25, iteration=500, data=data.matrix)
    path, path_len = model.run()
    DP_dict[data.NAME] = path_len
    # 路径可视化
    #root_from_list(path,data.matrix)
    
    model = PSO(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    PSO_dict[data.NAME] = path_len
    # 路径可视化
    #root_from_list(path,data.matrix)
    
    model = TS(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    TS_dict[data.NAME] = path_len
    # 路径可视化
    #root_from_list(path,data.matrix)

    
get_best_result_from_web()