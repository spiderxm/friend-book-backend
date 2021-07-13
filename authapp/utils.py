import sendgrid
import os
from sendgrid.helpers.mail import *


class Helper:
    @staticmethod
    def send_account_verification_email(data):
        try:
            sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("API_KEY"))
            from_email = Email(os.environ.get('EMAIL_ID'))
            to_email = To(data['email'])
            subject = data['email_subject']
            content = Content("text/plain", data['email_body'])
            mail = Mail(from_email, to_email, subject, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response)
        except Exception as e:
            print(e)
