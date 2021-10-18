import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, MiniBatchKMeans

# 主程序
def main():
    # 读取数据文件
    readPath = "data/A.xlsx"  # 数据文件的地址和文件名
    table = pd.read_excel(readPath, engine='openpyxl', sheet_name=0, header=0)
    # print(dfFile.dtypes)  # 查看 df 各列的数据类型
    # print(dfFile.shape)  # 查看 df 的行数和列数
    print(dfFile.head())

    # 数据准备
    z_scaler = lambda x:(x-np.mean(x))/np.std(x)  # 定义数据标准化函数
    dfScaler = dfFile[['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10']].apply(z_scaler)  # 数据归一化
    dfData = pd.concat([dfFile[['地区']], dfScaler], axis=0)  # 行级别合并
    df = dfData.loc[:,['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10']]  # 基于全部 10个特征聚类分析
    # df = dfData.loc[:,['x1','x2','x7','x8','x9','x10']]  # 降维后选取 6个特征聚类分析
    X = np.array(df)  # 准备 sklearn.cluster.KMeans 模型数据
    print("Shape of cluster data:", X.shape)

    # KMeans 聚类分析(sklearn.cluster.KMeans)
    nCluster = 4
    kmCluster = KMeans(n_clusters=nCluster).fit(X)  # 建立模型并进行聚类，设定 K=2
    print("Cluster centers:\n", kmCluster.cluster_centers_)  # 返回每个聚类中心的坐标
    print("Cluster results:\n", kmCluster.labels_)  # 返回样本集的分类结果

    # 整理聚类结果
    listName = dfData['地区'].tolist()  # 将 dfData 的首列 '地区' 转换为 listName
    dictCluster = dict(zip(listName,kmCluster.labels_))  # 将 listName 与聚类结果关联，组成字典
    listCluster = [[] for k in range(nCluster)]
    for v in range(0, len(dictCluster)):
        k = list(dictCluster.values())[v]  # 第v个城市的分类是 k
        listCluster[k].append(list(dictCluster.keys())[v])  # 将第v个城市添加到 第k类
    print("\n聚类分析结果(分为{}类):".format(nCluster))  # 返回样本集的分类结果
    for k in range(nCluster):
        print("第 {} 类：{}".format(k, listCluster[k]))  # 显示第 k 类的结果

    return

# === 关注 Youcans，分享更多原创系列 https://www.cnblogs.com/youcans/ ===
if __name__ == '__main__':
    main()
