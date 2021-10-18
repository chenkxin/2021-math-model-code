import pandas as pd

KEYS = ["SO2监测浓度(μg/m³)", "NO2监测浓度(μg/m³)", "PM10监测浓度(μg/m³)", "PM2.5监测浓度(μg/m³)", "O3最大八小时滑动平均监测浓度(μg/m³)",
        "CO监测浓度(mg/m³)"]
dict = [
    [0, 50, 150, 475, 800, 1600, 2100, 2620],  # SO2
    [0, 40, 80, 180, 280, 565, 750, 940],  # NO2
    [0, 50, 150, 250, 350, 420, 500, 600],  # PM10
    [0, 35, 75, 115, 150, 250, 350, 500],  # P2.5
    [0, 100, 160, 215, 265, 800, 800, 800],  # O3
    [0, 2, 4, 14, 24, 36, 48, 60],  # CO
    [0, 50, 100, 150, 200, 300, 400, 500],  # 空气质量分指数
]


def compute_qualities(pollution_list):
    result = []
    for i, e in enumerate(pollution_list):
        length = 8  # 表格长度
        if i == 4:  # if now is O3, len is 6
            length = 6

        Cp = e
        # 与相近的污染物浓度限值的高位值与低位值
        j = 0
        min_ = dict[i][j]
        while Cp > min_ and j + 1 < length:
            j = j + 1
            min_ = dict[i][j]

        if Cp > min_:  # 污染物浓度过高， 不再计算
            result.append([])
            continue

        if Cp == min_:  # 相等的情况， j 往后取一位
            BPLo = min_
            BPHi = dict[i][j + 1]
            x = j  # x 是 BPHi 对应 IAQIHo 的位置
        else:
            if j - 1 >= 0:  # j 向前取， 需要小心数组越界
                j = j - 1
            BPLo = dict[i][j]
            BPHi = min_
            x = j  # x 是 BPHi 对应 IAQIHo 的位置

        IAQIHi = dict[6][x + 1]
        IAQILo = dict[6][x]
        result.append([BPLo, BPHi, Cp, IAQIHi, IAQILo])
    return result


def compute_aqi(so2, no2, pm10, pm25, o3, co):
    """
    :return: AQI
    """
    result = []
    qualities = compute_qualities([so2, no2, pm10, pm25, o3, co])
    for q in qualities:
        if q:
            result.append(compute_iaqi(q))
        else:
            result.append(0)
    print(result)
    return max(result)


def compute_iaqi(quality):
    # BPLo, BPHi, Cp, IAQIHi, IAQILo
    BPLo, BPHi, Cp, IAQIHi, IAQILo = quality
    if BPHi - BPLo == 0:
        print("warning: divided by zero")
        return 0
    IAQIp = (IAQIHi - IAQILo) / (BPHi - BPLo) * (Cp - BPLo) + IAQILo
    return round(IAQIp)


if __name__ == '__main__':
    so2 = 12
    no2 = 66
    pm10 = 83
    pm25 = 39
    o3 = 210
    co = 0.8

    # BPLo, BPHi, Cp, IAQIHi, IAQILo
    quality = compute_qualities([so2, no2, pm10, pm25, o3, co])
    q = quality[4]
    print("BPLo, BPHi, Cp, IAQIHi, IAQILo:", q)
    # print(compute_iaqi(q))
    data = ((8, 12, 27, 11, 112, 0.5),
    (7, 16, 24, 10, 92, 0.5),
    (7, 31, 37, 23, 169, 0.6),
    (8, 30, 47, 33, 201, 0.7))
    for i in data:
        print(compute_aqi(*i))
    print("so2, no2, pm10, pm25, o3, co")

    # should be 146
    # print(compute_aqi(so2, no2, pm10, pm25, o3, co))
