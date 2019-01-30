from django.urls import re_path
from web.views import customer, bill, account

urlpatterns = [
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^logout/$', account.logout, name='logout'),

    re_path(r'^customer/list/$', customer.customer_list, name='customer_list'),
    re_path(r'^customer/add/$', customer.customer_add, name='customer_add'),
    re_path(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit, name='customer_edit'),
    re_path(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del, name='customer_del'),
    re_path(r'^customer/import/$', customer.customer_import, name='customer_import'),
    re_path(r'^customer/tpl/$', customer.customer_tpl, name='customer_tpl'),

    re_path(r'^bill/list/$', bill.bill_list, name='bill_list'),
    re_path(r'^bill/add/$', bill.bill_add, name='bill_add'),
    re_path(r'^bill/edit/(?P<bid>\d+)/$', bill.bill_edit, name='bill_edit'),
    re_path(r'^bill/del/(?P<bid>\d+)/$', bill.bill_del, name='bill_del'),
]