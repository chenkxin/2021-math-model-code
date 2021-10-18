import pandas as pd
import aqi
from common.io import PLACES
import numpy as np

if __name__ == '__main__':
    # compute_aqi_for_all_tables()
    # compute_aqi_for_table()
    table = pd.read_excel('data/A.xlsx', engine='openpyxl', sheet_name=None)
    sheetnames = {0: '0', 1: '1', 2: '2'}
    result = {'A': {}}

    for k, v in sheetnames.items():
        table[v.format('A')].name = v.format('A')
        result['A'][k] = table[v.format('A')]

    writer = pd.ExcelWriter('data/A.xlsx', engine='xlsxwriter')
    for partition in range(3):
        data = result['A'][partition]
        length = len(data.iloc[0])
        data.insert(length, "bool", 0)
        print(data)

        res = []
        aqi_column = data['AQI']
        for i in range(len(data)):
            aqi = aqi_column[i]
            if 50 >= aqi >= 0:
                res.append(0)
            elif 100 >= aqi >= 51:
                res.append(1)
            elif 150 >= aqi >= 100:
                res.append(2)
            elif 200 >= aqi >= 151:
                res.append(3)
            elif 300 >= aqi >= 201:
                res.append(4)
            elif aqi >= 301:
                res.append(5)
        data['bool'] = res
        data.to_excel(writer, sheet_name=str(partition))
        print(partition, " compute done")

    writer.close()
    print(" has been processed")