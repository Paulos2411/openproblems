from ....tools.decorators import method
from ....tools.normalize import log_cpm
from ....tools.utils import check_version

import numpy as np
import sklearn.decomposition


@method(
    method_name="Random Features",
    paper_name="Random Features (baseline)",
    paper_url="https://openproblems.bio",
    paper_year=2022,
    code_url="https://github.com/openproblems-bio/openproblems",
    is_baseline=True,
)
def random_features(adata, test=False, n_svd=20):
    n_svd = min([n_svd, min(adata.X.shape) - 1, min(adata.obsm["mode2"].shape) - 1])
    adata = log_cpm(adata)
    X_pca = sklearn.decomposition.TruncatedSVD(n_svd).fit_transform(adata.X)
    adata.obsm["aligned"] = X_pca[np.random.permutation(np.arange(adata.shape[0]))]
    adata.obsm["mode2_aligned"] = X_pca[
        np.random.permutation(np.arange(adata.shape[0]))
    ]
    adata.uns["method_code_version"] = check_version("openproblems")
    return adata


@method(
    method_name="True Features",
    paper_name="True Features (baseline)",
    paper_url="https://openproblems.bio",
    paper_year=2022,
    code_url="https://github.com/openproblems-bio/openproblems",
    is_baseline=True,
)
def true_features(adata, test=False, n_svd=20):
    n_svd = min([n_svd, min(adata.X.shape) - 1, min(adata.obsm["mode2"].shape) - 1])
    adata = log_cpm(adata)
    X_pca = sklearn.decomposition.TruncatedSVD(n_svd).fit_transform(adata.X)
    adata.obsm["aligned"] = X_pca
    adata.obsm["mode2_aligned"] = X_pca
    adata.uns["method_code_version"] = check_version("openproblems")
    return adata
