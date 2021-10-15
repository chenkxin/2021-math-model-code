# prob 1
## 使用 datacleaner 进行数据清洗
```bash
pip install datacleaner
```
[datacleaner](https://github.com/rhiever/datacleaner)

```bash
datacleaner 1.csv -o 1.clean.csv -is , -os ,
```
得到 1.clean.csv, 中位数填充
```bash
datacleaner 1.csv -o 1.clean-drop-nans.csv -is , -os , --drop-nans
```
得到 1.clean-drop-nans.csv, 直接删除

## 添加表头， IAQI1..6, AQI
## 计算 AQI