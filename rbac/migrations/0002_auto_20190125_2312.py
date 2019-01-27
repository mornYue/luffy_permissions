# Generated by Django 2.1.4 on 2019-01-25 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='图标'),
        ),
        migrations.AddField(
            model_name='permission',
            name='is_menu',
            field=models.BooleanField(default=False, help_text='使用布尔值来存放该url是否可以作为菜单', verbose_name='菜单'),
            preserve_default=False,
        ),
    ]