import pandas as pd
import scanpy as sc


def data_processing(args, adata):
    sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
    # sc.logging.print_header()
    sc.settings.set_figure_params(dpi=80, facecolor="white")

    # make unique var names (unique gene ids)
    adata.var_names_make_unique()  # this is unnecessary if using `var_names='gene_ids'` in `sc.read_10x_mtx`

    return args, adata
