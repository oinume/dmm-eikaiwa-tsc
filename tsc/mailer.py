# coding: utf-8

import sendgrid
import xml.sax.saxutils
from typing import List


class Mailer:

    def __init__(self, sendgrid_username: str, sendgrid_password: str=None):
        self.client = sendgrid.SendGridClient(sendgrid_username, sendgrid_password)

    def send(self, from_address: str, to_address: str, subject: str, body: str):
        mail = sendgrid.Mail()
        mail.set_from(from_address)
        mail.add_to(to_address)
        mail.set_subject(subject)
        body_text = xml.sax.saxutils.escape(body)
        mail.set_html(body_text.replace("\n", "<br>"))
        self.client.send(mail)

    def send_multi(self, from_address: str, to_addresses: List[str], subject: str, body: str):
        for to in to_addresses:
            self.send(from_address, to, subject, body)
