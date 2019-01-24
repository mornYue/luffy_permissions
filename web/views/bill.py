from django.shortcuts import render, redirect
from web import models
from web.custom_forms.bill_form import BillForm


def bill_list(request):
    bills = models.Bill.objects.all()

    return render(request, "bill_list.html", {"bills": bills, })


def bill_add(request):
    if request.method == "GET":
        form = BillForm()
        return render(request, "bill_add.html", {"form": form})
    form = BillForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/customer/list")
    return render(request, "bill_add.html", {"form": form})


def bill_edit(request, bid):
    bill = models.Bill.objects.filter(pk=bid)
    if request.method == "GET":
        form = BillForm(instance=bill)
        return render(request, "bill_edit.html", {"form": form})
    form = BillForm(data=request.POST, instance=bill)
    if form.is_valid():
        form.save()
        return redirect("/customer/list")
    return render(request, "bill_edit.html", {"form": form})


def bill_del(request, bid):
    models.Bill.objects.filter(pk=bid).delete()
    return redirect("/bill/list")
