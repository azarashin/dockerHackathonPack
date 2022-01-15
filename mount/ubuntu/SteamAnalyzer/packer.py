# coding: utf-8

import glob
import pickupper
import re
import pickle
import sys

path = './steam.pickle'

if __name__ == '__main__':
    datas = {}
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        with open(path, 'rb') as f:
            datas = pickle.load(f)
    files = glob.glob("./html/**/**/*.html")
    m = re.compile(r'./html/.+?/.+?/(.+?)\.html', flags=re.DOTALL)
    cnt = 0
    max_id = max([d for d in datas if datas[d].status == 'active' or datas[d].status == 'closed'])
    for file in files:
        id = m.search(file.replace('\\', '/')).group(1)
        print('\r', id, end='')
        if not id in datas or id > max_id:
            datas[id] = pickupper.ProductInfo(id, file)
            cnt += 1
            if cnt > 1000:
                cnt = 0
                print(' -- saved: {}\n'.format(path))
                with open(path, 'wb') as f:
                    pickle.dump(datas, f)


    with open(path, 'wb') as f:
        pickle.dump(datas, f)
