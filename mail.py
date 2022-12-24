import smtplib

my_email = "boryans.yans@gmail.com"
my_pass = "dicxsgwzqxrfyaay"


def send_mail(mail_subject, mail_content):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # this will make the connection secure
        connection.login(user=my_email, password=my_pass)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="janevskiboris9@gmail.com",
            msg=f"Subject: {mail_subject}\n\n{mail_content}"
        )
