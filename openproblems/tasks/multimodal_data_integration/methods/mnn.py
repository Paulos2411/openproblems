from ....tools.decorators import method
from ....tools.normalize import log_cpm
from ....tools.normalize import log_scran_pooling
from ....tools.utils import check_version
from ....tools.conversion import r_function

_mnn = r_function("mnn.R", __file__)


@method(
    method_name="Mutual Nearest Neighbors (log CPM)",
    paper_name="Batch effects in single-cell RNA-sequencing data are corrected by "
    "matching mutual nearest neighbors",
    paper_url="https://www.nature.com/articles/nbt.4091",
    paper_year=2018,
    code_url="https://github.com/LTLA/batchelor",
    code_version=check_version("rpy2"),
    image="openproblems-r-extras",
)
def mnn_log_cpm(adata, n_svd=100):
    log_cpm(adata)
    log_cpm(adata, obsm="mode2", obs="mode2_obs", var="mode2_var")
    return _mnn(adata, n_svd=n_svd)


@method(
    method_name="Mutual Nearest Neighbors (log scran)",
    paper_name="Batch effects in single-cell RNA-sequencing data are corrected by "
    "matching mutual nearest neighbors",
    paper_url="https://www.nature.com/articles/nbt.4091",
    paper_year=2018,
    code_url="https://github.com/LTLA/batchelor",
    code_version=check_version("rpy2"),
    image="openproblems-r-extras",
)
def mnn_log_scran_pooling(adata, n_svd=100):
    log_scran_pooling(adata)
    log_cpm(adata, obsm="mode2", obs="mode2_obs", var="mode2_var")
    return _mnn(adata, n_svd=n_svd)
