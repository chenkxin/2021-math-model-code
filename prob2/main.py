import seaborn as sns
from sklearn.cluster import SpectralClustering
from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = ['Noto Serif CJK JP']
#
# #get correlations of each features in dataset
# data = pd.read_excel('data/A.xlsx', engine='openpyxl', header=None, usecols='E:S', sheet_name='0')
# data = np.array(data.iloc[1:, :]).T
# print(data.shape)

if __name__ == '__main__':
    # X, y = datasets.make_blobs(n_samples=500, n_features=6, centers=5, cluster_std=[0.4, 0.3, 0.4, 0.3, 0.4],random_state=11)
    # clustering = SpectralClustering(n_clusters=5, assign_labels="discretize", gamma=1.0).fit_predict(data)
    # print(clustering.labels_)
    data = pd.read_excel('data/A.xlsx', engine='openpyxl', usecols='E:S', header=None, sheet_name='0')
    data.head()
    print(data)
    corrmat = data.corr()
    top_corr_features = corrmat.index
    plt.figure(figsize=(20, 20))
    # plot heat map
    corr = data[top_corr_features].corr()
    mask = np.zeros_like(corr, dtype=np.bool)  # 构造与corr同维数矩阵为bool型矩阵
    mask[np.triu_indices_from(mask)] = True  # 角分线右侧为True
    g = sns.heatmap(corr, mask=mask, square=True, annot=True, cmap="RdYlGn")
    plt.savefig('./prob2/pics/heatmap')
    plt.show()