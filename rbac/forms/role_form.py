# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/26 
from rbac.forms.base_form import BaseForm
from rbac import models


class RoleForm(BaseForm):
    class Meta:
        model = models.Role
        fields = ['name']
