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

    return G

def root_from_list(root_list, distance_matrix, auto=False):
    """
    root_list:
        最优路径，保存为list，记得得走成闭环
    distance_matrix:
        距离矩阵
    auto:
        自动规划路径
    """
    distance_matrix = np.array(distance_matrix)

    G = from_matrix(distance_matrix)
    pos = nx.get_node_attributes(G, "pos")

    # Depot should be at (0,0)
    pos[0] = (0.5, 0.5)

    H = G.copy()


    #   计算路径
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
            dist = dist
            G.add_edge(i, j, weight=dist)
    # 自动规划路径
    if auto:
        cycle = nx_app.christofides(G, weight="weight")
        edge_list = list(nx.utils.pairwise(cycle))
    else:
        edge_list = root_list

    # 画全连接网
    nx.draw_networkx_edges(H, pos, edge_color="blue", width=0.5)

    # 画路径
    nx.draw_networkx(
        G,
        pos,
        with_labels=True,
        edgelist=edge_list,
        edge_color="red",
        node_size=200,
        width=3,
    )

    #print("The route of the traveller is:", cycle)
    plt.show()   

if __name__ == "__main__":
    distance_matrix = np.array([
        [0, 56, 35, 2, 51, 60],
        [56, 0, 21, 57, 78, 70],
        [35, 21, 0, 36, 68, 68],
        [2, 57, 36, 0, 51, 61],
        [51, 78, 68, 51, 0, 13],
        [60, 70, 68, 61, 13, 0]
    ])
    root = [0,1,3,2,5,4,0]

    from_matrix(distance_matrix)
    root_from_list(root,distance_matrix)