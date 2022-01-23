# coding: utf-8

import glob
import pickle

from work import Work
from notifier import Notifier
from user import User
from user_manager import UserManager

class Analyzer:
    def __init__(self):
        pass

    def scan(self, closed = False):
        files = glob.glob('datas/**/*.pickle', recursive=True)
        print('Number of Coconara proposal: {}'.format(len(files)))
        ret = []
        count = 0
        for file in files:
            print('{}/{}'.format(count, len(files)), end='\r')
            count += 1
            with open(file, 'rb') as f:
                proposal = pickle.load(f)
                if not closed or proposal.remainin_days is not None:
                    ret.append(proposal)
        return ret

    def match(self, proposal, keywords):
        for keyword in keywords:
            keyword = keyword.lower()
            description = proposal.description.lower()
            title = proposal.title.lower()
            if not(keyword in description or keyword in title):
                return False
        return True



if __name__=='__main__':
    analyzer = Analyzer()
    user_manager = UserManager()
    targets = analyzer.scan(False)
    active_works = [Work(t.title, t.title_link, t.description, t.user_link, user_manager) for t in targets 
        if analyzer.match(t, ['Unity'])]
    notifier = Notifier()
    notifier.notify(active_works)
