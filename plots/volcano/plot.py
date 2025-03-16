import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize


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
    if kwargs.get("color") is not None:
        colors = kwargs["color"]
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

        # 计算点的大小，与 -log10(pvalue) 成正比
        point_sizes = -np.log10(pvalue) # 调整系数以控制点的大小范围

        # 画图
        scatter = ax.scatter(log2fc, -np.log10(pvalue), c=point_colors, s=point_sizes, alpha=0.7)

        # 添加图例
        legend_elements = [
            Line2D([0], [0], marker='o', linestyle="none", color=colors[0], markersize=5, label="Down"),
            Line2D([0], [0], marker='o', linestyle="none", color=colors[1], markersize=5, label="Not"),
            Line2D([0], [0], marker='o', linestyle="none", color=colors[2], markersize=5, label="Up")
        ]
        point_color_legend = ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1.02, 1))
    else:
        # 默认颜色映射及图例
        point_colors = []
        for fc, pv in zip(log2fc, pvalue):
            if fc > 1 and pv < 0.05:  # 上调且显著
                point_colors.append("red")  # 上调颜色
            elif fc < -1 and pv < 0.05:  # 下调且显著
                point_colors.append("blue")  # 下调颜色
            else:  # 不显著或无变化
                point_colors.append("grey")  # 不显著颜色

        # 计算点的大小，与 -log10(pvalue) 成正比
        point_sizes = -np.log10(pvalue)  # 调整系数以控制点的大小范围

        # 画图
        scatter = ax.scatter(log2fc, -np.log10(pvalue), c=point_colors, s=point_sizes, alpha=0.7)

        # 添加图例
        legend_elements = [
            Line2D([0], [0], marker='o', linestyle="none", color="blue", markersize=5, label="Down"),
            Line2D([0], [0], marker='o', linestyle="none", color="grey", markersize=5, label="Not"),
            Line2D([0], [0], marker='o', linestyle="none", color="red", markersize=5, label="Up")
        ]
        point_color_legend = ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1.02, 1))

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
    if gene_names is not None and kwargs.get("annotate", False):
        # 标注前20个显著基因
        for idx in range(len(top20_indices)):
            gene_idx = significant_indices[top20_indices[idx]]
            ax.text(log2fc[gene_idx], -np.log10(pvalue[gene_idx]), gene_names[gene_idx], ha='center', va='bottom',
                    fontsize=8)

        # 添加点大小的图例
        # 获取pvalue中的最小值和最大值
        min_p = min(pvalue)
        max_p = max(pvalue)

        # 计算对数值范围
        min_log_p = -np.log10(min_p)
        max_log_p = -np.log10(max_p)

        # 生成n个等间距的对数值
        n = 5
        log_p_values = np.linspace(min_log_p, max_log_p, n)

        # 转换回原始p值
        p_values = [10 ** (-log_p) for log_p in log_p_values]

        # 计算点的大小，基于-log10(p)并乘以10
        point_sizes = [log_p * 10 for log_p in log_p_values]

        # 限制点的大小在20到200之间
        point_sizes = np.clip(point_sizes, 20, 200)

        # 创建点的标签，显示-log10(p)的整数值
        point_labels = [int(round(log_p)) for log_p in log_p_values]

        # 创建图例元素
        legend_elements = []
        for p, size, label in zip(p_values, point_sizes, point_labels):
            legend_elements.append(
                Line2D([0], [0], marker='o', linestyle="none",
                       color='black', markersize=np.sqrt(size),
                       label=f"{label} (p={p:.1e})"
                       )
            )

        # 添加点大小图例到ax
        ax.legend(handles=legend_elements,
                  loc="upper left",
                  bbox_to_anchor=(1.02, 0.8),
                  title="-log10(p)")

    ax.add_artist(point_color_legend)

    # 保存热图
    plt.savefig("output/volcano.png")

    # 显示热图
    plt.show()