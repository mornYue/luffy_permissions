from django.shortcuts import reverse
from django.http import QueryDict


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
