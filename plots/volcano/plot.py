import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.lines import Line2D


def plot(data, **kwargs):
    # 提取数据
    log2fc = np.array(data['log2FoldChange'])
    pvalue = np.array(data['padj'])
    gene_names = np.array(data['gene_name'])

    print(f"kwargs: {kwargs}")
    # 计算显著性阈值
    significant = (pvalue < 0.05) & (np.abs(log2fc) > 1)

    # 绘制火山图
    fig, ax = plt.subplots(figsize=(10, 8))
    # 设置fig的大小
    plt.subplots_adjust(right=0.8)

    # 创建自定义颜色映射
    if kwargs["color"] is not None:
        colors = kwargs["color"]
        # cmap_name = 'custom_colormap'
        # cmap = LinearSegmentedColormap.from_list(cmap_name, colors)
        # 添加颜色条
        # cax = fig.add_axes([0.82, 0.5, 0.02, 0.3])  # [left, bottom, width, height]
        # cbar = fig.colorbar(scatter, cax=cax, orientation='vertical')
        # cbar.set_label('log2(fold change)')
        # 动态设置颜色条的范围
        # max_log2fc = max(abs(log2fc))  # 获取 log2FoldChange 的最大绝对值
        # norm = Normalize(vmin=-max_log2fc, vmax=max_log2fc)  # 创建归一化对象，范围对称
        if len(colors) != 3:
            raise Exception("colors must be 3 colors for down, not, up regulation")

        point_colors = []
        for fc, pv in zip(log2fc, pvalue):
            if fc > 1 and pv < 0.05:  # 上调且显著
                point_colors.append(colors[2])  # 上调颜色
            elif fc < -1 and pv < 0.05:  # 下调且显著
                point_colors.append(colors[0])  # 下调颜色
            else:  # 不显著或无变化
                point_colors.append(colors[1])  # 不显著颜色

        # 画图
        scatter = ax.scatter(log2fc, -np.log10(pvalue), c=point_colors, alpha=0.7)

        # 添加图例
        legend_elements = [
            Line2D([0], [0], marker='o', linestyle="none", color=colors[0], markersize=5, label="Down"),
            Line2D([0], [0], marker='o', linestyle="none", color=colors[1], markersize=5, label="Not"),
            Line2D([0], [0], marker='o', linestyle="none", color=colors[2], markersize=5, label="Up")
        ]
        ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1.02, 1))
    else:
        # 默认颜色映射及图例
        scatter = ax.scatter(log2fc, -np.log10(pvalue), c=["blue", "white", "red"], alpha=0.7)

        # 添加图例
        legend_elements = [
            Line2D([0], [0], marker='o', linestyle="none", color="blue", markersize=5, label="Down"),
            Line2D([0], [0], marker='o', linestyle="none", color="white", markersize=5, label="Not"),
            Line2D([0], [0], marker='o', linestyle="none", color="red", markersize=5, label="Up")
        ]
        ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1.02, 1))

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

    # 筛选显著基因
    significant_indices = np.where(significant)[0]
    top20_indices = []
    # 计算综合得分
    score = -np.log10(pvalue) * np.abs(log2fc)
    if len(significant_indices) > 0:
        # 获取显著基因的综合得分和名称
        significant_scores = score[significant_indices]
        significant_gene_names = gene_names[significant_indices]
        significant_log2fc = log2fc[significant_indices]
        significant_pvalue = pvalue[significant_indices]

        # 按综合得分降序排序
        sorted_indices = np.argsort(significant_scores)[::-1]
        top20_indices = sorted_indices[:20]
        top20_gene_names = significant_gene_names[top20_indices]
        top20_log2fc = significant_log2fc[top20_indices]
        top20_pvalue = significant_pvalue[top20_indices]

        # 创建一个DataFrame来保存前20个显著基因的数据并导出为Excel文件
        top20_data = pd.DataFrame({
            'Gene Name': top20_gene_names,
            'log2FoldChange': top20_log2fc,
            'padj': top20_pvalue
        })
        top20_data.to_excel('top20_genes.xlsx', index=False)

    # 注释基因
    # 方法一：只根据Log2FC的排序进行注释
    # if gene_names is not None and kwargs["annotate"]:
    #     significant_indices = np.where(significant)[0]
    #     if len(significant_indices) > 0:
    #         significant_log2fc = log2fc[significant_indices]
    #         significant_gene_names = gene_names[significant_indices]
    #         sorted_indices = np.argsort(np.abs(significant_log2fc))[::-1]
    #         top20_indices = sorted_indices[:20]
    #         top20_gene_names = significant_gene_names[top20_indices]
    #         top20_original_indices = significant_indices[top20_indices]
    #
    #         for idx in top20_original_indices:
    #             ax.text(log2fc[idx], -np.log10(pvalue[idx]), gene_names[idx], ha='center', va='bottom', fontsize=8)

    # 方法二：根据综合得分scores = -log10(padj) * |log2Fc|进行注释
    if gene_names is not None and kwargs["annotate"]:
        # 标注前20个显著基因
        for idx in range(len(top20_indices)):
            gene_idx = significant_indices[top20_indices[idx]]
            ax.text(log2fc[gene_idx], -np.log10(pvalue[gene_idx]), gene_names[gene_idx], ha='center', va='bottom',
                    fontsize=8)

    plt.show()
    plt.savefig("volcano_log2_fold_change.png")

