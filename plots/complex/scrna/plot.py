import scanpy as sc
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.decorator import log


def preprocessing(data, output_path, n_top, min_genes, min_cells):
    """
    This preprocessing process is copied from the scanpy official website.

    :param data: AnnData object containing the raw data.
    :param output_path: Path to save the output files.
    :param n_top: Number of top genes to plot.
    :param min_genes: Minimum number of genes expressed in a cell.
    :param min_cells: Minimum number of cells expressing a gene.
    :return: Processed AnnData object.
    """
    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)

    # 绘制最高表达基因图
    sc.pl.highest_expr_genes(data, n_top=n_top, show=False)
    plt.savefig(f"{output_path}/1_highest_expr_genes.png", bbox_inches='tight', dpi=300)
    plt.close()

    # filter cells and genes
    sc.pp.filter_cells(data, min_genes=min_genes)
    sc.pp.filter_genes(data, min_cells=min_cells)

    # qc metrics
    data.var["mt"] = data.var_names.str.startswith("MT-")
    sc.pp.calculate_qc_metrics(
        data, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True
    )

    # A violin plot of some of the computed quality measures:
    #   the number of genes expressed in the count matrix
    #   the total counts per cell
    #   the percentage of counts in mitochondrial genes
    sc.pl.violin(
        data,
        ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
        jitter=0.4,
        multi_panel=True,
        show=False
    )
    plt.savefig(f"{output_path}/2_violin.png", bbox_inches='tight', dpi=300)
    plt.close()

    sc.pl.scatter(data, x="total_counts", y="pct_counts_mt", show=False)
    plt.savefig(f"{output_path}/3_pct_counts_mt_vs_total_counts.png", bbox_inches='tight', dpi=300)
    plt.close()
    sc.pl.scatter(data, x="total_counts", y="n_genes_by_counts", show=False)
    plt.savefig(f"{output_path}/4_n_genes_by_counts_vs_total_counts.png", bbox_inches='tight', dpi=300)
    plt.close()

    # filter again by slicing
    data = data[data.obs.n_genes_by_counts < 2500, :]
    data = data[data.obs.pct_counts_mt < 5, :].copy()

    # Total-count normalize (library-size correct) the data matrix
    #  to 10,000 reads per cell, so that counts become comparable among cells.
    sc.pp.normalize_total(data, target_sum=1e4)
    # logarithmize the data:
    sc.pp.log1p(data)

    # identify highly-variable genes
    sc.pp.highly_variable_genes(data, min_mean=0.0125, max_mean=3, min_disp=0.5)
    sc.pl.highly_variable_genes(data, show=False)
    plt.savefig(f"{output_path}/5_highly_variable_genes.png")
    plt.close()

    data.raw = data.copy()

    # If you don’t proceed below with correcting the data with sc.pp.regress_out and scaling it via sc.pp.scale,
    # you can also get away without using .raw at all.
    data = data[:, data.var.highly_variable]
    sc.pp.regress_out(data, ["total_counts", "pct_counts_mt"])
    # Scale each gene to unit variance. Clip values exceeding standard deviation 10.
    sc.pp.scale(data, max_value=10)

    return data


@log
def plot(args, data):
    # 确保输出目录存在
    if args.output is None:
        output_path = "output/scrna"
    else:
        output_path = args.output

    os.makedirs(output_path, exist_ok=True)

    # extract parameters from args
    n_top = args.n_top if hasattr(args, 'n_top') else 20
    min_genes = args.min_genes if hasattr(args, 'min_genes') else 200
    min_cells = args.min_cells if hasattr(args, 'min_cells') else 3
    data = preprocessing(data, output_path, n_top, min_genes, min_cells)

    # PCA analysis
    print(f"after preprocess: {data}")
    sc.tl.pca(data, svd_solver="arpack")
    sc.pl.pca(data, color="S100a6", show=False)
    plt.savefig(f"{output_path}/6_pca.png", bbox_inches='tight', dpi=300)
    plt.close()

    sc.pl.pca_variance_ratio(data, log=True, show=False)
    plt.savefig(f"{output_path}/7_pca_variance_ratio.png", bbox_inches='tight', dpi=300)
    plt.close()

    # save results
    data.write(f"{output_path}/processed_data.h5ad")

    # compute the neighborhood graph of cells using the PCA representation of the data matrix.
    sc.pp.neighbors(data, n_neighbors=10, n_pcs=40)

    # embedding the neighborhood graph
    sc.tl.leiden(
        data,
        resolution=0.9,
        random_state=0,
        flavor="igraph",
        n_iterations=2,
        directed=False,
    )
    sc.tl.umap(data)

    # clustering the neighborhood graph
    sc.pl.umap(data, color=["S100a6", "leiden"], show=False)
    # You can also plot the scaled and corrected gene expression by explicitly stating that you don’t want to use .raw.
    # sc.pl.umap(data, color=["CST3", "NKG7", "PPBP", "leiden"], show=False, use_raw=False)
    plt.savefig(f"{output_path}/8_umap.png", bbox_inches='tight', dpi=300)
    plt.close()

    # save results
    data.write(f"{output_path}/processed_data.h5ad")

    # find marker genes
    sc.tl.rank_genes_groups(data, "leiden", method="wilcoxon") # methods can be chosen as 'logreg', 'wilcoxon', 't-test', 't-test_overestim_var'
    sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, show=False)
    plt.savefig(f"{output_path}/9_marker_genes.png", bbox_inches='tight', dpi=300)
    plt.close()
    rank_genes_groups = pd.DataFrame(data.uns["rank_genes_groups"]["names"]).head(5)
    result = data.uns["rank_genes_groups"]
    groups = result["names"].dtype.names
    NP = pd.DataFrame(
        {
            f"{group}_{key[:1]}": result[key][group]
            for group in groups
            for key in ["names", "pvals"]
        }
    ).head(5)

    # sc.tl.rank_genes_groups(data, "leiden", groups=["0"], reference="1", method="wilcoxon")
    # sc.pl.rank_genes_groups(data, groups=["0"], n_genes=20, show=False)
    # sc.pl.rank_genes_groups_violin(data, groups="0", n_genes=8, show=False)
    # plt.close()

    # If you want to compare a certain gene across groups, use the following.
    # sc.pl.violin(data, ["CST3", "NKG7", "PPBP"], groupby="leiden")

    new_cluster_names = [
        "CD4 T",
        "B",
        "FCGR3A+ Monocytes",
        "NK",
        "CD8 T",
        "CD14+ Monocytes",
        "Dendritic",
        "Megakaryocytes",
    ]
    data.rename_categories("leiden", new_cluster_names)
    sc.pl.umap(
        data, color="leiden", legend_loc="on data", title="", frameon=False
    )
    plt.savefig(f"{output_path}/10_annotated_umap.png", bbox_inches="tight", dpi=300)
    plt.close()

    marker_genes = [
        *["IL7R", "CD79A", "MS4A1", "CD8A", "CD8B", "LYZ", "CD14"],
        *["LGALS3", "S100A8", "GNLY", "NKG7", "KLRB1"],
        *["FCGR3A", "MS4A7", "FCER1A", "CST3", "PPBP"],
    ]

    data.write(f"{output_path}/processed_data.h5ad")


