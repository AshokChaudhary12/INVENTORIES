from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from my_app.models import User, Inventories, InventoriesTypes


class UserForm(UserCreationForm):
    password1 = forms.CharField(error_messages={'required': 'enter a valid user password'},
                                widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(error_messages={'required': 'enter a valid user password'},
                                widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))

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


class InventoriesForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Inventories
        fields = ('inventry_type', 'name', 'quantity', 'purchase_date')
        widgets = {
            "inventry_type": forms.Select(attrs={'placeholder': 'enter inventry_type', 'class': 'form-control'}),
            "name": forms.TextInput(attrs={'placeholder': 'Enter name', 'class': 'form-control'}),
            "quantity": forms.TextInput(attrs={'placeholder': 'Enter quantity', 'class': 'form-control'}),
            "purchase_date": forms.DateInput(
                attrs={'placeholder': 'Enter purchase date', 'class': 'form-control', 'type': 'Date'}),
        }

    def __init__(self, **kwargs):
        type = kwargs.pop('type', None)
        super(InventoriesForm, self).__init__(**kwargs)
        if type:
            self.fields['inventry_type'].queryset = InventoriesTypes.objects.filter(type=type)


class InventoriesTypesForm(forms.ModelForm):
    class Meta:
        model = InventoriesTypes
        fields = ('type', 'name')
        widgets = {
            "type": forms.Select(attrs={'placeholder': 'enter inventry_type', 'class': 'form-control'}),
            "name": forms.TextInput(attrs={'placeholder': 'enter inventories_type name', 'class': 'form-control'})

        }
