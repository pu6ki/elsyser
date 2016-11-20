from django.core.exceptions import ValidationError

from datetime import datetime


def validate_date(date):
    if date < datetime.now().date():
        raise ValidationError('Only future dates allowed.')
    if date.weekday() not in range(0, 5):
        raise ValidationError('Weekend days are not valid.')
