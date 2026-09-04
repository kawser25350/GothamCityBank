from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .constrants import account_choice,Gender_Type
from .models import UserBank_account,User_address

class RegisterForm(UserCreationForm):
    
    account_type=forms.ChoiceField(choices=account_choice)
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'})); 
    gender=forms.ChoiceField(choices=Gender_Type)

    street_address=forms.CharField(max_length=120)
    city=forms.CharField(max_length=100)
    postal=forms.CharField(max_length=5)
    country=forms.CharField(max_length=140)

    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2","account_type","gender","birth_date","street_address","city","postal","country"]

    def save(self,commit=True):
        my_user = super().save(commit=False)

        if commit:
            my_user.save()
            UserBank_account.objects.create(
                user=my_user,
                account_type=self.cleaned_data['account_type'],
                birth_date=self.cleaned_data['birth_date'],
                gender=self.cleaned_data['gender'],
                account_no=2310 + my_user.id
            )
            User_address.objects.create(
                user=my_user,
                street_address=self.cleaned_data['street_address'],
                city=self.cleaned_data['city'],
                postal=self.cleaned_data['postal'],
                country=self.cleaned_data['country']
            )
        return my_user


class UserChangeForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=account_choice)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=Gender_Type)
    street_address = forms.CharField(max_length=120)
    city = forms.CharField(max_length=100)
    postal = forms.CharField(max_length=5)
    country = forms.CharField(max_length=140)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'account_type',
            'gender', 'birth_date', 'street_address', 'city', 'postal', 'country',
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        self.address = kwargs.pop('address')
        super().__init__(*args, **kwargs)
        self.fields['account_type'].initial = self.account.account_type
        self.fields['birth_date'].initial = self.account.birth_date
        self.fields['gender'].initial = self.account.gender
        self.fields['street_address'].initial = self.address.street_address
        self.fields['city'].initial = self.address.city
        self.fields['postal'].initial = self.address.postal
        self.fields['country'].initial = self.address.country

    def save(self, commit=True):
        user = super().save(commit=commit)
        self.account.account_type = self.cleaned_data['account_type']
        self.account.birth_date = self.cleaned_data['birth_date']
        self.account.gender = self.cleaned_data['gender']
        self.address.street_address = self.cleaned_data['street_address']
        self.address.city = self.cleaned_data['city']
        self.address.postal = self.cleaned_data['postal']
        self.address.country = self.cleaned_data['country']

        if commit:
            self.account.save(update_fields=['account_type', 'birth_date', 'gender'])
            self.address.save(update_fields=['street_address', 'city', 'postal', 'country'])
        return user





