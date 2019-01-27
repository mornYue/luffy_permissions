import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class PermissionMiddleware(MiddlewareMixin):
    """
    对用户权限进行验证
    """
    def process_request(self, request):
        req_path = request.path_info
        for item in settings.WHITE_LIST:
            if re.match(item, req_path):
                return None
        permissions = request.session.get(settings.USER_PERMISSIONS_KEY).values()
        url_record = [
            {"title": "首页", "url": "/customer/list"}
        ]
        if not permissions:
            return HttpResponse("没有检测到登录信息，请重新登录")
        for item in permissions:
            url = "^%s$" % item["url"]
            print()
            if re.match(url, req_path):
                request.selected_permission = item["sub_menu"] or item["permission_id"]
                if item["sub_menu"]:
                    url_record.append(
                        {
                            "title": item["sub_menu_title"],
                            "url": item["sub_menu_url"]
                        }
                    )

                url_record.append(
                    {
                        "title": item["title"],
                        "url": item["url"]
                    }
                )
                request.url_record = url_record
                return None
        return HttpResponse("权限不足，无法访问")
