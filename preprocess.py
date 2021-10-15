from threading import Thread
from common.io import *
import numpy as np


def create_new_table_for_place(p):
    writer = pd.ExcelWriter("data/" + p + '.xlsx', engine='xlsxwriter')
    for i in range(3):
        df = data[p][i]

        # 负值处理
        num = df._get_numeric_data()
        num[num < 0] = np.nan

        if args.fillna == "mean":
            # 空值用中位数填充
            df = df.fillna(df.median())
        elif args.fillna == "mean":
            # 空值用均值填充
            df = df.fillna(df.mean())

        df.to_excel(writer, sheet_name=str(i))
    writer.save()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fillna",
                        type=str,
                        default="mean",
                        choices=["mean", "median"])
    args = parser.parse_args()
    print("Use {} to fillna".format(args.fillna))

    data = load()
    print("data load success")
    threads = []
    for p in PLACES:
        threads.append(Thread(target=create_new_table_for_place, args=(p, )))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Done")
