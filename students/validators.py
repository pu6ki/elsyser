from django.core.exceptions import ValidationError

from datetime import datetime
import os


def validate_date(date):
    if date < datetime.now().date():
        raise ValidationError('Only future dates allowed.')
    if date.weekday() not in range(0, 5):
        raise ValidationError('Weekend days are not valid.')


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.zip', '.rar']

    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'Allowed file extensions are: {}'.format(','.join(valid_extensions))
        )
