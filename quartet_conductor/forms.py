from django import forms
from django.forms import widgets
from quartet_conductor.models import Session, InputMap
from django.utils.safestring import SafeString

lot_regex = r'^10([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,20})$'


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['lot', 'expiry']


class InputMapForm(forms.ModelForm):
    class Meta:
        model = InputMap
        fields = '__all__'

    def as_table(self):
        ret = super().as_table()
        return SafeString(ret.replace('helptext', 'uk-text-small uk-text-light'))

    def update_field_styles(self):
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) and isinstance(field.widget, widgets.Textarea):
                field.widget.attrs.update({
                    'class':'uk-textarea'
                })
            elif isinstance(field, forms.CharField):
                field.widget.attrs.update({
                    'class':'uk-input'
                })
            elif isinstance(field, forms.ModelChoiceField):
                field.widget.attrs.update({
                    'class': 'uk-select'
                })
            elif isinstance(field, forms.IntegerField):
                field.widget.attrs.update({
                    'class': 'uk-input'
                })
