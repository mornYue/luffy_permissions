from django.forms import ModelForm

from web import models


class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __int__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for name, value in self.fields.item():
            value.widget.attr['class'] = "form-control"
            value.widget.attr['placeholder'] = value.label
