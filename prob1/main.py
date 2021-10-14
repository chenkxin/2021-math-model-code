import pandas as pd

# 中位数填充
# file_path = "./1.clean.csv"
# output_path = "1.clean.csv"

# drop, 直接删除无效值所在行
file_path = "./1.clean-drop-nans.csv"
output_path = "1.AQI.drop-nans.csv"
data = pd.read_csv(file_path)

# print("获取到所有的值:\n{0}".format(data))

KEYS = ["SO2监测浓度(μg/m³)", "NO2监测浓度(μg/m³)", "PM10监测浓度(μg/m³)", "PM2.5监测浓度(μg/m³)", "O3最大八小时滑动平均监测浓度(μg/m³)", "CO监测浓度(mg/m³)"]
dict = [
        [0, 50, 150, 475, 800, 1600, 2100, 2620], # SO2
        [0, 40, 80, 180, 280, 565, 750, 940],  # NO2
        [0, 50, 150, 250, 350, 420, 500, 600], # PM10
        [0, 35, 75, 115, 150, 250 ,350, 500], # P2.5
        [0, 100, 160, 215, 265, 800, 800, 800], # O3
        [0, 2, 4, 14, 24, 36, 48, 60], # CO
        [0, 50, 100, 150, 200, 300, 400, 500], # 空气质量分指数
]

for index, row in data.iterrows():
    for i in range(6):
        # print(i)
        len = 8  # 表格长度
        if i == 4:  # if now is O3, len is 6
            len = 6
        IAQIp = 0
        BPLo = 0
        BPHi = 0
        IAQIHi = 0
        IAQILo = 0
        x = 0  # x 是 BPHi 对应 IAQIHo 的位置
        Cp = row[KEYS[i]]
        # 与相近的污染物浓度限值的高位值与低位值
        j = 0
        min = dict[i][j]
        while Cp > min and j + 1 < len:
            j = j + 1
            min = dict[i][j]

        if Cp > min: # 污染物浓度过高， 不再计算
            IAQIp = 0
            continue

        if Cp == min: # 相等的情况， j 往后取一位
            BPLo = min
            BPHi = dict[i][j + 1]
            x = j  # x 是 BPHi 对应 IAQIHo 的位置
        else:
            if j - 1 >= 0: # j 向前取， 需要小心数组越界
                j = j - 1
            BPLo = dict[i][j]
            BPHi = min
            x = j  # x 是 BPHi 对应 IAQIHo 的位置

        IAQIHi = dict[6][x]
        IAQILo = dict[6][x + 1]

        IAQIp = (IAQIHi - IAQILo) / (BPHi - BPLo) * (Cp - BPLo) + IAQILo
        data.iloc[index, i + 6] = round(IAQIp)
        # print(IAQIp)

    AQI = max(data.iloc[index, 6], data.iloc[index, 7], data.iloc[index, 8], data.iloc[index, 9], data.iloc[index, 10], data.iloc[index, 11])
    print(BPLo, BPHi, Cp, IAQIHi, IAQILo, IAQIp, AQI)
    data.iloc[index, 12] = AQI

data.to_csv(output_path, sep=',', index=False)