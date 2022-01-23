# coding: utf-8

class Work:
    def __init__(self, title, url, detail, user_link, user_manager):
        self.title = title
        self.url = url
        self.detail = detail
        self.user_link = user_link
        self.user_manager = user_manager
    
    def __str__(self):
        user = self.user_manager.get(self.user_link)
        return '<h2><a href="{}">{}</h2><div>{}</div><p>{}</p>'.format(self.url, self.title, user.email_info(), self.detail[:256])
