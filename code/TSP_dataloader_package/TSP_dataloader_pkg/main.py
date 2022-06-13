# -*- coding: utf-8 -*-
# ���ݼ���
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA
from dataloader.load_TSP_from_floder import get_all_TSP_and_ATSP_in_floder
# �㷨����
from dataloader.SOM import SOM
from collection.SA import SA
from collection.DP import DP

# ��������
samples = get_all_TSP_and_ATSP_in_floder()

samples_name_list = []
SOM_dict = {}
SA_dict = {}
DP_dict = {}

# ������������
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

