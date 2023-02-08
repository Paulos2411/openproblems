## VIASH START
par = {
    'input': './src/batch_integration/resources/datasets_pancreas.h5ad',
    'output': './src/batch_integration/resources/pancreas_bbknn.h5ad',
    'hvg': True,
    'scaling': True,
    'debug': True
}
## VIASH END

print('Importing libraries')
from pprint import pprint
import scanpy as sc
from scib.integration import scvi

if par['debug']:
    pprint(par)

adata_file = par['input']
output = par['output']
hvg = par['hvg']
scaling = par['scaling']

print('Read adata')
adata = sc.read_h5ad(adata_file)

if hvg:
    print('Select HVGs')
    adata = adata[:, adata.var['highly_variable']]

if scaling:
    print('Scale')
    adata.X = adata.layers['logcounts_scaled']
else:
    adata.X = adata.layers['logcounts']

print('Integrate')
adata = scvi(adata, batch='batch')

print('Postprocess data')
sc.pp.neighbors(adata, use_rep='X_emb')

print('Save HDF5')
adata.uns['method_id'] = meta['functionality_name']
adata.uns['hvg'] = hvg
adata.uns['scaled'] = scaling

adata.write(output, compression='gzip')
