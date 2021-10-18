import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = ['Noto Serif CJK JP']

# x = [1,2,3,4,5,6,7,8,9,10]
x = np.arange(10)
print(x)
y = np.random.rand(10)
y2 = np.random.rand(10)
plt.style.use('ggplot')
plt.figure(figsize=(10,5))
plt.title("上证50指数历史最高价、收盘价走势折线图")
plt.xlabel("??")
plt.xticks(ticks=x, rotation=45, labels=x)
plt.xticks(rotation=45)
plt.ylabel("指数")
plt.plot_date(x,y,'-',label="收盘价")
plt.plot_date(x,y2,'-',label="最高价")
plt.legend()
plt.show()
plt.grid(True)