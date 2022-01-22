from email.mime.text import MIMEText
import smtplib
import json

class Work:
    def __init__(self, title, url, detail):
        self.title = title
        self.url = url
        self.detail = detail
    
    def __str__(self):
        return '<h2><a href="{}">{}</h2><a>{}</a>'.format(self.url, self.title, self.detail)

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

        # MIMEの作成
        subject = "新しい仕事が見つかりました"
        message = '\n\n'.join([str(s) for s in works])
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
