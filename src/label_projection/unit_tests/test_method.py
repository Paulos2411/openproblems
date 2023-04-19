import anndata as ad
import subprocess
from os import path

input_train_path = meta["resources_dir"] + "/pancreas/train.h5ad"
input_test_path = meta["resources_dir"] + "/pancreas/test.h5ad"
input_solution_path = meta["resources_dir"] + "/pancreas/solution.h5ad"
output_path = "output.h5ad"

cmd = [
  meta['executable'],
  "--input_train", input_train_path,
  "--input_test", input_test_path,
  "--output", output_path
]

# todo: if we could access the viash config, we could check whether
# .functionality.info.type == "positive_control"
if meta['functionality_name'] == 'true_labels':
  cmd = cmd + ["--input_solution", input_solution_path]

print(">> Running script as test")
out = subprocess.check_output(cmd).decode("utf-8")

print(">> Checking whether output file exists")
assert path.exists(output_path)

print(">> Reading h5ad files")
input_test = ad.read_h5ad(input_test_path)
output = ad.read_h5ad(output_path)
print("input_test:", input_test)
print("output:", output)

print(">> Checking whether predictions were added")
assert "label_pred" in output.obs
assert meta['functionality_name'] == output.uns["method_id"]

print("Checking whether data from input was copied properly to output")
assert input_test.n_obs == output.n_obs
assert input_test.uns["dataset_id"] == output.uns["dataset_id"]

print("All checks succeeded!")