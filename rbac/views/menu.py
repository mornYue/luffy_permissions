# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/28 

from django.shortcuts import  render, redirect, HttpResponse

from rbac import models
from rbac.forms.menu_form import MenuForm, SubmenuForm, PermissionForm
from rbac.utils.url_util import reverse_url_v


def menu_list(request):
    menus = models.Menu.objects.all()
    menu_id = request.GET.get("mid")
    if menu_id:
        submenus = models.Permission.objects.filter(menu=menu_id)
    submenu_id = request.GET.get("sid")
    if submenu_id:
        permissions = models.Permission.objects.filter(sub_menu=submenu_id)
    return render(request, "rbac/menu_list.html", locals())


def menu_add(request):
    if request.method == "GET":
        form = MenuForm()
        return render(request, "rbac/update.html", locals())
    form = MenuForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse_url_v(request, "rbac:menu_list"))
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
        return redirect(reverse_url_v(request, "rbac:menu_list"))
    return render(request, "rbac/update.html", locals())


def menu_del(request, mid):
    menu = models.Menu.objects.get(pk=mid)
    if not menu:
        return HttpResponse("菜单不存在，删除失败")
    if request.method == "GET":
        return render(request, "rbac/delete.html", {"cancel": reverse_url_v(request, "rbac:menu_list")})
    menu.delete()
    return redirect(reverse_url_v(request, "rbac:menu_list"))


def submenu_add(request, mid):
    if request.method == "GET":
        menu = models.Menu.objects.get(pk=mid)
        form = SubmenuForm(initial={"menu": menu})
        return render(request, "rbac/update.html", locals())
    form = SubmenuForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse_url_v(request, "rbac:menu_list"))
    return render(request, "rbac/update.html", locals())


def submenu_edit(request, sid):
    submenu = models.Permission.objects.get(pk=sid)
    if not submenu:
        return HttpResponse("子菜单不存在，修改失败")
    form = SubmenuForm(instance=submenu)
    if request.method == "GET":
        return render(request, "rbac/update.html", locals())
    form = SubmenuForm(request.POST)
    if form.is_valid():
        models.Permission.objects.filter(pk=sid).update(**form.cleaned_data)
        return redirect(reverse_url_v(request, "rbac:menu_list"))
    return render(request, "rbac/update.html", locals())


def submenu_del(request, sid):
    submenu = models.Permission.objects.get(pk=sid)
    if not submenu:
        return HttpResponse("子菜单不存在，删除失败")
    if request.method == "GET":
        return render(request, "rbac/delete.html", {"cancel": reverse_url_v(request, "rbac:menu_list")})
    submenu.delete()
    return redirect(reverse_url_v(request, "rbac:menu_list"))


def permission_add(request, sid):
    if request.method == "GET":
        form = PermissionForm()
        return render(request, "rbac/update.html", locals())
    form = PermissionForm(request.POST)
    if form.is_valid():
        sub_menu = models.Permission.objects.get(pk=sid)
        form.instance.sub_menu = sub_menu
        form.save()
        return redirect(reverse_url_v(request, "rbac:menu_list"))
    return render(request, "rbac/update.html", locals())


def permission_edit(request, pid):
    permission = models.Permission.objects.get(pk=pid)
    if not permission:
        return HttpResponse("子菜单不存在，修改失败")
    form = PermissionForm(instance=permission)
    if request.method == "GET":
        return render(request, "rbac/update.html", locals())
    form = PermissionForm(request.POST)
    if form.is_valid():
        models.Permission.objects.filter(pk=pid).update(**form.cleaned_data)
        return redirect(reverse_url_v(request, "rbac:menu_list"))
    return render(request, "rbac/update.html", locals())


def permission_del(request, pid):
    permission = models.Permission.objects.get(pk=pid)
    if not permission:
        return HttpResponse("子菜单不存在，删除失败")
    if request.method == "GET":
        return render(request, "rbac/delete.html", {"cancel": reverse_url_v(request, "rbac:menu_list")})
    permission.delete()
    return redirect(reverse_url_v(request, "rbac:menu_list"))
