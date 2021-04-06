## VIASH START
par = {
    "input_rna": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE100866&format=file&file=GSE100866%5FCBMC%5F8K%5F13AB%5F10X%2DRNA%5Fumi%2Ecsv%2Egz",
    "input_adt": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE100866&format=file&file=GSE100866%5FCBMC%5F8K%5F13AB%5F10X%2DADT%5Fumi%2Ecsv%2Egz",
    "output": "output.h5ad",
    "test": False
}
resources_dir = "..."
## VIASH END

print("Running imports")
import sys
sys.path.append(resources_dir)
from utils import create_joint_adata
from utils import filter_joint_data_empty_cells
from utils import subset_joint_data
import scprep

print("(Down)loading expression datasets from GEO")
sys.stdout.flush()

rna_data = scprep.io.load_csv(
    par["input_rna"], cell_axis="col", compression="gzip", sparse=True, chunksize=1000
)
adt_data = scprep.io.load_csv(
    par["input_adt"], cell_axis="col", compression="gzip", sparse=True, chunksize=1000
)

print("Transforming into adata")
adata = create_joint_adata(rna_data, adt_data)
adata = filter_joint_data_empty_cells(adata)

if par["test"]:
    print("Subsetting dataset")
    adata = subset_joint_data(adata)

print("Writing adata to file")
adata.write(par["output"])