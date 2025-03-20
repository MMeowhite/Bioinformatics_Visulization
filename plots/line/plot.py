import numpy as np
import gseapy as gp
import pandas as pd
import matplotlib.pyplot as plt
from bioservices import KEGG, QuickGO
from gseapy.plot import barplot, dotplot


def plot(args, data, **kwargs):
    """
    主函数，用于进行基因富集分析并绘制结果。

    parameters:
    - args: 包含分析参数的命名空间，如基因列表、背景基因列表、输出目录等。
    - data: 输入数据，可以是基因表达矩阵或其他相关数据。
    - kwargs: 其他关键字参数，如基因集数据库、分析类型等。
    """
    # 提取参数
    gene_list = kwargs['gene_list']
    outdir = kwargs["output"]
    analysis_type = args.analysis_type

    # 根据分析类型选择相应的分析函数
    if analysis_type == 'gsea':
        # 基因集合富集分析 (GSEA)
        gsea_results = gp.gsea(
            data=data,
            gene_sets='KEGG_2021_Human',
            cls=args.cls_file,
            outdir=outdir,
            permutation_num=100,
            method='signal_to_noise'
        )
        # 绘制 GSEA 结果
        gsea_results.plot_top_terms()

    elif analysis_type == 'go':
        # GO 富集分析
        go_results = gp.enrichr(
            gene_list=gene_list,
            gene_sets='GO_Biological_Process_2023',
            background=background,
            outdir=outdir
        )
        # 绘制 GO 富集结果
        barplot(go_results.res2d, title='GO Biological Process Enrichment')
        plt.show()

    elif analysis_type == 'kegg':
        # KEGG 富集分析
        kegg_results = gp.enrichr(
            gene_list=gene_list,
            gene_sets='KEGG_2021_Human',
            background=background,
            outdir=outdir
        )
        # 绘制 KEGG 富集结果
        barplot(kegg_results.res2d, title='KEGG Pathway Enrichment')
        plt.show()

    else:
        print("未知的分析类型，请选择 'gsea', 'go' 或 'kegg'。")


if __name__ == "__main__":
    import argparse

    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='基因富集分析工具')
    parser.add_argument('--gene_list', type=str, required=True, help='输入基因列表文件')
    parser.add_argument('--background', type=str, required=True, help='背景基因列表文件')
    parser.add_argument('--cls_file', type=str, help='样本分类文件（仅用于 GSEA）')
    parser.add_argument('--outdir', type=str, default='enrichment_results', help='输出目录')
    parser.add_argument('--analysis_type', type=str, choices=['gsea', 'go', 'kegg'], required=True, help='分析类型')

    args = parser.parse_args()

    # 读取基因列表和背景基因列表
    with open(args.gene_list, 'r') as f:
        gene_list = [line.strip() for line in f]

    with open(args.background, 'r') as f:
        background = [line.strip() for line in f]

    # 将基因列表和背景基因列表传递给 plot 函数
    plot(args, data=gene_list, background=background)