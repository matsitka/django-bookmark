from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
#from django.utils.translation import ugettext_lazy as _

class MainForm(forms.Form):
    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])

class SigninForm(MainForm):
    email = forms.EmailField(required=True,  widget=forms.TextInput(attrs = {'class': 'first-top', 'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs = {'class': 'last-bottom', 'placeholder': 'Password'}, render_value=False))


class UserForm(SigninForm):
    name = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs = {'class': 'first-top', 'placeholder': 'Username'}), label=('name'))

    #url = forms.CharField(max_length=200, widget=forms.TextInput(attrs = {'class': 'first-top', 'placeholder': 'URL'}))

    email = forms.EmailField(required=True, max_length=200, widget=forms.TextInput(attrs = {'placeholder': 'Email'}))
    password = forms.CharField(required=True, label=('Password'), widget=forms.PasswordInput(attrs = {'placeholder': 'Password'}, render_value=False))
    ver_password = forms.CharField(required=True, label=('Verify Password'), widget=forms.PasswordInput(attrs = {'class': 'last-bottom', 'placeholder': 'Confirm Password'}, render_value=False))

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        ver_password = cleaned_data.get('ver_password')
        if password != ver_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    #order the forms field http://stackoverflow.com/a/5747259/2942942
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
        'name',
        'email',
        'password',
        'ver_password']

