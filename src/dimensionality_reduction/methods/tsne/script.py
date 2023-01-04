import anndata as ad
import scanpy as sc
import yaml

## VIASH START
par = {
    'input': 'resources_test/common/pancreas/train.h5ad',
    'output': 'reduced.h5ad',
    'n_pca': 50,
}
meta = {
    'functionality_name': 'tsne',
    'config': 'src/dimensionality_reduction/methods/tsne/config.vsh.yaml'
}
## VIASH END

print("Load input data", flush=True)
input = ad.read_h5ad(par['input'])

print('Select top 1000 high variable genes', flush=True)
n_genes = 1000
idx = input.var['hvg_score'].to_numpy().argsort()[::-1][:n_genes]
input = input[:, idx].copy()
print('Apply PCA with 50 dimensions', flush=True)
input.obsm['X_pca_hvg'] = sc.tl.pca(input.layers['normalized'], n_comps=par['n_pca'], svd_solver="arpack")

print('Run t-SNE', flush=True)
sc.tl.tsne(input, use_rep="X_pca_hvg", n_pcs=par['n_pca'])
input.obsm["X_emb"] = input.obsm["X_tsne"].copy()

print('Add method ID', flush=True)
input.uns['method_id'] = meta['functionality_name']

print('Copy data to new AnnData object', flush=True)
output = ad.AnnData(
    obs=input.obs[[]],
    uns={}
)
output.obsm['X_emb'] = input.obsm['X_emb']
output.uns['dataset_id'] = input.uns['dataset_id']
output.uns['normalization_id'] = input.uns['normalization_id']
output.uns['method_id'] = input.uns['method_id']

print("Write output to file", flush=True)
output.write_h5ad(par['output'], compression="gzip")