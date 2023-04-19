import anndata as ad
import subprocess
from os import path

input_prediction_path = meta["resources_dir"] + "/pancreas/knn.h5ad"
input_solution_path = meta["resources_dir"] + "/pancreas/solution.h5ad"
output_path = "output.h5ad"

cmd = [
  meta['executable'],
  "--input_prediction", input_prediction_path,
  "--input_solution", input_solution_path,
  "--output", output_path
]

print(">> Running script as test")
out = subprocess.check_output(cmd).decode("utf-8")

print(">> Checking whether output file exists")
assert path.exists(output_path)

input_solution = ad.read_h5ad(input_solution_path)
input_prediction = ad.read_h5ad(input_prediction_path)
output = ad.read_h5ad(output_path)

print("Checking whether data from input was copied properly to output")
assert output.uns["dataset_id"] == input_prediction.uns["dataset_id"]
assert output.uns["method_id"] == input_prediction.uns["method_id"]
assert output.uns["metric_ids"] is not None
assert output.uns["metric_values"] is not None

# TODO: check whether the metric ids are all in .functionality.info

print("All checks succeeded!")
