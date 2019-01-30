import re
from collections import OrderedDict
from django.shortcuts import reverse
from django.http import QueryDict
from django.utils.module_loading import import_string
from django.conf import settings
from django.urls import URLResolver, URLPattern


def reverse_url_v(request, name, *args, **kwargs):
    base_url = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return base_url
    params = request.GET.get("_filter")
    return "%s?%s" % (base_url, params)


def reverse_url_t(request, name, *args, **kwargs):
    base_url = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return base_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    return "%s?%s" % (base_url, query_dict.urlencode())


# def exclude_list(match_str):
#     """
#     排除掉不需要显示的url
#     :param match_str:
#     :return:
#     """
#     exclude = [
#         '/admin/.*',
#         '/login/.*'
#     ]
#     for item in exclude:
#         if re.match(item, match_str):
#             return True
#     return False
#
#
# def recursion_retrieve(pre_namespace, pre_url, patterns, ordered_dict):
#     """
#     递归检索url
#     :param pre_namespace: 当前检索的patterns的之前的名称空间
#     :param pre_url: 之前的url
#     :param patterns: 需要检索的patterns
#     :param ordered_dict: 一个有序的字典，用来存储所有的url
#     :return:
#     """
#     for item in patterns:
#         url = pre_url + str(item.pattern)  # 获取当前的url
#         if isinstance(item, URLResolver):  # 属于路由分发
#             # print(item.pattern.__class__.__name__)
#             # print("route", item.pattern._route)
#             # print("regex", item.pattern._regex)
#             if exclude_list(url):
#                 continue
#             if pre_namespace:
#                 if item.namespace:
#                     namespace = "%s:%s" % (pre_namespace, item.namespace,)
#                 else:
#                     namespace = pre_namespace
#             else:
#                 if item.namespace:
#                     namespace = item.namespace
#                 else:
#                     namespace = None
#             recursion_retrieve(namespace, url, item.url_patterns, ordered_dict)
#         elif isinstance(item, URLPattern):
#             # print("route", item.pattern._route)
#             # print("regex", item.pattern._regex)
#             if not item.name:
#                 continue
#             # url = pre_url + item.pattern.__str__
#             if exclude_list(url):
#                 continue
#             if pre_namespace:
#                 name = "%s:%s" % (pre_namespace, item.name)
#             else:
#                 name = item.name
#             ordered_dict[name] = {'name': name, 'url': url}
#
#
# def retrieve_all_urls():
#     """
#     检索项目中所有的url
#     :return:
#     """
#     urls_ordered_dict = OrderedDict()
#
#     root_url = import_string(settings.ROOT_URLCONF)
#     recursion_retrieve(None, '/', root_url.urlpatterns, urls_ordered_dict)
#     return urls_ordered_dict


def exclude_url(url):
    for regex_str in settings.EXCLUDE_URLS_LIST:
        if re.match(regex_str, url):
            return True


def retrieve_urls(pre_namespace, pre_url, urlpatterns, url_dict):
    """
    递归部分
    :param pre_namespace: 当前url的前namespace
    :param pre_url: 当前url的前url
    :param urlpatterns: 当前url的patterns
    :param url_dict: 存储url的一个有序字典
    :return:
    """
    for item in urlpatterns:
        sub_url = item.pattern.regex.pattern
        url = pre_url + sub_url
        url = url.replace('^', '').replace('$', '')
        if exclude_url(url):
            continue
        if isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    namespace = pre_namespace
            else:
                namespace = item.namespace
            patterns = item.url_patterns
            retrieve_urls(namespace, url, patterns, url_dict)
        elif isinstance(item, URLPattern):
            name = item.name
            if not name:
                continue
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, name)
            url_dict[name] = {
                "name": name,
                "url": url
            }


def retrieve_project_urls():
    """
    检索项目中的所有url
    :return:
    """
    project_urls_dict = OrderedDict()
    root_url = import_string(settings.ROOT_URLCONF)
    retrieve_urls(None, "/", root_url.urlpatterns, project_urls_dict)
    return project_urls_dict
