# -*- coding: utf-8 -*-

"""
用于可视化邻接矩阵
https://networkx.org/documentation/stable/reference/convert.html

"""
import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.approximation as nx_app
import math
import numpy as np

def from_matrix(distance_matrix):
    """从矩阵生成图像对象
    distance_matrix
        list或者np形式的临界矩阵
    return
        #图像对象
    """
    distance_matrix = np.array(distance_matrix)

    def get_noself_list(aGraph):
        tmp = {}
        for u, v, d in G.edges(data=True):
            if u!=v:
                tmp[(u, v)]=d['weight']
        return tmp
    # 新建空对象
    G = nx.Graph()
    assert distance_matrix.shape[0]==distance_matrix.shape[1]
    vertex_list = list(range(distance_matrix.shape[0]))

    G_list = [(vertex_list[i], vertex_list[j], distance_matrix[i, j]) for i in range(distance_matrix.shape[0]) for j in range(distance_matrix.shape[1])]
    # 从任何可迭代容器中添加节点，例如列表
    G.add_weighted_edges_from(G_list)
    # 去除自环
    G.remove_edges_from(nx.selfloop_edges(G))
    # 也能去除，麻烦
    # edge_labels = dict([((u, v), d['weight']) for u, v, d in G.edges(data=True)])
    edge_labels = get_noself_list(G)
    pos = nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    nx.draw_networkx(G, pos, node_size=400)
    plt.show()

    return 

if __name__ == "__main__":
    distance_matrix = np.array([
        [0, 56, 35, 2, 51, 60],
        [56, 0, 21, 57, 78, 70],
        [35, 21, 0, 36, 68, 68],
        [2, 57, 36, 0, 51, 61],
        [51, 78, 68, 51, 0, 13],
        [60, 70, 68, 61, 13, 0]
    ])

    from_matrix(distance_matrix)