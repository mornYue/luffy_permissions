from django.conf import settings


def init_permissions(request, current_user):
    user_permissions_queryset = current_user.roles.filter(permissions__isnull=False).values(
        "permissions__title", "permissions__url", "permissions__is_menu").distinct()
    permission_list = []
    menu_list = []
    for item in user_permissions_queryset:
        permission_list.append(item["permissions__url"])
        if item["permissions__is_menu"]:
            menu_list.append({"title": item["permissions__title"], "url": item["permissions__url"]})
    request.session[settings.USER_PERMISSIONS_KEY] = permission_list
    request.session[settings.USER_MENU_KEY] = menu_list
    print(menu_list)

