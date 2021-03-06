import csv
import requests

ID_LIST = ['dongsi_aq', 'tiantan_aq', 'guanyuan_aq', 'wanshouxigong_aq', 'aotizhongxin_aq', 'nongzhanguan_aq', 'wanliu_aq', 'beibuxinqu_aq', 'zhiwuyuan_aq', 'fengtaihuayuan_aq', 'yungang_aq', 'gucheng_aq', 'fangshan_aq', 'daxing_aq', 'yizhuang_aq', 'tongzhou_aq', 'shunyi_aq', 'pingchang_aq', 'mentougou_aq', 'pinggu_aq',
           'huairou_aq', 'miyun_aq', 'yanqin_aq', 'dingling_aq', 'badaling_aq', 'miyunshuiku_aq', 'donggaocun_aq', 'yongledian_aq', 'yufa_aq', 'liulihe_aq', 'qianmen_aq', 'yongdingmennei_aq', 'xizhimenbei_aq', 'nansanhuan_aq', 'dongsihuan_aq', 'CD1', 'BL0', 'GR4', 'MY7', 'HV1', 'GN3', 'GR9', 'LW2', 'GN0', 'KF1', 'CD9', 'ST5', 'TH4']
OUTPUT_FILE_NAME = 'sub-0424-1.csv'

QUERY_NAME = ['PM25_Concentration', 'PM10_Concentration', 'O3_Concentration']

def crawler(url, value, count):
    # a = requests.get(url)

    # decoded_content = a.content.decode('utf-8')
    reader = csv.DictReader(url, delimiter=',')

    for row in reader:
        date = row['time'].split(' ')
        time = date[1].split(':')[0]
        if row['station_id'] not in ID_LIST:
            continue
        for name in QUERY_NAME:
            if row[name]:
                value[row['station_id']][str(time)][name] += float(row[name])
                count[row['station_id']][str(time)][name] += 1

    return (value, count)

if __name__ == '__main__':

    value_dict = {name:
                {str(num).zfill(2): {'PM10_Concentration': 0, 'PM25_Concentration': 0,
                                    'O3_Concentration': 0} for num in range(0, 24)}
                for name in ID_LIST}

    count_dict = {name:
                {str(num).zfill(2): {'PM10_Concentration': 0, 'PM25_Concentration': 0,
                                    'O3_Concentration': 0} for num in range(0, 24)}
                for name in ID_LIST}

    # value_dict, count_dict = crawler(BJ_URL_1, value_dict, count_dict)
    # value_dict, count_dict = crawler(LD_URL_1, value_dict, count_dict)
    bj_old_file = open('beijing_17_18_aq.csv', newline='')
    value_dict, count_dict = crawler(bj_old_file, value_dict, count_dict)
    ld_old_file = open('London_historical_aqi_forecast_stations_20180331.csv', newline='')
    value_dict, count_dict = crawler(ld_old_file, value_dict, count_dict)

    for key, value in value_dict.items():
        for time_key, time_value in value.items():
            for element_key in time_value.keys():
                if count_dict[key][time_key][element_key]:
                    value_dict[key][time_key][element_key] /= count_dict[key][time_key][element_key]


    write_file = open(OUTPUT_FILE_NAME, 'w')
    print(OUTPUT_FILE_NAME)
    print('test_id,PM2.5,PM10,O3', file=write_file)

    for key, value in value_dict.items():
        for time_key, time_value in value.items():
            print(key, file=write_file, end='')
            print('#',int(time_key), file=write_file,end='',sep='')
            for name in QUERY_NAME:
                print(',', int(round(value_dict[key][time_key][name])), file=write_file, end='', sep='')
            print('',file=write_file,end='\n')

    for key, value in value_dict.items():
        for time_key, time_value in value.items():
            print(key, file=write_file, end='')
            print('#', int(time_key) + 24, file=write_file, end='', sep='')
            for name in QUERY_NAME:
                print(',', int(
                    round(value_dict[key][time_key][name])), file=write_file, end='', sep='')
            print('', file=write_file, end='\n')

    write_file.close()
