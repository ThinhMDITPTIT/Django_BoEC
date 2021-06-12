from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.fields.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
            'last_name': forms.fields.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
            'username': forms.fields.TextInput(attrs={'placeholder': 'User name', 'class': 'form-control'}),
            'email': forms.fields.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'password1': forms.fields.TextInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
            'password2': forms.fields.TextInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }

        def save(self, commit=True):
            user = super(CustomerForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user