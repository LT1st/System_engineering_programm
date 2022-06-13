# -*- coding: utf-8 -*-
# 数据加载
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA
from dataloader.load_TSP_from_floder import get_all_TSP_and_ATSP_in_floder
# 算法加载
from collection.SA import SA
from dataloader.DP import DP
# 可视化加载
from visualization.from_matrix import from_matrix,root_from_list
# 加载数据
samples,samples_atsp = get_all_TSP_and_ATSP_in_floder()

samples_name_list = []
# 构建字典，储存各个算法结果
SA_dict = {}
DP_dict = {}

# 遍历测试样例
for sample in samples:
    data = TSP_DATA(sample)
    samples_name_list.append(data.NAME)

    model = SA(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    SA_dict[data.NAME] = path_len

    model = DP(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    DP_dict[data.NAME] = path_len

    # 路径可视化
    root_from_list(path,data.matrix)