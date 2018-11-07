from django import forms

from captcha import fields as captcha_fields


class CommentForm(forms.Form):
    text = forms.CharField(
        label='متن نظر',
        help_text='حداکثر ۱۰۲۴ کاراکتر',
        widget=forms.Textarea,
    )
    captcha = captcha_fields.CaptchaField(
        label='حروف تصویر:',
    )
