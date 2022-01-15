# coding: utf-8

import requests
import time
import codecs
import os
import datetime
import pickupper
import sys

# set PATH=%PATH%;F:\Anaconda3\Library\bin

max_loaded_id_path = 'max_loaded_id.txt'
max_loaded_id = 0

if os.path.exists(max_loaded_id_path):
    max_loaded_id = int(open(max_loaded_id_path, 'r').read())

id_min = 100
id_max = 1800000
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        id_min = int(sys.argv[1])
        if id_min < 0:
            id_min = max_loaded_id
    if len(sys.argv) >= 3:
        id_max = int(sys.argv[2])
    while True:
        for id in range(id_min, id_max+1, 10):
            group10000 = (int)(id / 100000)
            group100 = (int)(id / 1000)
            dir = 'html/{}/{}'.format(group10000, group100)
            path = '{}/{}.html'.format(dir, id)

            pi = pickupper.ProductInfo(id, path)
            if (pi.status == 'invalid' or pi.status == 'error') and id < max_loaded_id:
                print('id={}, status={}'.format(id, pi.status))
                continue

            url = 'https://store.steampowered.com/app/{}/'.format(id)
            try:
                response = requests.get(url)
            except: 
                with codecs.open('{}/{}.html'.format(dir, id), 'w', 'utf-8') as f:
                    f.write(url + '\n')
                    f.write('[[error]]')
                continue
            res = 'id={}, code={}'.format(id, response.status_code)
            print(res)    # HTTPのステータスコード取得
            os.makedirs(dir, exist_ok=True)
            with codecs.open(path, 'w', 'utf-8') as f:
                f.write(str(datetime.datetime.now()) + '\n')
                f.write(url + '\n')
                f.write(res + '\n')
                if url in response.text:
                    f.write(response.text)
                    if id > max_loaded_id:
                        max_loaded_id = id
                        with open(max_loaded_id_path, 'w') as fm:
                            fm.write('{}\n'.format(max_loaded_id))
                else:
                    f.write('[[invalid]]')
            time.sleep(3)
        id_min = 100

