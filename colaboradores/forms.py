from django import forms
from django.contrib.auth.forms import AuthenticationForm

class FormLoginPersonalizado(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def clean(self):
        cleaned_data = super().clean()
        remember_me = self.cleaned_data.get('remember_me')
        
        if remember_me:
            
            self.request.session.set_expiry(1209600)
            self.request.session.cookie_date_changed = True
        else:
            
            self.request.session.set_expiry(0)
            
        return cleaned_data