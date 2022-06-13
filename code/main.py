# -*- coding: utf-8 -*-
# 数据加载
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA
from dataloader.load_TSP_from_floder import get_all_TSP_and_ATSP_in_floder
# 算法加载
from collection_from_web.SOM import SOM
from collection_from_web.SA import SA
from collection_from_web.DP import DP

# 加载数据
# 一次性返回目标位置的tsp和atsp两种
samples,atsp_samples = get_all_TSP_and_ATSP_in_floder(r'D:\0latex\System_engineering_programm\TSP_tst_data')

samples_name_list = []
SOM_dict = {}
SA_dict = {}
DP_dict = {}

# 遍历测试样例
for sample in samples:
    data = TSP_DATA(sample)
    samples_name_list.append(data.NAME)

#    model = SOM(num_city=data.DIMENSION, data=data.matrix)
#    path, path_len = model.run()
#    SOM_dict[data.NAME] = path_len

    model = SA(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    SA_dict[data.NAME] = path_len

    model = DP(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    DP_dict[data.NAME] = path_len

