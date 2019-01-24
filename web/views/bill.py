from django.shortcuts import render
from web import models


def bill_list(request):
    bills = models.Bill.objects.all()

    return render(request, "bill_list.html", {"bills": bills, })


def bill_add(request):
    pass


def bill_edit(request, bid):
    pass


def bill_del(request, bid):
    pass
