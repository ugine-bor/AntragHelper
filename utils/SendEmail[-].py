import smtplib
import ssl
from email.message import EmailMessage

from data.config import mail_login, mail_app_pass
from load import __


def mailsender(mail, filepath):
    me = mail_login
    passwd = mail_app_pass
    server = "smtp.gmail.com"
    port = 465 #587

    subject = __("Ваши заполненные документы")

    to = mail

    text = __("Архив с заполненными документами, который вы запросили в телеграм боте")

    # тело
    msg = EmailMessage()
    msg['From'] = me
    msg['To'] = to
    msg['Subject'] = subject

    msg.set_content(text)

    with open(filepath, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='zip', filename='Filled_Docs.zip')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(server, port, context=context) as smtp:
        smtp.login(me, passwd)
        smtp.send_message(msg)
