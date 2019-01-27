# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/27 
from django import forms
from django.core.exceptions import ValidationError

from rbac.forms.base_form import BaseForm
from rbac import models


class UserForm(BaseForm):
    re_pwd = forms.CharField(label="确认密码")

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 're_pwd', 'email']
        widgets = {
            "password": forms.PasswordInput(),
            "re_pwd": forms.PasswordInput()
        }

    def clean_re_pwd(self):
        req_pwd = self.cleaned_data.get("password")
        req_re_pwd = self.cleaned_data.get("re_pwd")
        if req_pwd != req_re_pwd:
            raise ValidationError("两次密码不一致")
        return req_re_pwd
