import re
from django.core.exceptions import ValidationError


def team_name_validator(value):
    if re.match(r'^[A-Za-z0-9_]+$', value) is None:
        raise ValidationError('نام تیم نامعتبر است.')


def english_string_validator(value):
    if re.match(r'^[A-Za-z ]+$', value) is None:
        raise ValidationError('ورودی باید به انگلیسی باشد.')
