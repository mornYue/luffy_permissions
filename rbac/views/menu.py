# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/28
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.forms.formsets import formset_factory

from rbac import models
from rbac.forms.menu_form import MenuForm, SubmenuForm, PermissionForm, BatchAddPermissionsForm
from rbac.forms.menu_form import BatchUpdatePermissionsForm
from rbac.utils.url_util import reverse_url_v, retrieve_project_urls


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


def bulk_operate(request):
    """
    权限批量操作, 基于三点
        1. formset实现批量数据
            可以尝试使用modelformset
            注意: 在进行保存的时候，如果是添加的话，可以将对象存在一个列表中，之后批量创建，但是更新的话需要每个对象都保存
                并且，因为数据库中表的某些字段存在唯一性约束，所以需要判断，如果重复，提示用户，并且提交失败
        2. 自动发现项目中的url
            获取当前url的时候利用的是urlpattern和resolverpattern
        3. 利用set的集合运算
            项目中的集合: set_project
            数据库中的集合: set_db

    批量更新：
        项目中存在的url，但是在数据库中不存在
            set_project - set_db
    批量删除:
        数据库中存在的url，项目中不存在
            set_db - set_project
            不推荐进行批量删除操作，推荐让用户自行绝对删除
    批量更新:
        数据库和项目中都存在的
            set_db & set_project
        这里需要注意一点，推荐对url进行对比，之后显示出来的时候提示数据库中的项目中的是否一致，如果一致，可以更新，否则需要
        处理，在url字段部分显示数据库和项目中不匹配来提醒用户
    :param request:
    :return:
    """
    create_formset_class = formset_factory(BatchAddPermissionsForm, extra=0)
    create_formset = None
    update_formset_class = formset_factory(BatchUpdatePermissionsForm, extra=0)
    update_formset = None
    operate_type = request.GET.get("type")
    if request.method == "POST":
        if operate_type == "create":
            create_formset = create_formset_class(request.POST)
            if create_formset.is_valid():
                post_row_list = create_formset.cleaned_data
                bulk_create_list = []
                flag = True
                for index in range(0, create_formset.total_form_count()):
                    try:
                        row = post_row_list[index]
                        create_obj = models.Permission(**row)
                        create_obj.validate_unique()
                        bulk_create_list.append(create_obj)
                        print(create_obj)
                    except ValidationError as e:
                        create_formset.errors[index].update(e)
                        flag = False
                if flag:
                    models.Permission.objects.bulk_create(bulk_create_list)
        elif operate_type == "update":
            update_formset = update_formset_class(request.POST)
            if update_formset.is_valid():
                post_row_list = update_formset.cleaned_data
                for index in range(0, update_formset.total_form_count()):
                    try:
                        row = post_row_list[index]
                        update_obj = models.Permission.objects.get(pk=row['id'])
                        if not update_obj:
                            return HttpResponse("该权限不存在，提交失败")
                        update_obj.validate_unique()
                        update_obj.save()
                    except ValidationError as e:
                        create_formset.errors[index].update(e)
            elif operate_type == "delete":
                pid = request.GET.get('pid')
                permission = models.Permission.objects.get(pk=pid)
                if not permission:
                    return HttpResponse("权限不存在，删除失败")
                permission.delete()
                return redirect(reverse_url_v(request, "rbac:bulk_operate"))
    # 获取集合
    db_url_set = set()
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'sub_menu_id')
    permission_dict = {}
    for item in permissions:
        permission_dict[item['name']] = item
        db_url_set.add(item['name'])
    project_url_dict = retrieve_project_urls()
    project_url_set = set(project_url_dict.keys())
    # 判断项目中的url和数据库中的url是否相等，因为修改的时候是以数据库为准的，所以这里会修改数据库的value值提示异常
    # 批量添加
    bulk_create_set = project_url_set - db_url_set
    if not create_formset:
        create_formset = create_formset_class(
            initial=[value for name, value in project_url_dict.items() if name in bulk_create_set]
        )
    # 删除
    delete_set = db_url_set - project_url_set
    delete_list = [value for name, value in permission_dict.items() if name in delete_set]
    # 批量修改
    bulk_update_set = project_url_set & db_url_set
    if not  update_formset:
        update_formset = update_formset_class(
            initial=[value for name, value in permission_dict.items() if name in bulk_update_set]
        )
    return render(request, "rbac/batch_operate.html", {
        'create_formset': create_formset,
        'delete_list': delete_list,
        'update_formset': update_formset,
    })


def bulk_del(request, pk):
    """
    批量页面的权限删除
    :param request:
    :param pk:
    :return:
    """
    url = reverse_url_v(request, 'rbac:bulk_operate')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)
