# coding: utf-8

from user import User

class UserManager:
    def __init__(self):
        self.dic = {}

    def get(self, url):
        if not url in self.dic:
            self.dic[url] = User(url)
        return self.dic[url]
