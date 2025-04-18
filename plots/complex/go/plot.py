# import rpy2.robjects as robjects
# from rpy2.robjects import pandas2ri
# import pandas as pd

# ### R语言版本调用
# # 初始化 rpy2 和 pandas 转换
# pandas2ri.activate()
#
# # 定义 R 脚本
# r_script = """
# # 安装必要的 R 包（如果尚未安装）
# if (!require("clusterProfiler")) install.packages("clusterProfiler")
# if (!require("org.Hs.eg.db")) install.packages("org.Hs.eg.db", repos="http://bioconductor.org/packages/release/bioc")
# if (!require("enrichplot")) install.packages("enrichplot")
# if (!require("ggplot2")) install.packages("ggplot2")
#
# library(clusterProfiler)
# library(org.Hs.eg.db)
# library(enrichplot)
# library(ggplot2)  # 加载 ggplot2 包
#
# # 定义基因名称到 ID 的转换函数
# symbol_to_entrez <- function(gene_symbols) {
#     entrez_ids <- unlist(mapIds(org.Hs.eg.db, keys=gene_symbols, column="ENTREZID", keytype="SYMBOL"))
#     return(entrez_ids)
# }
#
# # 定义富集分析函数
# perform_enrichment_analysis <- function(gene_symbols, species, analysis_type, top_n, output_file, plot_file = NULL) {
#     # 转换基因名称为基因 ID
#     gene_ids <- symbol_to_entrez(gene_symbols)
#     if (length(gene_ids) == 0) {
#         stop("没有找到对应的基因 ID，请检查输入的基因名称")
#     }
#
#     # 根据物种选择注释数据库
#     if (species == "human") {
#         anno_db <- org.Hs.eg.db
#     } else if (species == "mouse") {
#         anno_db <- org.Mm.eg.db
#     } else {
#         stop("不支持的物种，请选择 'human' 或 'mouse'")
#     }
#
#     # 执行富集分析
#     if (analysis_type == "go") {
#         enrich_result <- enrichGO(gene = gene_ids, ont = "ALL", pAdjustMethod = "BH", pvalueCutoff = 0.05, readable = TRUE, OrgDb = anno_db)
#     } else if (analysis_type == "kegg") {
#         enrich_result <- enrichKEGG(gene = gene_ids, organism = species, pAdjustMethod = "BH", pvalueCutoff = 0.05)
#     } else {
#         stop("未知的分析类型，请选择 'go' 或 'kegg'")
#     }
#
#     # 检查富集结果是否为空
#     if (is.null(enrich_result)) {
#         stop("富集分析结果为空，请检查输入的基因列表和参数")
#     }
#
#     # 绘制结果
#     p <- dotplot(enrich_result, showCategory = top_n) + ggtitle(paste0("Top ", top_n, " ", analysis_type, " Enrichment"))
#
#     # 保存结果
#     write.csv(as.data.frame(enrich_result), file = output_file)
#
#     # 如果指定了 plot_file，则保存图片
#     if (!is.null(plot_file)) {
#         ggsave(filename = plot_file, plot = p, device = "png", width = 8, height = 6)
#     }
#
#     # 返回结果
#     return(enrich_result)
# }
# """
#
# # 将 R 脚本传递给 R 运行环境
# robjects.r(r_script)
#
# # 定义 Python 函数来调用 R 函数
# def perform_enrichment_analysis(gene_list, species="human", analysis_type="go", top_n=20,
#                                 output_file="enrichment_results.csv", plot_file=None):
#     """
#     使用 clusterProfiler 进行基因富集分析。
#
#     parameters:
#     - parameter: gene_list: 输入的基因列表（基因名称）
#     - parameter: species: 物种名称，支持 'human' 和 'mouse'
#     - parameter: analysis_type: 分析类型，'go' 或 'kegg'
#     - parameter: top_n: 显示前 N 个富集结果
#     - parameter: output_file: 结果输出文件路径
#     - parameter: plot_file: 图片保存路径，如果为 None 则不保存图片
#     """
#     # 转换基因列表为 R 向量
#     r_gene_list = robjects.StrVector(gene_list)
#
#     # 调用 R 函数
#     enrich_result = robjects.r['perform_enrichment_analysis'](r_gene_list, species, analysis_type, top_n, output_file, plot_file)
#
#     # 检查富集结果是否为空
#     if enrich_result is None:
#         raise ValueError("富集分析结果为空，请检查输入的基因列表和参数")
#
#     # 将结果转换为 Pandas DataFrame
#     result_df = pd.read_csv(output_file)
#
#     return result_df
#
#
# if __name__ == "__main__":
#     # 示例基因列表
#     gene_list = ["TP53", "EGFR", "BRCA1", "KRAS", "PTEN", "ALDH1A1", "FOLH1", "MSLN", "DAB2", "STEAP2"]
#
#     # 进行 GO 富集分析并保存图片
#     go_result = perform_enrichment_analysis(
#         gene_list,
#         species="human",
#         analysis_type="go",
#         top_n=20,
#         output_file="go_enrichment_results.csv",
#         plot_file="go_enrichment_plot.png"
#     )
#     print("GO 富集分析结果:")
#     print(go_result.head())
#
#     # 进行 KEGG 富集分析并保存图片
#     kegg_result = perform_enrichment_analysis(
#         gene_list,
#         species="human",
#         analysis_type="kegg",
#         top_n=20,
#         output_file="kegg_enrichment_results.csv",
#         plot_file="kegg_enrichment_plot.png"
#     )
#     print("KEGG 富集分析结果:")
#     print(kegg_result.head())

import gseapy as gp

args = None
data = None

def plot(args, data):

    gene_list = ["TP53", "EGFR", "BRCA1", "KRAS", "PTEN", "ALDH1A1", "FOLH1", "MSLN", "DAB2", "STEAP2"]

    enr = gp.enrichr(
        gene_list=gene_list,
        gene_sets=['KEGG_2016', 'KEGG_2013'],
        organism='Human',
        outdir="./enrichr",
        cutoff=0.05,
        top_term=20
    )

    print(enr.results.head(5))

plot(args, data)