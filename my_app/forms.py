import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import modelformset_factory

from my_app.models import User, Inventories, InventoriesTypes, InventoryImage


class UserForm(UserCreationForm):
    password1 = forms.CharField(error_messages={'required': 'enter a valid user password'},
                                widget=forms.PasswordInput(attrs={'placeholder': 'password'}), min_length=8)
    password2 = forms.CharField(error_messages={'required': 'enter a valid user password'},
                                widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}), min_length=8)

    def clean_username(self):
        data = self.cleaned_data.get('username')

        if not re.match('^[a-z A-Z/!#$%^&*()_+\-=\[\]{}:",.<>?]', data):
            raise forms.ValidationError("Enter a valid username. This value may dnot int")
        return data

    def clean_email(self):
        data = self.cleaned_data.get('email')
        special_characters_pattern = r"[0-9 !#$%&*()_+=\[\]{}:;\"',<>?^]"

        if re.search(special_characters_pattern, data):
            raise forms.ValidationError("Email contains invalid characters.")
        return data

    def clean_password1(self):
        data = self.cleaned_data.get('password1')
        lowercase_pattern = r'[a-z]'
        uppercase_pattern = r'[A-Z]'
        digit_pattern = r'[0-9]'
        special_char_pattern = r'[!@#$%^&*(),.?":{}|<>]'

        if (not re.search(lowercase_pattern, data) or
                not re.search(uppercase_pattern, data) or
                not re.search(digit_pattern, data) or
                not re.search(special_char_pattern, data)):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character. ")
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'inventories')

        widgets = {
            "username": forms.TextInput(attrs={'placeholder': 'enter username'}),
            "email": forms.TextInput(attrs={'placeholder': 'enter Email address'}),
        }
        error_messages = {
            "username": {'required': 'enter a valid username'},
            "email": {'required': 'enter a valid email'},
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(error_messages={'required': 'enter a valid user username'},
                               widget=forms.TextInput(attrs={'placeholder': 'enter username'}))
    password = forms.CharField(error_messages={'required': 'enter a valid user password'},
                               widget=forms.PasswordInput(attrs={'placeholder': 'enter Password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User does not exist.! enter a valid user')
        return username

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #
    #     if not User.objects.filter(password=password).exists():
    #         raise forms.ValidationError('Incorrect username  password !!')
    #     return password


class InventoriesForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Inventories
        fields = ('inventry_type', 'name', 'quantity', 'unit_price', 'purchase_date')
        widgets = {
            "inventry_type": forms.Select(attrs={'placeholder': 'enter inventry_type', 'class': 'form-control'}),
            "name": forms.TextInput(attrs={'placeholder': 'Enter name', 'class': 'form-control'}),
            "quantity": forms.NumberInput(attrs={'placeholder': 'Enter quantity', 'class': 'form-control'}),
            "purchase_date": forms.DateInput(
                attrs={'placeholder': 'Enter purchase date', 'class': 'form-control', 'type': 'Date'}),
            "unit_price": forms.NumberInput(attrs={'placeholder': 'Enter a price', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        type = kwargs.pop('type', None)
        super(InventoriesForm, self).__init__(*args, **kwargs)
        if type:
            self.fields['inventry_type'].queryset = InventoriesTypes.objects.filter(type=type)


class InventoryImageForm(forms.ModelForm):

    class Meta:
        model = InventoryImage
        fields = ['image']


InventoryImageFormSet = modelformset_factory(InventoryImage, form=InventoryImageForm, extra=1)


class InventoriesTypesForm(forms.ModelForm):
    class Meta:
        model = InventoriesTypes
        fields = ('type', 'name')
        widgets = {
            "type": forms.Select(attrs={'placeholder': 'enter inventry_type', 'class': 'form-control'}),
            "name": forms.TextInput(attrs={'placeholder': 'enter inventories_type name', 'class': 'form-control'})

        }
