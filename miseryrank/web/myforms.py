import re
from django import forms

from django.core.exceptions import ValidationError


# 手机号格式验证
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')  #自定义验证规则的时候，如果不符合你的规则，需要自己发起错误


# 注册功能相关验证
class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=6,
        label='用户名',
        widget=forms.widgets.TextInput(attrs={'class':'username','autocomplete':'off','placeholder': '用户名'}),
        error_messages={
            'required':'用户名不能为空',
            'max_length':'用户名不能大于16位',
            'min_length':'用户名不能小于6位',
        }

    )
    #placeholder="输入密码" oncontextmenu="return false"
             #onpaste="return false"
    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder': '输入密码', 'oncontextmenu': 'return false', 'onpaste': 'return false'}),

        error_messages={
            'required': '密码不能为空',
            'max_length': '密码不能大于32位',
            'min_length': '密码不能小于6位',
        }
    )
    r_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder': '请再次输入密码', 'oncontextmenu': 'return false', 'onpaste': 'return false'}),
        error_messages={
            'required': '确认密码不能为空',
        }
    )
    telephone = forms.CharField(
        label='手机号',
        error_messages={
            'required': '手机不能为空',
        },
        validators=[mobile_validate, ],
        widget=forms.widgets.TextInput(
            attrs={'class': 'phone_number', 'placeholder': '输入手机号码', 'autocomplete': 'off', 'id': 'number'}),
    )

    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'required': '邮箱不能为空',
            'invalid':'邮箱格式不对',
        },
        widget=forms.widgets.TextInput(attrs={'class': 'email', 'placeholder': '输入邮箱地址', 'oncontextmenu': 'return false', 'type': 'email'}),
        # validators=[]
    )

    def clean(self):
        values = self.cleaned_data
        password = values.get('password')
        r_password = values.get('r_password')

        if password == r_password:
            return values
        else:
            self.add_error('r_password','两次输入的密码不一致！')
