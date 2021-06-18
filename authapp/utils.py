from django.core.mail import EmailMessage


class Helper:
    @staticmethod
    def send_account_verification_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['email']]
        )
        email.send()
