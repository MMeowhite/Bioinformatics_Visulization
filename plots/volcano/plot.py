import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize


def plot(args, data, **kwargs):
    # 提取数据
    log2fc = np.array(data['log2FoldChange'])
    pvalue = np.array(data['padj'])
    gene_names = np.array(data['gene_id'])

    # 计算显著性阈值
    significant = (pvalue < 0.05) & (np.abs(log2fc) > 1)

    # 创建自定义颜色映射
    if args.color:
        colors = args.color
        cmap_name = 'custom_colormap'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors)
    else:
        cmap = 'viridis'

    # 绘制火山图
    fig, ax = plt.subplots(figsize=(10, 8))

    # 动态设置颜色条的范围
    max_log2fc = max(abs(log2fc))  # 获取 log2FoldChange 的最大绝对值
    norm = Normalize(vmin=-max_log2fc, vmax=max_log2fc)  # 创建归一化对象，范围对称
    scatter = ax.scatter(log2fc, -np.log10(pvalue), c=log2fc, cmap=cmap, norm=norm, alpha=0.7)

    # 设置fig的大小
    plt.subplots_adjust(right=0.8)

    # 添加颜色条
    cax = fig.add_axes([0.82, 0.5, 0.02, 0.3])  # [left, bottom, width, height]
    cbar = fig.colorbar(scatter, cax=cax, orientation='vertical')
    cbar.set_label('log2(fold change)')

    # 动态设置x轴和y轴的范围
    max_x = max(abs(log2fc)) * 1.1  # x轴范围扩大10%
    min_x = -max_x
    max_y = max(-np.log10(pvalue)) * 1.1  # y轴范围扩大10%
    min_y = -5  # y轴最小值为0，因为-log10(p-value)是非负的
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # 添加阈值线
    ax.axvline(x=1, color='gray', linestyle='--', alpha=0.7)
    ax.axvline(x=-1, color='gray', linestyle='--', alpha=0.7)
    ax.axhline(y=-np.log10(0.05), color='gray', linestyle='--', alpha=0.7)

    # 设置标题和轴标签
    ax.set_title('Volcano Plot')
    ax.set_xlabel('log2(fold change)')
    ax.set_ylabel('-log10(p-value)')

    # 注释基因
    if gene_names is not None and args.annotate:
        significant_indices = np.where(significant)[0]
        if len(significant_indices) > 0:
            significant_log2fc = log2fc[significant_indices]
            significant_gene_names = gene_names[significant_indices]
            sorted_indices = np.argsort(np.abs(significant_log2fc))[::-1]
            top20_indices = sorted_indices[:20]
            top20_gene_names = significant_gene_names[top20_indices]
            top20_original_indices = significant_indices[top20_indices]

            for idx in top20_original_indices:
                ax.text(log2fc[idx], -np.log10(pvalue[idx]), gene_names[idx], ha='center', va='bottom', fontsize=8)

    plt.show()