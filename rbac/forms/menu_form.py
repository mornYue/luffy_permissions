# -*-coding:utf-8-*-
# __author__ = "Morn"
# Date:2019/1/28
from django import forms
from django.utils.safestring import mark_safe
from django.db.models import Q

from rbac import models
from rbac.forms.base_form import BaseForm

ICON_LIST = [
    ['fa-hand-scissors-o', '<i aria-hidden="true" class="fa fa-hand-scissors-o"></i>'],
    ['fa-hand-spock-o', '<i aria-hidden="true" class="fa fa-hand-spock-o"></i>'],
    ['fa-hand-stop-o', '<i aria-hidden="true" class="fa fa-hand-stop-o"></i>'],
    ['fa-handshake-o', '<i aria-hidden="true" class="fa fa-handshake-o"></i>'],
    ['fa-hard-of-hearing', '<i aria-hidden="true" class="fa fa-hard-of-hearing"></i>'],
    ['fa-hashtag', '<i aria-hidden="true" class="fa fa-hashtag"></i>'],
    ['fa-hdd-o', '<i aria-hidden="true" class="fa fa-hdd-o"></i>'],
    ['fa-headphones', '<i aria-hidden="true" class="fa fa-headphones"></i>'],
    ['fa-heart', '<i aria-hidden="true" class="fa fa-heart"></i>'],
    ['fa-heart-o', '<i aria-hidden="true" class="fa fa-heart-o"></i>'],
    ['fa-heartbeat', '<i aria-hidden="true" class="fa fa-heartbeat"></i>'],
    ['fa-history', '<i aria-hidden="true" class="fa fa-history"></i>'],
    ['fa-home', '<i aria-hidden="true" class="fa fa-home"></i>'],
    ['fa-hotel', '<i aria-hidden="true" class="fa fa-hotel"></i>'],
    ['fa-hourglass', '<i aria-hidden="true" class="fa fa-hourglass"></i>'],
    ['fa-hourglass-1', '<i aria-hidden="true" class="fa fa-hourglass-1"></i>'],
    ['fa-hourglass-2', '<i aria-hidden="true" class="fa fa-hourglass-2"></i>'],
    ['fa-hourglass-3', '<i aria-hidden="true" class="fa fa-hourglass-3"></i>'],
    ['fa-hourglass-end', '<i aria-hidden="true" class="fa fa-hourglass-end"></i>'],
    ['fa-hourglass-half', '<i aria-hidden="true" class="fa fa-hourglass-half"></i>'],
    ['fa-hourglass-o', '<i aria-hidden="true" class="fa fa-hourglass-o"></i>'],
    ['fa-hourglass-start', '<i aria-hidden="true" class="fa fa-hourglass-start"></i>'],
    ['fa-i-cursor', '<i aria-hidden="true" class="fa fa-i-cursor"></i>'],
    ['fa-id-badge', '<i aria-hidden="true" class="fa fa-id-badge"></i>'],
    ['fa-id-card', '<i aria-hidden="true" class="fa fa-id-card"></i>'],
    ['fa-id-card-o', '<i aria-hidden="true" class="fa fa-id-card-o"></i>'],
    ['fa-image', '<i aria-hidden="true" class="fa fa-image"></i>'],
    ['fa-mail-reply-all', '<i aria-hidden="true" class="fa fa-mail-reply-all"></i>'],
    ['fa-reply', '<i aria-hidden="true" class="fa fa-reply"></i>'],
    ['fa-reply-all', '<i aria-hidden="true" class="fa fa-reply-all"></i>'],
    ['fa-retweet', '<i aria-hidden="true" class="fa fa-retweet"></i>'],
    ['fa-wrench', '<i aria-hidden="true" class="fa fa-wrench"></i>']]

for icon in ICON_LIST:
    icon[1] = mark_safe(icon[1])


class MenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = "__all__"

        widgets = {
            "icon": forms.RadioSelect(
                attrs={"class": "clearfix"},
                choices=ICON_LIST
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            )
        }


class SubmenuForm(BaseForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url', 'name', 'menu']


class PermissionForm(BaseForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url', 'name']


class BatchAddPermissionsForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    url = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    menu_id = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=[
            (None, '------'),
        ],
        required=False
    )
    sub_menu_id = forms.ChoiceField(
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        choices=[
            (None, '------')
        ],
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(BatchAddPermissionsForm, self).__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['sub_menu_id'].choices += models.Permission.objects.filter(
            Q(menu__isnull=False) & Q(sub_menu__isnull=True)
        ).values_list('id', 'title')


class BatchUpdatePermissionsForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    url = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    menu_id = forms.ChoiceField(
        choices=[(None, "------")],
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    sub_menu_id = forms.ChoiceField(
        choices=[(None, '------')],
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(BatchUpdatePermissionsForm, self).__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['sub_menu_id'].choices += models.Permission.objects.filter(
            menu__isnull=False, sub_menu__isnull=True).values_list('id', 'title')
