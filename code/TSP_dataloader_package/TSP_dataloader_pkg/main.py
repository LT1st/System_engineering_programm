# -*- coding: utf-8 -*-
# ���ݼ���
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA
from dataloader.load_TSP_from_floder import get_all_TSP_and_ATSP_in_floder
# �㷨����
from collection.SA import SA
from dataloader.DP import DP
# ���ӻ�����
from visualization.from_matrix import from_matrix,root_from_list
# ��������
samples,samples_atsp = get_all_TSP_and_ATSP_in_floder()

samples_name_list = []
# �����ֵ䣬��������㷨���
SA_dict = {}
DP_dict = {}

# ������������
for sample in samples:
    data = TSP_DATA(sample)
    samples_name_list.append(data.NAME)

    model = SA(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    SA_dict[data.NAME] = path_len

    model = DP(num_city = data.DIMENSION , mat = data.matrix)
    path, path_len = model.run()
    DP_dict[data.NAME] = path_len

    # ·�����ӻ�
    root_from_list(path,data.matrix)