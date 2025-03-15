import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def plot(args, data, **kwargs):
    # 如果用户提供了自定义颜色，创建自定义颜色映射
    if args.color:
        colors = args.color
        cmap_name = 'custom_colormap'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors)
    else:
        cmap = 'viridis'  # 默认颜色映射集 viridis

    plt.imshow(data, cmap=cmap, interpolation='nearest')
    plt.colorbar()
    plt.xticks(data['gene_id'])
    plt.yticks(np.arange(5), ['1', '2', '3', '4', '5'])

    if args.annotate:
        for i in range(5):
            for j in range(5):
                plt.text(
                    j,
                    i,
                    '{:.2f}'.format(data[i, j]),
                    ha='center',
                    va='center',
                    color='white'
                )

    plt.show()
