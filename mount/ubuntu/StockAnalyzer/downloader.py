# coding: utf-8

import requests
import time
import codecs
import os
import datetime
import sys

# set PATH=%PATH%;F:\Anaconda3\Library\bin

id_min = 1300
id_max = 9999
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        id_min = int(sys.argv[1])
    while True:
        for id in range(id_min, id_max+1, 1):
            group100 = (int)(id / 100)
            dir = 'html/{}'.format(group100)
            path = '{}/{}.html'.format(dir, id)

            url = 'https://minkabu.jp/stock/{}'.format(id)
            try:
                response = requests.get(url)
            except: 
                with codecs.open('{}/{}.html'.format(dir, id), 'w', 'utf-8') as f:
                    f.write(url + '\n')
                    f.write('[[error]]')
                continue
            res = 'id={}, code={}'.format(id, response.status_code)
            print(res)    # HTTPのステータスコード取得
            if response.status_code != 404:
                os.makedirs(dir, exist_ok=True)
                with codecs.open(path, 'w', 'utf-8') as f:
                    f.write(str(datetime.datetime.now()) + '\n')
                    f.write(url + '\n')
                    f.write(res + '\n')
                    if url in response.text:
                        f.write(response.text)
                    else:
                        f.write('[[invalid]]')
            time.sleep(1)
        id_min = 100

