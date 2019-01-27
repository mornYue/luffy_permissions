from django.urls import re_path

from rbac.views import role, user, menu

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
]
