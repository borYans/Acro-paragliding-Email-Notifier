import smtplib
import time

my_email = "boryans.yans@gmail.com"
my_pass = "dicxsgwzqxrfyaay"
e_mails = [
    "janevskiboris9@gmail.com",
    "kajeskaivana@gmail.com"
    "antoniolukovski701@gmail.com",
    "nikola.eftovski@gmail.com",
    "usamedin.nuhiji@gmail.com",
    "dartanjan15@gmail.com",
    "acromacedonia@gmail.com"
]


def send_mail(mail_subject, mail_content):
    for mail_address in e_mails:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # this will make the connection secure
            connection.login(user=my_email, password=my_pass)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=mail_address,
                msg=f"Subject: {mail_subject}\n\n{mail_content}"
            )
            time.sleep(1)
