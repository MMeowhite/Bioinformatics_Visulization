import numpy as np
import gseapy as gp
import pandas as pd


def plot(args, data, **kwargs):
    # 示例数据：基因表达矩阵和表型标签
    # 假设你已经有了基因表达矩阵 `expr_data` 和表型标签 `phenotype`

    # 基因表达矩阵示例（随机生成）
    np.random.seed(0)
    genes = [f"Gene_{i}" for i in range(1000)]  # 假设有1000个基因
    samples = ["Ctrl_1", "Ctrl_2", "Exp_1", "Exp_2"]  # 两个对照组和两个实验组
    expr_data = pd.DataFrame(np.random.randn(1000, 4), index=genes, columns=samples)

    # 表型标签
    phenotype = {"Ctrl_1": "Ctrl", "Ctrl_2": "Ctrl", "Exp_1": "Exp", "Exp_2": "Exp"}

    # 基因集文件（.gmt格式）
    # 你可以从 MSigDB 下载基因集文件，或者自己创建一个
    gene_sets = "path/to/your/gene_sets.gmt"

    # 运行 GSEA 分析
    pre_res = gp.prerank(rnk=expr_data, gene_sets=gene_sets, phenotypes=phenotype, min_size=10, max_size=500)

    # 绘制富集图
    pre_res.plot_top_terms(top=10, ofname="GSEA_top10_terms.png")  # 保存为图片


if __name__ == "__main__":
    plot()