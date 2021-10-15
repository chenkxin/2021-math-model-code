from threading import Thread
from common.io import *


def create_new_table_for_place(p):
    writer = pd.ExcelWriter("data/" + p + '.xlsx', engine='xlsxwriter')
    for i in range(3):
        df = data[p][i]

        if args.fillna == "mean":
            # 空值用中位数填充
            df.fillna(df.median())
        elif args.fillna == "mean":
            # 空值用均值填充
            df.fillna(df.mean())

        data[p][i].to_excel(writer, sheet_name=df.name)
    writer.save()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fillna", type=str, default="mean", choices=["mean", "median"] )
    args = parser.parse_args()
    print("Use {} to fillna".format(args.fillna))

    data = load()
    print("data load success")
    threads = []
    for p in PLACES:
        threads.append(Thread(target=create_new_table_for_place, args=(p,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Done")
