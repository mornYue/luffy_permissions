from django.forms import ModelForm

from web import models


class BillForm(ModelForm):
    class Meta:
        # 设置关联model和字段
        model = models.Bill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        初始化样式
        :param args:
        :param kwargs:
        """
        super(ModelForm, self).__init__(*args, **kwargs)

        for name, value in self.fields.items():
            value.widget.attr["class"] = "from-control"
            value.widget.attr["placeholder"] = value.label


