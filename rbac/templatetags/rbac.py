# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/25
import re
from collections import OrderedDict
from django.template import Library
from django.conf import settings

from rbac.utils.url_util import reverse_url_t

register = Library()


@register.inclusion_tag("rbac/first_level_menu.html")
def first_level_menu(request):
    menus = request.session[settings.USER_MENU_KEY]
    return {"menus": menus, "request": request}


"""
旧版本
@register.inclusion_tag("rbac/multi_menu.html")
def multi_menu(request):
    menu_dict = request.session[settings.USER_MENU_KEY]
    menus = OrderedDict()
    sort_keys = sorted(menu_dict)
    for key in sort_keys:
        menu = menu_dict[key]
        menu["class"] = "hide"
        for p_key, value in menu["children"].items():
            re_url = value["url"]
            if value.get("sub_menu"):
                value["class"] = "hide"
                if re.match(re_url, request.path_info):
                    menu["children"][str(value["sub_menu"])]["class"] = "active"
                    menu["class"] = ""
            elif re.match(re_url, request.path_info):
                value["class"] = "active"
                menu["class"] = ""
        menus[key] = menu
    return {"menus": menus.values(), "request": request}
"""


@register.inclusion_tag("rbac/multi_menu.html")
def multi_menu(request):
    menu_dict = request.session[settings.USER_MENU_KEY]
    menus = OrderedDict()
    # print(menu_dict)
    sort_keys = sorted(menu_dict)
    for key in sort_keys:
        menu = menu_dict[key]
        menu["class"] = "hide"
        for value in menu["children"]:
            req_id = request.selected_permission
            if value["permission_id"] == req_id:
                value["class"] = "active"
                menu["class"] = ""
        menus[key] = menu
    return {"menus": menus.values(), "request": request}


@register.filter
def permission_display(request, name):
    menu_dict = request.session[settings.USER_PERMISSIONS_KEY]
    if name in menu_dict:
        return True


@register.simple_tag
def reverse_url(request, name, *args, **kwargs):
    """
    url反向解析并且保存选中信息
    :param request:
    :param name: url别名
    :param args: 参数
    :param kwargs: 参数
    :return:
    """
    return reverse_url_t(request, name, *args, **kwargs)

