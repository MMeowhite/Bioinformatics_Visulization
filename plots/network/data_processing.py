import pandas as pd


def _adjacency_matrix_to_data(args, data):
    """
    创建邻接矩阵。

    参数:
        data (pd.DataFrame): 包含边信息的数据框。
            - 'source': 边的起点节点。
            - 'target': 边的终点节点。
            - 'weight' (可选): 边的权重。
            - 'community' (可选): 节点的社区编号。

    返回:
        dict: 包含节点和边信息的字典。
    """
    # 检查数据框是否包含必要的列
    required_columns = ['source', 'target']
    if not all(col in data.columns for col in required_columns):
        raise ValueError('The columns must contain both "source" and "target"')

    # 提取节点和边
    source = data['source'].tolist()
    target = data['target'].tolist()

    if len(source) != len(target):
        raise ValueError('The length of source and target must be equal')

    # 提取所有节点
    nodes = list(set(source + target))

    # 提取边
    edges = []
    if 'weight' in data.columns:
        weights = data['weight'].tolist()
        for s, t, w in zip(source, target, weights):
            edges.append((s, t, w))
    else:
        for s, t in zip(source, target):
            edges.append((s, t))

    # 提取社区信息
    community = None
    if 'community' in data.columns:
        community = data['community'].tolist()
        # 确保每个节点都有社区信息
        community_dict = {}
        for node, comm in zip(source + target, community * ((len(source) + len(target)) // len(community) + 1)):
            community_dict[node] = comm
        community = [community_dict.get(node, None) for node in nodes]

    # 组织数据
    result = {
        'nodes': nodes,
        'edges': edges,
        'community': community
    }

    return result


def data_processing(args, data):
    return args, _adjacency_matrix_to_data(args, data=data)


# 示例用法
if __name__ == "__main__":
    # 示例数据框
    data = pd.DataFrame({
        'source': ['A', 'A', 'B', 'C', 'D'],
        'target': ['B', 'C', 'C', 'D', 'E'],
        'weight': [2, 1, 3, 2, 1],
        'community': [0, 0, 0, 1, 1]
    })

    # 处理数据
    processed_data = data_processing(None, data)
