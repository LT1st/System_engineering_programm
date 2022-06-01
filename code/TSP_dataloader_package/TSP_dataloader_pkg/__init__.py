# -*- coding: utf-8 -*-
# import 所有子模块 直接使用算法
# 却并不需要知道它们是怎么实现的，也不想去了解arithmetic中是如何组织各个子模块的
# 数据加载
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA,TSP_load
from dataloader.load_TSP_from_floder import get_all_TSP_and_ATSP_in_floder
# 算法加载
from collection_from_web.SOM import SOM
from collection_from_web.SA import SA
from collection_from_web.DP import DP

# 可用模块名直接导入以上算法