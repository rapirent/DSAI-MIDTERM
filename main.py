import csv
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--day', default='1')
parser.add_argument('--month', default='1')
args = parser.parse_args()

if args.day == '1' or args.day == '2':
    DURATION_1 = '2018-' + str(int(args.month) - 1).zfill(2) + '-1-0/2018-' + args.month.zfill(2) + '-1-0'
    DURATION_2 = '2018-' + str(int(args.month) - 1).zfill(2) + '-1-0/2018-' + args.month.zfill(2) + '-1-0'
else:
    DURATION_1 = '2018-' + str(int(args.month) - 1).zfill(2) + '-' + str(int(args.day) - 2) + '-0/2018-' + args.month.zfill(2) + '-' + str(int(args.day) - 1) + '-0'
    DURATION_2 = '2018-' + str(int(args.month) - 1).zfill(2) + '-' + str(int(args.day) - 1) + '-0/2018-' + args.month.zfill(2) + '-' + args.day + '-0'

print('1', DURATION_1)
print('2', DURATION_2)

BJ_URL_1 = 'https://biendata.com/competition/airquality/bj/' + DURATION_1 +'/2k0d1d8'
LD_URL_1 = 'https://biendata.com/competition/airquality/ld/' + DURATION_1 + '/2k0d1d8'
BJ_URL_2 = 'https://biendata.com/competition/airquality/bj/' + DURATION_2 + '/2k0d1d8'
LD_URL_2 = 'https://biendata.com/competition/airquality/ld/' + DURATION_2 + '/2k0d1d8'
ID_LIST = ['dongsi_aq', 'tiantan_aq', 'guanyuan_aq', 'wanshouxigong_aq', 'aotizhongxin_aq', 'nongzhanguan_aq', 'wanliu_aq', 'beibuxinqu_aq', 'zhiwuyuan_aq', 'fengtaihuayuan_aq', 'yungang_aq', 'gucheng_aq', 'fangshan_aq', 'daxing_aq', 'yizhuang_aq', 'tongzhou_aq', 'shunyi_aq', 'pingchang_aq', 'mentougou_aq', 'pinggu_aq',
           'huairou_aq', 'miyun_aq', 'yanqin_aq', 'dingling_aq', 'badaling_aq', 'miyunshuiku_aq', 'donggaocun_aq', 'yongledian_aq', 'yufa_aq', 'liulihe_aq', 'qianmen_aq', 'yongdingmennei_aq', 'xizhimenbei_aq', 'nansanhuan_aq', 'dongsihuan_aq', 'CD1', 'BL0', 'GR4', 'MY7', 'HV1', 'GN3', 'GR9', 'LW2', 'GN0', 'KF1', 'CD9', 'ST5', 'TH4']
OUTPUT_FILE_NAME = args.month + "-" + args.day + '.csv'

QUERY_NAME = ['PM25_Concentration', 'PM10_Concentration', 'O3_Concentration']

def crawler(url, value, count):
    a = requests.get(url)

    decoded_content = a.content.decode('utf-8')
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')

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

    value_dict, count_dict = crawler(BJ_URL_1, value_dict, count_dict)
    value_dict, count_dict = crawler(LD_URL_1, value_dict, count_dict)

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

    value_dict = {name:
                    {str(num).zfill(2): {'PM10_Concentration': 0, 'PM25_Concentration': 0,
                                        'O3_Concentration': 0} for num in range(0, 24)}
                    for name in ID_LIST}

    count_dict = {name:
                  {str(num).zfill(2): {'PM10_Concentration': 0, 'PM25_Concentration': 0,
                                       'O3_Concentration': 0} for num in range(0, 24)}
                  for name in ID_LIST}

    value_dict, count_dict = crawler(BJ_URL_2, value_dict, count_dict)
    value_dict, count_dict = crawler(LD_URL_2, value_dict, count_dict)

    for key, value in value_dict.items():
        for time_key, time_value in value.items():
            for element_key in time_value.keys():
                if count_dict[key][time_key][element_key]:
                    value_dict[key][time_key][element_key] /= count_dict[key][time_key][element_key]

    for key, value in value_dict.items():
        for time_key, time_value in value.items():
            print(key, file=write_file, end='')
            print('#', int(time_key) + 24, file=write_file, end='', sep='')
            for name in QUERY_NAME:
                print(',', int(
                    round(value_dict[key][time_key][name])), file=write_file, end='', sep='')
            print('', file=write_file, end='\n')

    write_file.close()
