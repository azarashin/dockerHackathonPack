# coding: utf-8

import glob
import pickupper
import re
import pickle

files = glob.glob("./html/**/**/*.html")
m = re.compile(r'./html/.+?/.+?/(.+?)\.html', flags=re.DOTALL)
datas = []
for file in files:
    id = m.search(file.replace('\\', '/')).group(1)
    print('\r', id, end='')
    datas.append(pickupper.ProductInfo(id, file))

with open('./steam.pickle', 'wb') as f:
    pickle.dump(datas, f)