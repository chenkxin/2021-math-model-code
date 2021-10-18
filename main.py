import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# Linux上解决字体问题
from common.io import load_table, PLACES

plt.rcParams['font.sans-serif'] = ['Noto Serif CJK JP']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')

for p in PLACES:
    data = load_table(p)
    for i in range(3):
        df = data[str(i)]
        index = list(df.columns).index('地点') + 1
        df1 = df[df.columns[index:]]
        corrmat = df1.corr()

        top_corr_features = corrmat.index
        fig = plt.figure(figsize=(12, 8))
        # plot heat map
        mask = np.zeros_like(corrmat, dtype=np.bool)  # 构造与corr同维数矩阵为bool型矩阵
        mask[np.triu_indices_from(mask)] = True  # 角分线右侧为True
        g = sns.heatmap(df1[top_corr_features].corr(), annot_kws={"size": 8}, mask=mask, annot=True, cmap="RdYlGn")
        fig.tight_layout()
        plt.savefig(f"{p}-{i}相关性分析.pdf", format="pdf")
        plt.close()