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

    # if request.method == 'GET':
    #     return render(request, 'customer_import.html')
    #
    # context = {'status': True, 'msg': '导入成功'}
    # try:
    #     customer_excel = request.FILES.get('customer_excel')
    #     """
    #     打开上传的Excel文件，并读取内容
    #     注：打开本地文件时，可以使用：workbook = xlrd.open_workbook(filename='本地文件路径.xlsx')
    #     """
    #     workbook = xlrd.open_workbook(file_contents=customer_excel.file.read())
    #
    #     # sheet = workbook.sheet_by_name('工作表1')
    #     sheet = workbook.sheet_by_index(0)
    #     row_map = {
    #         0: {'text': '客户姓名', 'name': 'name'},
    #         1: {'text': '年龄', 'name': 'age'},
    #         2: {'text': '邮箱', 'name': 'email'},
    #         3: {'text': '公司', 'name': 'company'},
    #     }
    #     customers = []
    #     for row_num in range(1, sheet.nrows):
    #         row = sheet.row(row_num)
    #         row_dict = {}
    #         for col_num, text_name in row_map.items():
    #             row_dict[text_name['name']] = row[col_num].value
    #         customers.append(models.Customer(**row_dict))
    #
    #     models.Customer.objects.bulk_create(customers, batch_size=20)
    # except Exception as e:
    #     context['status'] = False
    #     context['msg'] = '导入失败'
    #
    # return render(request, 'customer_import.html', context)


def customer_tpl(request):
    pass
