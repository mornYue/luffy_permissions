from django.shortcuts import render, redirect
from web import models
from web.custom_forms.bill_form import BillForm


def bill_list(request):
    bills = models.Bill.objects.all()

    return render(request, "bill_list.html", locals())


def bill_add(request):
    if request.method == "GET":
        form = BillForm()
        return render(request, "bill_add.html", locals())
    form = BillForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/customer/list")
    return render(request, "bill_add.html", locals())


def bill_edit(request, bid):
    bill = models.Bill.objects.filter(pk=bid).get()
    if request.method == "GET":
        form = BillForm(instance=bill)
        return render(request, "bill_edit.html", locals())
    form = BillForm(data=request.POST, instance=bill)
    if form.is_valid():
        form.save()
        return redirect("/customer/list")
    return render(request, "bill_edit.html", locals())


def bill_del(request, bid):
    models.Bill.objects.filter(pk=bid).delete()
    return redirect("/bill/list")
