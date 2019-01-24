import xlrd
from django.shortcuts import render, redirect

from web import models
from web.custom_forms.customer_form import CustomerForm


def customer_list(request):
    """
    客户列表
    :param request:
    :return:
    """
    customers = models.Customer.objects.all()

    return render(request, 'customer_list.html', {'customers': customers})


def customer_add(request):
    """
    添加客户
    :param request:
    :return:
    """
    if request.method == "GET":
        form = CustomerForm()
        return render(request, "customer_add.html", {"form": form})
    form = CustomerForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/customer/list")
    return render(request, "customer_add.html", {"form": form})


def customer_edit(request, cid):
    """
    客户编辑
    :param request:
    :param cid: 客户id
    :return:
    """
    customer = models.Customer.objects.filter(pk=cid)
    if request.method == "GET":
        form = CustomerForm(instance=customer)
        return render(request, "customer_edit.html", {"form": form})
    form = CustomerForm(data=request.POST, instance=customer)
    if form.is_valid():
        form.save()
        return redirect("/customer/list")
    return render(request, "customer_edit.html", {"form": form})


def customer_del(request, cid):
    """
    删除客户
    :param request:
    :param cid:
    :return:
    """
    models.Customer.objects.filter(pk=cid).delete()
    return redirect("/customer/list")


def customer_import(request):
    """
    用户批量导入
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "customer_import.html")
    context = {"status": True, "msg": "success"}
    try:
        # 获取文件
        import_file = request.FILES.get("customer_excel")
        # 打开excel文件
        work_book = xlrd.open_workbook(file_contents=import_file.file.read())
        row_map = {
            0: {"text": "客户姓名", "name": "name"},
            1: {"text": "年龄", "name": "age"},
            2: {"text": "邮箱", "name": "email"},
            3: {"text": "公司", "name": "company"},
        }
        customers = []
        import_sheet = work_book.sheet_by_index(0)
        for row_num in range(0, import_sheet.nrows):
            row = import_sheet.row(row_num)
            customer_dict = {}
            for col_num, text_name in row_map.items():
                customer_dict[text_name["name"]] = row[col_num].value
            customer = models.Customer(**customer_dict)
            customers.append(customer)
        models.Customer.objects.bulk_create(customers)
    except Exception:
        context["status"] = False
        context["msg"] = "failed"
    return render(request, "customer_import.html")


def customer_tpl(request):
    pass
