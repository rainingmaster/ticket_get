#import httplib2, json, urllib, time
#reference:https://www.shiyanlou.com/courses/623/labs/2072/document
"""Train tickets query via command-line.

Usage:
    get [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    get beijing shanghai 2016-08-25
"""

import requests, json
import winsound
from stations import stations
from docopt import docopt

def parse(data):
    for row in data:
        if row['zy_num'].isnumeric() and int(row['zy_num']) > 10:
            print("SUCCESS!")
            print("-".join([row['station_train_code'], row['from_station_name'], row['to_station_name']]))
            winsound.Beep(32767, 9999999)
            return True
    print("FAILED!")
    return False

def main():
    args = docopt(__doc__)
    from_station = stations.get(args['<from>'])
    to_station = stations.get(args['<to>'])
    date = args['<date>']
    
    if from_station == None:
        print("From Station is wrong")
        exit()
    
    if to_station == None:
        print("To Station is wrong")
        exit()
    
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station
    )
    ret = False
    
    while not ret:
        r = requests.get(url, verify = False)
        if r.status_code != 200:
            print("return status is " + str(r.status_code))
            continue
            
        rows = r.json()["data"]["datas"]
        ret = parse(rows)
        
 
if __name__ == '__main__':
   main()