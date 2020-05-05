from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pandas as pd


def compute_embedding(df, method='pca', k=2, plot=False):
    df = df.fillna(0)

    columns = [col for col in df.columns if col != 'PatientID']

    x = df[columns].values

    if method == 'pca':
        pca = PCA(n_components=k)
        x = pca.fit_transform(x)

        if plot:
            pca_variance = pd.DataFrame({
                'values': pca.explained_variance_ratio_,
            })
            pca_variance['values'].plot(kind='line', style=['o-'])
            plt.show()
    elif method == 'tsne':
        tsne2 = TSNE(n_components=k, random_state=3)
        x = tsne2.fit_transform(x)
    else:
        raise ValueError('Invalid method.')

    return pd.concat([df[['PatientID']].reset_index(drop=True), pd.DataFrame(x)], axis=1)
