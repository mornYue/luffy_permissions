# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/28 

from django.shortcuts import reverse, render, redirect, HttpResponse

from rbac import models
from rbac.forms.menu_form import MenuForm


def menu_list(request):
    menus = models.Menu.objects.all()
    menu_id = request.GET.get("mid")
    return render(request, "rbac/menu_list.html", locals())


def menu_add(request):
    if request.method == "GET":
        form = MenuForm()
        return render(request, "rbac/update.html", locals())
    form = MenuForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse("rbac:menu_list"))
    return render(request, "rbac/update.html", locals())


def menu_edit(request, mid):
    menu = models.Menu.objects.get(pk=mid)
    if not menu:
        return HttpResponse("菜单不存在，修改失败")
    form = MenuForm(instance=menu)
    if request.method == "GET":
        return render(request, "rbac/update.html", locals())
    form = MenuForm(request.POST)
    if form.is_valid():
        models.Menu.objects.filter(pk=mid).update(**form.cleaned_data)
        return redirect(reverse("rbac:menu_list"))
    return render(request, "rbac/update.html", locals())


def menu_del(request, mid):
    menu = models.Menu.objects.get(pk=mid)
    if not menu:
        return HttpResponse("菜单不存在，删除失败")
    if request.method == "GET":
        return render(request, "rbac/delete.html", {"cancel": reverse("rbac:menu_list")})
    menu.delete()
    return redirect(reverse("rbac:menu_list"))
