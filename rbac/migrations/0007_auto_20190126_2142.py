# Generated by Django 2.1.4 on 2019-01-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='访问地址别名'),
        ),
    ]