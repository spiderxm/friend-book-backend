from django.core.mail import send_mail
from django.conf import settings

class Helper:
    @staticmethod
    def send_account_verification_email(data):
        try:
            send_mail(
                data['email_subject'],
                data['email_body'],
                settings.EMAIL_HOST_USER,
                [data['email']],
                fail_silently=False,
            )
        except Exception as e:
            print(e)
