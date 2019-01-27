# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/26 
from django.shortcuts import reverse, render, redirect, HttpResponse

from rbac import models
from rbac.forms.role_form import RoleForm


def role_list(request):
    roles = models.Role.objects.all()
    return render(request, "rbac/role_list.html", locals())


def role_add(request):
    if request.method == "GET":
        form = RoleForm()
        return render(request, "rbac/update.html", locals())
    form = RoleForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse("rbac:role_list"))
    return render(request, "rbac/update.html", locals())


def role_edit(request, rid):
    role = models.Role.objects.get(pk=rid)
    if not role:
        return HttpResponse("用户不存在，修改失败")
    form = RoleForm(instance=role)
    if request.method == "GET":
        return render(request, "rbac/update.html", locals())
    form = RoleForm(request.POST)
    if form.is_valid():
        models.Role.objects.filter(pk=rid).update(**form.cleaned_data)
        return redirect(reverse("rbac:role_list"))
    return render(request, "rbac/update.html", locals())


def role_del(request, rid):
    role = models.Role.objects.get(pk=rid)
    if not role:
        return HttpResponse("用户不存在，删除失败")
    if request.method == "GET":
        return render(request, "rbac/delete.html", {"cancel": reverse("rbac:role_list")})
    role.delete()
    return redirect(reverse("rbac:role_list"))
