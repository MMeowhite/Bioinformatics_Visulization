import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def plot(data, **kwargs):
    # 解析数据
    heat_data = data.get("heat_data")  # 热图数据
    rownames = data.get("rownames")  # 行名（基因名）
    colnames = data.get("colnames")  # 列名（样本名）

    print(f"{heat_data.shape, heat_data.dtype}")

    # 如果用户提供了自定义颜色，创建自定义颜色映射
    if kwargs.get("color") is not None:
        colors = kwargs["color"]
        cmap_name = 'custom_colormap'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors)
    else:
        cmap = 'viridis'  # 默认颜色映射集 viridis

    # 根据数据形状动态调整图形大小
    rows, cols = heat_data.shape
    cell_width = 0.4  # 每个格子的宽度（英寸）
    cell_height = 0.2  # 每个格子的高度（英寸）
    fig_width = cols * cell_width
    fig_height = rows * cell_height
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # 创建热图
    heatmap = ax.imshow(heat_data, cmap=cmap, interpolation='nearest')

    # 添加颜色条
    cax = fig.add_axes([0.8, 0.6, 0.02, 0.2])  # [left, bottom, width, height]
    cbar = fig.colorbar(heatmap, cax=cax, orientation='vertical')  # 传入 heatmap 对象
    cbar.set_label('Gene Expression')

    # 设置坐标轴标签
    ax.set_xticks(np.arange(len(colnames)))
    ax.set_xticklabels(colnames, rotation=45, ha='right')
    ax.set_yticks(np.arange(len(rownames)))
    ax.set_yticklabels(rownames)

    # 检查数据维度是否匹配
    if heat_data.shape[1] != len(colnames):
        raise ValueError(
            f"Column names length ({len(colnames)}) does not match heat_data columns ({heat_data.shape[1]})")

    # 添加数据标注
    if kwargs.get("annotate", False):
        for i in range(len(rownames)):
            for j in range(len(colnames)):
                # 确保数据值在白色和黑色之间有良好的对比度
                cell_value = heat_data[i, j]
                text_color = 'white' if cell_value < 0.5 else 'black'
                ax.text(j, i, f'{cell_value:.2f}', ha='center', va='center', color=text_color)

    # 添加标题
    ax.set_title("Heatmap")

    # 保存图片
    plt.savefig("output/heatmap.png")

    # 显示热图
    plt.show()
