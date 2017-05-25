from datetime import datetime

from django.core.exceptions import ValidationError


def validate_date(date):
    if date < datetime.now().date():
        raise ValidationError('Only future dates allowed.')
    if date.weekday() not in range(0, 5):
        raise ValidationError('Weekend days are not valid.')
