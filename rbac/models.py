from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """
    用户表
    使用auth组件进行创建
    """
    roles = models.ManyToManyField(to="Role")

    def __str__(self):
        return self.username


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, verbose_name="角色名称")

    permissions = models.ManyToManyField(to="Permission", blank=True, null=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    权限表
    根据不同角色是否能访问某些url来间接的制定相应的权限
    """
    title = models.CharField(max_length=32, verbose_name="权限名称")
    url = models.CharField(max_length=128, verbose_name="访问地址", help_text="存放url的正则匹配的格式")

    def __str__(self):
        return self.title
