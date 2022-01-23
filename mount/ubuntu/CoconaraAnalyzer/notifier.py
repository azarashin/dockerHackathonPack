# coding: utf-8

from email.mime.text import MIMEText
import smtplib
import json

from work import Work

class Notifier:
    def __init__(self):
        env=json.loads(open(".env").read())

        # SMTP認証情報
        self.account = env["account"]
        self.password = env["password"]
        
        # 送受信先
        self.to_email = ';'.join(env["email_to"])
        self.from_email = env["email_from"]

    def notify(self, works):
        print('active works: {}\n'.format(len(works)))
        show_max = 10

        # MIMEの作成
        subject = "新しい仕事が見つかりました"
        message = '\n\n'.join([str(s) for s in works[:show_max]])
        msg = MIMEText(message, "html")
        msg["Subject"] = subject
        msg["To"] = self.to_email
        msg["From"] = self.from_email
        
        # メール送信処理
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.account, self.password)
        server.send_message(msg)
        server.quit()

if __name__ == '__main__':
    works = [
        Work('workA', 'https://urlA.com', 'detailA'), 
        Work('workB', 'https://urlB.com', 'detailB')
    ]

    n = Notifier()
    n.notify(works)
