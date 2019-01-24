from django.db import models

# Create your models here.


class Customer(models.Model):
    """
    客户表
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    company = models.CharField(verbose_name='公司', max_length=32)


class Bill(models.Model):
    """
    交易记录
    """
    customer = models.ForeignKey(verbose_name='客户', to='Customer', on_delete=models.CASCADE)
    money = models.IntegerField(verbose_name='交易金额')
    create_time = models.DateTimeField(verbose_name='交易时间', auto_now_add=True)