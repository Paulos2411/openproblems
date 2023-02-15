import anndata as ad
from scib.metrics import silhouette

## VIASH START
par = {
    'input_integrated': 'resources_test/batch_integration/embedding/scvi.h5ad',
    'input_solution': 'resources_test/batch_integration/pancreas/solution.h5ad',
    'output': 'output.h5ad',
}

meta = {
    'functionality_name': 'foo',
}
## VIASH END

print('Read input', flush=True)
adata = ad.read_h5ad(par['input_integrated'])
adata_solution = ad.read_h5ad(par['input_solution'])

print('Transfer obs annotations')
adata.obs['label'] = adata_solution.obs['label'][adata.obs_names]

print('compute score')
score = silhouette(
    adata,
    group_key='label',
    embed='X_emb'
)

print("Create output AnnData object")
output = ad.AnnData(
    uns={
        "dataset_id": adata.uns['dataset_id'],
        'normalization_id': adata.uns['normalization_id'],
        "method_id": adata.uns['method_id'],
        "hvg": adata.uns['hvg'],
        "output_type": adata.uns['output_type'],
        "metric_ids": [meta['functionality_name']],
        "metric_values": [score]
    }
)

if 'parent_method_id' in adata.uns:
    output.uns['parent_method_id'] = adata.uns['parent_method_id']

print("Write data to file", flush=True)
output.write_h5ad(par["output"], compression="gzip")
