import uuid

from django.conf import settings
from django.core.mail import send_mail, send_mass_mail


# TODO: Use send_mass_mail()
# TODO: Use HTML template

def generate_activation_key():
    return uuid.uuid4().hex


def send_email(subject, message, user):
    msg = 'Hello, {full_name}!\n\n{message}\n\n ~ The ELSYSER Team ~'.format(
        full_name=user.get_full_name(),
        message=message
    )

    send_mail(
        subject=subject,
        message=msg,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )


def send_verification_email(user):
    subject = 'ELSYSER Account activation'
    client_url = 'http://elsyser.netlify.com/#/auth/activate/{activation_key}/'.format(
        activation_key=user.student.activation_key
    )
    message = 'Visit this link to activate your ELSYSER account: {url}'.format(url=client_url)

    send_email(subject, message, user)


def send_creation_email(user, model):
    model_name = model.__class__.__name__
    subject = 'ELSYSER - {model_name} for you was created'.format(model_name=model_name)
    message = '{model_name} for you was added just now:\n{model}'.format(
        model_name=model_name, model=model
    )

    send_email(subject, message, user)
