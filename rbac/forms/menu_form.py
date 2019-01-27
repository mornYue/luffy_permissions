# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/28 
from rbac.forms import base_form
from rbac import models


class MenuForm(base_form.BaseForm):
    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
