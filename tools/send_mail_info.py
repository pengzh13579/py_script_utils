# Author pengzihao
# Date 2019/1/9
import configparser
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 生成config对象用于读取db.conf文件
conf = configparser.ConfigParser()
# 读取文件
conf.read('../conf/send_mail_conf.conf')
# 获得邮件相关配置
mail_host = conf.get('email', 'mail_host')
mail_port = conf.getint('email', 'mail_port')
# 邮箱的授权码
mail_user = conf.get('email', 'mail_user')
mail_pass = conf.get('email', 'mail_pass')
mail_nickname = conf.get('email', 'mail_nickname')
mail_sender = conf.get('email', 'mail_sender')


# 发送邮件
def send_email_info(text, subject, receiver):
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header( mail_sender, 'utf-8') # 对应发件人邮箱昵称、发件人邮箱账号
    message['To'] = Header(receiver) # 对应收件人邮箱昵称、收件人邮箱账号

    message['Subject'] = Header(subject, 'utf-8') # 邮件的主题

    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtp_obj.login(mail_user, mail_pass)
        smtp_obj.sendmail(mail_sender, [receiver,], message.as_string())
        smtp_obj.quit()
        print(u"邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


if __name__ == "__main__":
    send_email_info('python发送邮件', '使用python发送邮件的内容', "1794822268@qq.com")