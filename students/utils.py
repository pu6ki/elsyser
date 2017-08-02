from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(user):
    client_url = 'http://elsyser.aerobatic.io/activate/{id}/{activation_key}/'.format(
        id=user.id,
        activation_key=user.student.activation_key
    )

    message = '''Hello, {full_name}!
Visit this link to activate your account: {url}
    '''.format(full_name=user.get_full_name(), url=client_url)

    send_mail(
        subject='ELSYSER Account verification',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
