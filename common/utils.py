import pandas as pd
POLLUTIONS = ["SO2", "NO2", "PM10", "PM2.5", "O3", "CO"]

def remove_outlier(df_in, col_name):
    df_in[col_name] = df_in[col_name].apply(pd.to_numeric, errors='coerce')
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out

def remove_outlier_from_multi_cols(df_in, col_names):
    for c in col_names:
        df_in = remove_outlier(df_in, c)
    return df_in


def find_pollution_columns(data):
    result = []
    for name in POLLUTIONS:
        for i in data.columns:
            if i.startswith(name):
                result.append(i)
    return result

def get_useful_features(df):
    index = df.columns[list(df.columns).index('地点')+1:]
    return df[index]

def get_useful_indexes(df):
    return df.columns[list(df.columns).index('地点')+1:]


def write_excel(name, frame):
    writer = pd.ExcelWriter("data/" + name + '.xlsx', engine='xlsxwriter')
    for i in range(3):
        frame[str(i)].to_excel(writer, sheet_name=str(i))
    writer.save()