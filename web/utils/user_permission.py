import re

from django.conf import settings


def init_permissions(request, current_user):
    user_permissions_queryset = current_user.roles.filter(permissions__isnull=False).values(
        "permissions__id",
        "permissions__title",
        "permissions__url",
        "permissions__name",
        "permissions__menu",
        "permissions__menu__title",
        "permissions__menu__icon",
        "permissions__sub_menu",
        "permissions__sub_menu__title",
        "permissions__sub_menu__url",
    ).distinct()
    permission_dict = {}
    menu_dict = {}
    for item in user_permissions_queryset:
        permission_id = item["permissions__id"]
        title = item["permissions__title"]
        url = item["permissions__url"]
        name = item["permissions__name"]
        node = {"permission_id": permission_id, "title": title, "url": url}
        sub_menu = item["permissions__sub_menu"]
        sub_menu_url = item["permissions__sub_menu__url"]
        sub_menu_title = item["permissions__sub_menu__title"]
        menu_id = item["permissions__menu"]
        permission_dict[name] = {
            "url": url,
            "title": title,
            "permission_id": permission_id,
            "sub_menu": sub_menu,
            "sub_menu_url": sub_menu_url,
            "sub_menu_title": sub_menu_title,
        }
        if not item["permissions__menu"]:
            continue
        if menu_id in menu_dict:
            menu_dict[menu_id]["children"].append(node)
        else:
            menu_dict[menu_id] = {
                "title": item["permissions__menu__title"],
                "icon": item["permissions__menu__icon"],
                "children": [
                    node,
                ]
            }
    request.session[settings.USER_PERMISSIONS_KEY] = permission_dict
    request.session[settings.USER_MENU_KEY] = menu_dict
    print("初始化权限", menu_dict)
    # print(permission_list)

