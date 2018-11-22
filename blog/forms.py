from django import forms

from captcha import fields as captcha_fields


class CommentForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی'}),
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'ایمیل'}),
    )
    text = forms.CharField(
        label='متن نظر',
        help_text='حداکثر ۱۰۲۴ کاراکتر',
        widget=forms.Textarea(attrs={'placeholder': 'متن نظر'}),
    )
    captcha = captcha_fields.CaptchaField(
        label='حروف تصویر:',
    )
