import sys
sys.path.append(".")
sys.path.append("..")
import pandas as pd
import aqi
from common.io import PLACES

pollutions = ["SO2", "NO2", "PM10", "PM2.5", "O3", "CO"]


def _find_pollution_columns(data):
    result = []
    for name in pollutions:
        for i in data.columns:
            if i.startswith(name):
                result.append(i)
    return result


def compute_aqi_for_table(table_name):
    # read
    table = pd.read_excel(table_name, engine='openpyxl', sheet_name=None)
    print("Load table done")
    sheetnames = {0: '0', 1: '1', 2: '2'}
    result = {'A': {}}

    for k, v in sheetnames.items():
        table[v.format('A')].name = v.format('A')
        result['A'][k] = table[v.format('A')]

    # compute aqi
    writer = pd.ExcelWriter(table_name, engine='xlsxwriter')
    for partition in range(3):
        data = result['A'][partition]
        table_head = _find_pollution_columns(data)
        if table_head is None:
            raise Exception("Didn't find enough table head")
        length = len(data.iloc[0])
        data.insert(length, "AQI", 0)

        res_aqi = []
        pollution_data = [data[i] for i in table_head]
        for i in zip(*pollution_data):
            res_aqi.append(aqi.compute_aqi(*i))
        data['AQI'] = res_aqi
        data.to_excel(writer, sheet_name=str(partition))
        print(partition, " compute done")

    writer.close()
    print(table_name, " has been processed")


def compute_aqi_for_all_tables():
    for f in ["data/" + i + ".xlsx" for i in PLACES]:
        compute_aqi_for_table(f)


if __name__ == '__main__':
    compute_aqi_for_all_tables()
