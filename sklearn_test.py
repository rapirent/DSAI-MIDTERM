from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import io
import csv
import requests

MAX_DEPTH = 30

DURATION_1 = '2018-04-13-0/2018-04-20-23'
PREDICT_DAY = 22
PREDICT_MONTH = 4

BJ_URL_1 = 'https://biendata.com/competition/airquality/bj/' + DURATION_1 +'/2k0d1d8'
LD_URL_1 = 'https://biendata.com/competition/airquality/ld/' + DURATION_1 + '/2k0d1d8'
WT_BJ_URL_2 = 'https://biendata.com/competition/airquality/bj/' + DURATION_1 + '/2k0d1d8'
WT_LD_URL_2 = 'https://biendata.com/competition/airquality/ld/' + DURATION_1 + '/2k0d1d8'
ID_LIST = ['dongsi_aq', 'tiantan_aq', 'guanyuan_aq', 'wanshouxigong_aq', 'aotizhongxin_aq', 'nongzhanguan_aq', 'wanliu_aq', 'beibuxinqu_aq', 'zhiwuyuan_aq', 'fengtaihuayuan_aq', 'yungang_aq', 'gucheng_aq', 'fangshan_aq', 'daxing_aq', 'yizhuang_aq', 'tongzhou_aq', 'shunyi_aq', 'pingchang_aq', 'mentougou_aq', 'pinggu_aq',
           'huairou_aq', 'miyun_aq', 'yanqin_aq', 'dingling_aq', 'badaling_aq', 'miyunshuiku_aq', 'donggaocun_aq', 'yongledian_aq', 'yufa_aq', 'liulihe_aq', 'qianmen_aq', 'yongdingmennei_aq', 'xizhimenbei_aq', 'nansanhuan_aq', 'dongsihuan_aq', 'CD1', 'BL0', 'GR4', 'MY7', 'HV1', 'GN3', 'GR9', 'LW2', 'GN0', 'KF1', 'CD9', 'ST5', 'TH4']
OUTPUT_FILE_NAME = 'test.csv'
QUERY_NAME = ['PM25_Concentration', 'PM10_Concentration', 'O3_Concentration']

def crawler(decoded_content, data_index, day, month, hour, pm25, pm10, o3):
    reader = csv.DictReader(decoded_content, delimiter=',')

    for row in reader:
        date = row['time'].split(' ')
        if '-' in date[0]:
            encoding_date = date[0].split('-')
        else:
            encoding_date = date[0].split('/')
        if row['station_id'] not in ID_LIST:
            continue
        if (not row['PM25_Concentration']) or (not row['PM10_Concentration']) or (not row['O3_Concentration']):
            continue
        data_index.append(ID_LIST.index(row['station_id']))
        # 2018-04-12 00:00:00
        hour.append(int(date[1].split(':')[0]))
        pm25.append(float(row['PM25_Concentration']))
        pm10.append(float(row['PM10_Concentration']))
        o3.append(float(row['O3_Concentration']))
        day.append(encoding_date[2])
        month.append(encoding_date[1])

    return (data_index, day, month, hour, pm25, pm10, o3)

if __name__ == '__main__':
    data_index, day, month, hour, pm25, pm10, o3 = ([], [], [], [], [], [], [])

    a = requests.get(BJ_URL_1)
    decoded_content = a.content.decode('utf-8')
    data_index, day, month, hour, pm25, pm10, o3 = crawler(decoded_content.splitlines(), data_index, day, month, hour, pm25, pm10, o3)

    a = requests.get(LD_URL_1)
    decoded_content = a.content.decode('utf-8')
    data_index, day, month, hour, pm25, pm10, o3 = crawler(decoded_content.splitlines(), data_index, day, month, hour, pm25, pm10, o3)

    bj_old_file = open('beijing_17_18_aq.csv', newline='')
    data_index, day, month, hour, pm25, pm10, o3 = crawler(bj_old_file, data_index, day, month, hour, pm25, pm10, o3)

    ld_old_file = open('London_historical_aqi_forecast_stations_20180331.csv', newline='')
    data_index, day, month, hour, pm25, pm10, o3 = crawler(ld_old_file, data_index, day, month, hour, pm25, pm10, o3)

    X_train = np.array([day, month, data_index, hour])
    y_train = np.array([pm25, pm10, o3])
    regr_rf = RandomForestRegressor(max_depth=MAX_DEPTH, random_state=2)
    regr_rf.fit(X_train, y_train)

    first_day = np.zeros(24*len(ID_LIST))
    next_day = np.zeros(24*len(ID_LIST))
    predict_day = first_day.fill(PREDICT_DAY+1) + next_day.fill(PREDICT_DAY+2)
    predict_hour = np.array(list(range(0,24))*len(ID_LIST)*2)
    predict_month = np.zero(48*len(ID_LIST))
    predict_month.fill(PREDICT_MONTH)
    predict_index = np.array(list(range(len(ID_LIST))))
    predict_index.repeat(24)
    X_predict = np.array([predict_day, predict_month, predict_index, predict_hour])
    y_rf = regr_rf.predict(X_predict)
    print(y_rf)
