# coding: utf-8

# pip install bs4


import requests
from bs4 import BeautifulSoup
import codecs
import os
import pickle
import datetime
import time
import re

class WorkTask:
    def __init__(self, current_time, content):
        host='https://coconala.com'
        host_request='https://coconala.com/requests/'
        self.updated = current_time
        self.category = content.find('div', class_='c-itemInfo_category').a.text.strip()
        self.title = content.find('div', class_='c-itemInfo_title').a.text.strip()
        self.id = content.find('div', class_='c-itemInfo_title').a['href'][len(host_request):]
        self.title_link = content.find('div', class_='c-itemInfo_title').a['href']
        self.description = content.find('div', class_='c-itemInfo_description').text.strip()
        self.user_link = host + content.find('div', class_='c-itemInfoUser_name').a['href'].strip()
        self.user_name = content.find('div', class_='c-itemInfoUser_name').text.strip()
        self.timestamp = content.find('div', class_='c-itemInfoUser_created').find_all('span')[1]['title'].strip()
        self.timestamp_before = content.find('div', class_='c-itemInfoUser_created').find_all('span')[1].text.strip()
        self.proposal_count = content.find('span', class_='c-itemTileLine_emphasis-proposalCount').text.strip()
        budgets = content.find_all('span', class_='c-itemTileLine_emphasis-budget')
        if len(budgets) == 1:
            self.budget = None
        else:
            self.budget = [WorkTask.budget_to_int(s.text.strip()) for s in budgets]
        if content.find('span', class_='c-itemTileLine_emphasis-remainingDays') is None:
            self.remainin_days = None
        else:
            self.remainin_days = content.find('span', class_='c-itemTileLine_emphasis-remainingDays').text.strip()
    
    def __str__(self):
        ret = ''
        ret += 'id: {}\n'.format(self.id)
        ret += 'category: {}\n'.format(self.category)
        ret += 'title: {}\n'.format(self.title)
        ret += 'title_link: {}\n'.format(self.title_link)
        ret += 'user_link: {}\n'.format(self.user_link)
        ret += 'user_name: {}\n'.format(self.user_name)
        ret += 'timestamp: {}\n'.format(self.timestamp)
        ret += 'timestamp_before: {}\n'.format(self.timestamp_before)
        ret += 'proposal_count: {}\n'.format(self.proposal_count)
        ret += 'budget: {}\n'.format(self.budget)
        ret += 'remainin_days: {}\n'.format(self.remainin_days)
        ret += 'description: {}\n'.format(self.description.replace('\n', ''))
        return ret

    @classmethod
    def line_title(cls):
        return 'id\tcategory\ttitle\ttitle_link\tuser_link\tuser_name\ttimestamp\tago\tproposal_count\tbudget(min)\tbudget(max)\tbudget(expected)\tremaining_days\tdescription\n'
    
    @classmethod
    def budget_to_int(cls, budget):
        s = budget.replace(',', '').replace('万', '0000')
        return int(s)


    def line(self):
        ret = ''
        ret += '{}\t'.format(self.id)
        ret += '{}\t'.format(self.category)
        ret += '{}\t'.format(self.title)
        ret += '{}\t'.format(self.title_link)
        ret += '{}\t'.format(self.user_link)
        ret += '{}\t'.format(self.user_name)
        ret += '{}\t'.format(self.timestamp)
        ret += '{}\t'.format(self.timestamp_before)
        ret += '{}\t'.format(self.proposal_count)
        if(self.budget is None):
            ret += '{}\t{}\t{}\t'.format('Quote','Quote','Quote')
        else:
            ret += '{}\t{}\t{}\t'.format(min(self.budget), max(self.budget), sum(self.budget) / len(self.budget))
        if self.remainin_days is None:
            ret += '{}\t'.format('Closed')
        else:
            ret += '{}\t'.format(self.remainin_days)
        ret += '{}\n'.format(self.description.replace('\n', ''))
        return ret

class Coconara:
    def __init__(self):
        pass

    def max_page(self):
        url = 'https://coconala.com/requests'
        # 403 エラーが出ないようにヘッダを設定しておく
        # https://stackoverflow.com/questions/16627227/problem-http-error-403-in-python-3-web-scraping
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        return max([int(s) for s in re.findall(r'/requests\?page=(\d+)', response.text)])

    def get_page(self, page):
        url = 'https://coconala.com/requests?page={}'.format(page)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        return response.content

    def get_works(self, page):
        content = self.get_page(page)
        current_time = datetime.datetime.now()
        soup = BeautifulSoup(content, "html.parser")
        return [WorkTask(current_time, s) for s in soup.find_all('div', class_='c-searchItem')]
    
    def scan_all_pages(self):
        max_page = self.max_page()
        closed_count_repeatly = 0
        closed_count_repeatly_upper = 100
        for page in range(0, max_page):
            print('loading page {} / {}...'.format(page, max_page))
            works = self.get_works(page)
            for work in works:
                if work.remainin_days is None:
                    closed_count_repeatly += 1
                else:
                    closed_count_repeatly = 0
                if closed_count_repeatly >= closed_count_repeatly_upper:
                    return
                path, dir = self.get_path(work)
                if not os.path.exists(path):
                    closed_count_repeatly = 0
                self.write_work(work)
            time.sleep(3)


    def scan_page(self, page):
        works = self.get_works(page)
        for work in works:
            self.write_work(work)
    
    def get_path(self, work):
        id = int(work.id)
        dir0 = int(id / 1000000)
        dir1 = int(id / 10000)
        dir2 = int(id / 100)
        dir = 'datas/{}/{}/{}'.format(dir0, dir1, dir2)
        path = '{}/{}.pickle'.format(dir, id)
        return path, dir


    def write_work(self, work):
        path, dir = self.get_path(work)
        os.makedirs(dir, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(work, f)

    

if __name__ == '__main__':
    while True:
        coconara = Coconara()
        coconara.scan_all_pages()
        works = coconara.get_works(0)
        with codecs.open('list.csv', 'w', 'utf-8') as f:
            f.write(WorkTask.line_title())
            for work in works:
                f.write(work.line())
        print('Coconara downloader is sleeping.')
        time.sleep(3600) # 1時間ほど適当に休む



