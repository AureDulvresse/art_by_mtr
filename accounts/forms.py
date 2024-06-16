from django.contrib.auth.forms import AuthenticationForm
from django import forms
from accounts.models import Customer

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrer votre nom d''utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrer votre mot de passe'}))

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrer votre mot de passe'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer votre mot de passe'}))

    class Meta:
        model = Customer
        fields =  ['username', 'first_name', 'last_name', 'email', 'password']

    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error(None, 'Les mots de passe ne correspondent pas')