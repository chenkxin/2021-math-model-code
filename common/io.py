"""
Author: QiangZiBro
Contact: Github/QiangZiBro
Time: 2021/10/15
"""
import pandas as pd
import matplotlib.pyplot as plt
import time
import concurrent
from threading import Thread

plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

FIGSIZE = (30, 25)
FORMAT = "svg"
PLACES = ['A', 'B', 'C', 'A1', 'A2', 'A3']
TYPES = [0, 1, 2]

def cal_time(func):
    def inner(args):
        start = time.time()
        result = func(args)
        end = time.time()
        print(f"{end-start}s passed")
        return result
    return inner



@cal_time
def load_tables(places=PLACES):
    df = {i:None for i in places}
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(places)) as executor:
        for p, result in zip(places, executor.map(load_table, places)):
            df[p] = result
    return df

def _load_data():
    print("Use 3 threads to read table...")
    tables = [None]*3
    def _read_table(f, pos):
        tables[pos] = pd.read_excel(f, engine='openpyxl', sheet_name=None)

    table_files = """data/附件1 监测点A空气质量预报基础数据.xlsx
data/附件2 监测点B、C空气质量预报基础数据.xlsx
data/附件3 监测点A1、A2、A3空气质量预报基础数据.xlsx""".split("\n")
    threads = []
    t1 = time.time()
    for i,e in enumerate(table_files):
        threads.append(Thread(target=_read_table, args=(e,i)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    keys = [list(i.keys()) for i in tables]  # 每个表格的sheet list
    print("Done, cost {}s".format(time.time() - t1))
    return tables, keys

def load_table(name):
    return pd.read_excel("data/"+name+".xlsx", engine='openpyxl', sheet_name=None)


def _process_to_json(tables):
    sheetnames = {0: '监测点{}逐小时污染物浓度与气象一次预报数据', 1: '监测点{}逐小时污染物浓度与气象实测数据', 2: '监测点{}逐日污染物浓度实测数据'}
    result = {i: {} for i in PLACES}

    for k, v in sheetnames.items():
        tables[0][v.format('A')].name = v.format('A')
        result['A'][k] = tables[0][v.format('A')]
    for c in ['B', 'C']:
        for k, v in sheetnames.items():
            tables[1][v.format(c)].name = v.format(c)
            result[c][k] = tables[1][v.format(c)]
    for c in ['A1', 'A2', 'A3']:
        for k, v in sheetnames.items():
            tables[2][v.format(c)].name = v.format(c)
            result[c][k] = tables[2][v.format(c)]
    return result


def load():
    """得到一个Json格式的数据项

    Return:
        {
            "A":{
                "0":DataFrame,
                "1":DataFrame,
                "2":DataFrame,
            }
            ...
        }
    """

    tables, keys = _load_data()
    return _process_to_json(tables)


if __name__ == '__main__':
    data = load()
