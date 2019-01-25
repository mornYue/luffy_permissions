from django.shortcuts import render, redirect
from django.contrib import auth

from web.custom_forms.user_form import UserForm
from web.utils.user_permission import init_permissions


def login(request):
    form = UserForm()
    if request.method == "GET":
        return render(request, "login.html", locals())
    username = request.POST.get("username")
    password = request.POST.get("password")
    req_user = auth.authenticate(username=username, password=password)
    if not req_user:
        return render(request, "login.html", locals())
    auth.login(request, req_user)
    init_permissions(request, req_user)
    return redirect("/customer/list")


def logout(request):
    auth.logout(request)
    return redirect("/login/")



