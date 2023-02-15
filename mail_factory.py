import configparser
import datetime
from dataclasses import dataclass

import converter
import mail


@dataclass
class Mail:
    to: list
    subject: str
    body: str


@dataclass
class MailDataModel:
    site: str
    date: datetime
    wind_direction: int
    wind_speed: int
    wind_gust: int


def get_mails_from_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    emails = config['EMAILS']['e_mails'].split(',')
    return emails


def get_mail_content(mail_model):
    return f"Zdravo letaciste, imas letacki den na {mail_model.date}\n" \
           f"Veter na start: {mail_model.wind_speed}m/s so udari {mail_model.wind_gust}m/s.\n" \
           f"Pravec na veter: {mail_model.wind_direction} degrees\n" \
           f"Ova e avtomatski mail koj se isprakja sekojpat koga parametrite " \
           f"se zadovoleni za odredenata lokacija.\nNapolni instrumenti, " \
           f"spremi kamera i stavi eden par rakavici vo opremata.\n" \
           f"Se gledame na start!\n\n" \
           f"Pozdrav,\n" \
           f"Acromacedonia"


class MailFactory:
    @staticmethod
    def prepare_and_send_mail(mail_data_model):
        if mail_data_model.site == 'Vodno':
            e_mail = MailFactory.create_mail(mail_data_model, "Letacki den na Vodno")
            print(e_mail.body)
            mail.send_mail(e_mail)
        elif mail_data_model.site == 'Osoj':
            e_mail = MailFactory.create_mail(mail_data_model, "Letacki den na Osoj")
            print(e_mail.body)
            mail.send_mail(e_mail)
        elif mail_data_model.site == 'Ajvatovci':
            e_mail = MailFactory.create_mail(mail_data_model, "Letacki den na Ajvatovci")
            print(e_mail.body)
            mail.send_mail(e_mail)

        elif mail_data_model.site == 'Skopska Crna Gora':
            e_mail = MailFactory.create_mail(mail_data_model, "Letacki den na Skopska C.G")
            print(e_mail.body)
            mail.send_mail(e_mail)

    @staticmethod
    def create_mail(mail_data_model, subject):
        if mail_data_model.wind_speed > 3:
            return Mail(
                to=get_mails_from_config(),
                subject=f"{subject} - Edrenje",
                body=get_mail_content(mail_data_model)
            )
        else:
            return Mail(
                to=get_mails_from_config(),
                subject=f"{subject} - Spust/Termika",
                body=get_mail_content(mail_data_model)
            )
