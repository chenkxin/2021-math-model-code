from threading import Thread
from common.io import *


def create_new_table_for_place(p):
    writer = pd.ExcelWriter("data/" + p + '.xlsx', engine='xlsxwriter')
    for i in range(3):
        data[p][i].to_excel(writer, sheet_name=data[p][i].name)
    writer.save()


if __name__ == '__main__':
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
