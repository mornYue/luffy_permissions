# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/26 
from django.shortcuts import reverse, render, redirect, HttpResponse

from rbac import models
from rbac.forms.user_form import UserForm


def user_list(request):
    users = models.UserInfo.objects.all()
    return render(request, "rbac/user_list.html", locals())


def user_add(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "rbac/update.html", locals())
    form = UserForm(request.POST)

    if form.is_valid():
        form.cleaned_data.pop("re_pwd")
        models.UserInfo.objects.create_user(**form.cleaned_data)
        return redirect(reverse("rbac:user_list"))
    return render(request, "rbac/update.html", locals())


def user_edit(request, uid):
    user = models.UserInfo.objects.get(pk=uid)
    if not user:
        return HttpResponse("用户不存在，修改失败")
    form = UserForm(instance=user)
    if request.method == "GET":
        return render(request, "rbac/update.html", locals())
    form = UserForm(instance=user, data=request.POST)
    print(123)
    print(form)
    if form.is_valid():
        form.cleaned_data.pop("re_pwd")
        models.UserInfo.objects.filter(pk=uid).update(**form.cleaned_data)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return redirect(reverse("rbac:user_list"))
    return render(request, "rbac/update.html", locals())


def user_del(request, uid):
    user = models.UserInfo.objects.get(pk=uid)
    if not user:
        return HttpResponse("用户不存在，删除失败")
    if request.method == "GET":
        return render(request, "rbac/delete.html", {"cancel": reverse("rbac:user_list")})
    user.delete()
    return redirect(reverse("rbac:user_list"))
