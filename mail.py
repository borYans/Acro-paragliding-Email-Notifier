import smtplib
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')
sent_from = config['MAIL_CREDENTIALS']['my_email']
login_pass = config['PASS_CREDENTIALS']['my_pass']


def send_mail(mail):
    for mail_address in mail.to:
        print("Mail successfully sent.\n\n")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # this will make the connection secure
            connection.login(user="boryans.yans@gmail.com", password="dicxsgwzqxrfyaay")
            connection.sendmail(
                from_addr=sent_from,
                to_addrs=mail_address,
                msg=f"Subject: {mail.subject}\n\n{mail.body}"
            )
        time.sleep(1)
