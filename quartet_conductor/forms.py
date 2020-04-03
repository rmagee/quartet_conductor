from django import forms
from quartet_conductor.models import Session
lot_regex = r'^10([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,20})$'

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['lot', 'expiry']
