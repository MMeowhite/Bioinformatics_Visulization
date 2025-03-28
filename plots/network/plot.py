import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
from scipy.spatial import distance_matrix
from mpl_toolkits.mplot3d import Axes3D


class NetworkPlot:
    def __init__(self, args, data):
        print(data)
        self.args = args
        self.data = data
        self.fig = None
        self.ax = None

        # 从 args 中获取参数，如果没有则使用默认值
        self.title = args.title if hasattr(args, 'title') else 'Network Plot'
        self.node_size = args.node_size if hasattr(args, 'node_size') else 300
        self.node_color = args.node_color if hasattr(args, 'node_color') else 'blue'
        self.node_alpha = args.node_alpha if hasattr(args, 'node_alpha') else 0.8
        self.edge_color = args.edge_color if hasattr(args, 'edge_color') else 'gray'
        self.edge_alpha = args.edge_alpha if hasattr(args, 'edge_alpha') else 0.5
        self.with_labels = args.with_labels if hasattr(args, 'with_labels') else True
        self.layout = args.layout if hasattr(args, 'layout') else 'spring'
        self.weighted = args.weighted if hasattr(args, 'weighted') else False
        self.d3 = args.d3 if hasattr(args, 'd3') else False

    def plot_simple(self):
        print("Plotting network...")
        # 创建图
        G = nx.Graph()
        # 添加节点
        for node in self.data['nodes']:
            G.add_node(node)
        # 添加边
        for edge in self.data['edges']:
            G.add_edge(edge[0], edge[1])

        # 绘制网络图
        self._draw_network(G)

    def plot_weighted(self):
        # 创建图
        G = nx.Graph()
        # 添加节点
        for node in self.data['nodes']:
            G.add_node(node)
        # 添加带权重的边
        for edge in self.data['edges']:
            G.add_edge(edge[0], edge[1], weight=edge[2])

        # 绘制网络图
        self._draw_network(G, weighted=True)

    def plot_community(self):
        # 创建图
        G = nx.Graph()
        # 添加节点
        for node in self.data['node']:
            G.add_node(node)
        # 添加边
        for edge in self.data['edges']:
            G.add_edge(edge[0], edge[1])

        # 设置社区信息
        community = self.community
        # 为每个社区分配不同颜色
        colors = plt.cm.tab10(np.linspace(0, 1, len(set(community.values()))))
        color_map = {node: colors[community[node]] for node in G.nodes()}

        # 绘制网络图
        self._draw_network(G, node_color=color_map)

    def plot_3d(self):
        # 创建3D图
        G = nx.Graph()
        # 添加节点
        for node in self.data['nodes']:
            G.add_node(node)
        # 添加边
        for edge in self.data['edges']:
            G.add_edge(edge[0], edge[1])

        # 绘制3D网络图
        self._draw_3d_network(G)

    def _draw_network(self, G, weighted=False, node_color=None):
        # 创建图形
        self.fig, self.ax = plt.subplots(figsize=(10, 8))

        # 选择布局
        if self.layout == 'spring':
            pos = nx.spring_layout(G)
        elif self.layout == 'circular':
            pos = nx.circular_layout(G)
        elif self.layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G)

        # 绘制节点
        if node_color:
            nx.draw_networkx_nodes(G, pos, node_size=self.node_size, node_color=list(node_color.values()), alpha=self.node_alpha)
        else:
            nx.draw_networkx_nodes(G, pos, node_size=self.node_size, node_color=self.node_color, alpha=self.node_alpha)

        # 绘制边
        if weighted:
            weights = [G[u][v]['weight'] for u, v in G.edges()]
            nx.draw_networkx_edges(G, pos, width=weights, edge_color=self.edge_color, alpha=self.edge_alpha)
        else:
            nx.draw_networkx_edges(G, pos, edge_color=self.edge_color, alpha=self.edge_alpha)

        # 绘制标签
        if self.with_labels:
            nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

        # 设置标题
        self.ax.set_title(self.title)
        # 去掉坐标轴
        self.ax.axis('off')

    def _draw_3d_network(self, G):
        # 创建3D图形
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

        # 生成3D布局
        pos = nx.spring_layout(G, dim=3)

        # 提取节点和边的坐标
        node_xyz = np.array([pos[v] for v in sorted(G)])
        edge_xyz = np.array([(pos[u], pos[v]) for u, v in G.edges()])

        # 绘制节点
        self.ax.scatter(*node_xyz.T, s=self.node_size, ec='w', alpha=self.node_alpha, color=self.node_color)

        # 绘制边
        for vizedge in edge_xyz:
            self.ax.plot(*vizedge.T, color=self.edge_color, alpha=self.edge_alpha)

        # 设置标题
        self.ax.set_title(self.title)
        # 去掉坐标轴
        self.ax.axis('off')


def plot(args, data, plot_type='simple'):
    """
    绘制网络图函数，支持多种类型。

    :parameter
        :param args : 命令行参数对象
        :param data : 数据，包含节点和边信息
        :param plot_type : 网络图类型，可选值为 'simple', 'weighted', 'community', '3d'
    """
    print(f"data: {data}")

    network_plot = NetworkPlot(args, data)

    if plot_type == 'simple':
        network_plot.plot_simple()
    elif plot_type == 'weighted':
        network_plot.plot_weighted()
    elif plot_type == 'community':
        network_plot.plot_community()
    elif plot_type == '3d':
        network_plot.plot_3d()
    else:
        raise ValueError("Unsupported network plot type")

    # 保存图像
    plt.savefig('network.png', dpi=300, bbox_inches='tight')


