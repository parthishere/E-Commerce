from django import forms 

class GuestForm(forms.Form):
    email = forms.EmailField()