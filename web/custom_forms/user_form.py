from django.forms.models import ModelForm

from rbac import models


class UserForm(ModelForm):
    """
    自定义用户登录Form组件
    """
    class Meta:
        model = models.UserInfo
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field, value in self.fields.items():
            value.widget.attrs['class'] = "form-control"
            value.widget.attrs['placeholder'] = value.label
