# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/26 
from django.forms import ModelForm


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for name, value in self.fields.items():
            value.widget.attrs["class"] = "form-control"
            value.widget.attrs["placeholder"] = value.label