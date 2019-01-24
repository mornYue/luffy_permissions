from django.urls import re_path
from web.views import customer, bill

urlpatterns = [
    re_path(r'^customer/list/$', customer.customer_list),
    re_path(r'^customer/add/$', customer.customer_add),
    re_path(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit),
    re_path(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del),
    re_path(r'^customer/import/$', customer.customer_import),
    re_path(r'^customer/tpl/$', customer.customer_tpl),

    re_path(r'^bill/list/$', bill.bill_list),
    re_path(r'^bill/add/$', bill.bill_add),
    re_path(r'^bill/edit/(?P<bid>\d+)/$', bill.bill_edit),
    re_path(r'^bill/del/(?P<bid>\d+)/$', bill.bill_del),
]