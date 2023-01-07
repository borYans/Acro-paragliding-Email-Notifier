import configparser
from dataclasses import dataclass
import mail


@dataclass
class Mail:
    to: list
    subject: str
    body: str


def get_mails_from_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    emails = config['EMAILS']['e_mails'].split(',')
    return emails


def get_mail_content(wind, date, wind_gust):
    return f"Zdravo letaciste, imas letacki den na {date}!\n" \
           f"Veter na start: {wind}m/s so udari {wind_gust}m/s.\n" \
           f"Mailov se isprakja sekojpat koga parametrite " \
           f"se zadovoleni za odredenata lokacija.\nNapolni instrumenti, " \
           f"spremi kamera i stavi eden par rakavici vo opremata.\n" \
           f"Se gledame na start!\n\n" \
           f"Pozdrav,\n" \
           f"Acromacedonia"


class MailFactory:
    @staticmethod
    def send_mail(mail_type, wind, wind_gust, date):
        if mail_type == 'Vodno':
            e_mail = Mail(
                to=get_mails_from_config(),
                subject="Letacki den na VODNO",
                body=get_mail_content(wind, date, wind_gust)
            )
            mail.send_mail(e_mail)
        elif mail_type == 'Osoj':
            e_mail = Mail(
                to=get_mails_from_config(),
                subject="Letacki den na OSOJ",
                body=get_mail_content(wind, date, wind_gust)
            )
            mail.send_mail(e_mail)
