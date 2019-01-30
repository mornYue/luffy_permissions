from django.urls import re_path

from rbac.views import role, user, menu
from rbac.utils import url_util

urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name="role_list"),
    re_path(r'^role/add/$', role.role_add, name="role_add"),
    re_path(r'^role/edit/(?P<rid>\d+)', role.role_edit, name="role_edit"),
    re_path(r'^role/del/(?P<rid>\d+)', role.role_del, name="role_del"),

    re_path(r'^user/list/$', user.user_list, name="user_list"),
    re_path(r'^user/add/$', user.user_add, name="user_add"),
    re_path(r'^user/edit/(?P<uid>\d+)', user.user_edit, name="user_edit"),
    re_path(r'^user/del/(?P<uid>\d+)', user.user_del, name="user_del"),

    re_path(r'^menu/list/$', menu.menu_list, name="menu_list"),
    re_path(r'^menu/add/$', menu.menu_add, name="menu_add"),
    re_path(r'^menu/edit/(?P<mid>\d+)', menu.menu_edit, name="menu_edit"),
    re_path(r'^menu/del/(?P<mid>\d+)', menu.menu_del, name="menu_del"),

    re_path(r'^submenu/add/(?P<mid>\d+)', menu.submenu_add, name="submenu_add"),
    re_path(r'^submenu/edit/(?P<sid>\d+)', menu.submenu_edit, name="submenu_edit"),
    re_path(r'^submenu/del/(?P<sid>\d+)', menu.submenu_del, name="submenu_del"),

    re_path(r'^permission/add/(?P<sid>\d+)', menu.permission_add, name="permission_add"),
    re_path(r'^permission/edit/(?P<pid>\d+)', menu.permission_edit, name="permission_edit"),
    re_path(r'^permission/del/(?P<pid>\d+)', menu.permission_del, name="permission_del"),

    re_path(r'^bulk/operate/', menu.bulk_operate, name="bulk_operate"),
    re_path(r'^bulk/delete/(?P<pk>\d+)', menu.bulk_del, name="bulk_delete")
]
