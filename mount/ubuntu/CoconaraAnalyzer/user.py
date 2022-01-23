# coding: utf-8

import requests
from bs4 import BeautifulSoup
import codecs
import sys
import time

class User:
    def __init__(self, url):
        print(url)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        content = BeautifulSoup(response.content, "html.parser")
        time.sleep(3)
        info = content.find_all('li', class_='c-dataValue_item')
        sex = content.find('span', class_='c-userProfile_text -sex')
        if sex is None:
            self.sex = '-'
        else:
            self.sex = sex.text.strip()
        self.progress = info[0].find('span', class_='c-dataValue_value').text.strip()
        self.eval = info[1].find('span', class_='c-dataValue_value').text.strip()
        self.follower = info[2].find('span', class_='c-dataValue_value').text.strip()
        auth = content.find_all('li', class_='c-dataValue_item -authentication')
        self.identification = not (auth[0].find('i', class_='coconala-icon -check') is None)
        self.nda = not (auth[1].find('i', class_='coconala-icon -check') is None)
        
    
    def __str__(self):
        ret = ''
        ret += 'sex: {}\n'.format(self.sex)
        ret += 'progress: {}\n'.format(self.progress)
        ret += 'eval: {}\n'.format(self.eval)
        ret += 'follower: {}\n'.format(self.follower)
        ret += 'identification: {}\n'.format(self.identification)
        ret += 'nda: {}\n'.format(self.nda)
        return ret
    
    def email_info(self):
        ret = '<table border="1">\n'
        ret += '<tr><td>性別</td><td>販売数</td><td>評価</td><td>フォロワー</td><td>本人確認</td><td>NDA</td></tr>\n'
        ret += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(self.sex, self.progress, self.eval, self.follower, self.identification, self.nda)
        ret += '</table>\n'
        return ret
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: .py url')
        exit()
    url = sys.argv[1]
    user = User(url)
    print(user)
    print(user.email_info())


