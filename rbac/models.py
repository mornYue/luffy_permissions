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
    name = models.CharField(max_length=32, verbose_name="访问地址别名", unique=True)
    # is_menu = models.BooleanField(verbose_name="菜单", help_text="使用布尔值来存放该url是否可以作为菜单")
    menu = models.ForeignKey(to="Menu", verbose_name="所属菜单", on_delete=models.CASCADE,
                             blank=True, null=True)
    sub_menu = models.ForeignKey(to="self", related_name="parent", blank=True, null=True,
                                 verbose_name="所属子菜单", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(max_length=32, verbose_name="菜单名称")
    icon = models.CharField(max_length=32, verbose_name="图标", null=True, blank=True)

    def __str__(self):
        return self.title

