from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from rbac import models

# Register your models here.


class MyUserAdmin(UserAdmin):
    """
    继承UserAdmin，如果自己有新定义的字段，那么重写里面的fieldsets，该变量是元组，_是django.utils.translation
    模块的gettext_lazy
    _('Important_dates'),...这个元素之前的基本不用动，[看需求], 如果有自己定义的字段，可以在之后添加，e.g.
    (_('Roles'), {'fields': ('roles', )}),Roles是给需要添加的内容命名，可以任意叫，但是fileds里面的东西必须
    是自己已经定义过的字段
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Roles'), {'fields': ('roles', )})
        )


admin.site.register(models.UserInfo, MyUserAdmin)
admin.site.register(models.Role)
admin.site.register(models.Permission)