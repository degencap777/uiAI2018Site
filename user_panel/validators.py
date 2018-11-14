import re
from django.core.exceptions import ValidationError


def team_name_validator(value):
    if re.match(r'^[A-Za-z0-9 _-]+$', value) is None:
        raise ValidationError('نام تیم فقط باید شامل حروف انگلیسی، اعداد، فاصله و یا کاراکترهای - و ـ باشد.')


def english_string_validator(value):
    if re.match(r'^[A-Za-z ]+$', value) is None:
        raise ValidationError('ورودی باید به انگلیسی باشد.')


def phone_number_validator(value):
    if re.match(r'^09\d{9}$', value) is None:
        raise ValidationError('شماره تلفن نامعتبر است.')


def persian_name_validator(value):
    spaces = '[\u0020\u2000-\u200F\u2028-\u202F]'
    persian_alphabet = '[\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651' \
                       '\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC]'
    arabic_letters = '[\u0629\u0643\u0649-\u064B\u064D\u06D5]'
    regex = r'|'.join([spaces, persian_alphabet, arabic_letters])
    if re.match(r'^({})+$'.format(regex), value) is None:
        raise ValidationError('نام وارد شده فارسی نیست.')
