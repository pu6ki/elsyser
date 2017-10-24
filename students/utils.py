import uuid

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


BASE_CLIENT_URL = 'http://elsyser.netlify.com/#/'

def generate_activation_key():
    return uuid.uuid4().hex


def send_verification_email(user):
    subject = 'ELSYSER Account activation'
    client_url = BASE_CLIENT_URL + 'auth/activate/{activation_key}/'.format(
        activation_key=user.student.activation_key
    )
    message = 'Visit this link to activate your ELSYSER account: {url}'.format(url=client_url)

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


def send_creation_email(user, model):
    model_type = model.__class__.__name__.lower()
    client_resource_link = '{model_type}s/{id}/'.format(model_type=model_type, id=model.id)

    template_context = {
        'full_name': user.get_full_name(),
        'type': model_type,
        'model': model,
        'author': model.author,
        'link': BASE_CLIENT_URL + client_resource_link
    }
    html_content = render_to_string('utils/email.html', context=template_context)
    text_content = strip_tags(html_content)

    subject = 'ELSYSER {resource} added'.format(resource=model_type)

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
