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
            my_user = super.save(commit=False)
            

            if commit == True :
                my_user.save()
                acc_type=self.cleanded_data['account_type']
                gender=self.cleanded_data['gender']; 
                birth=self.cleanded_data['birth_date']
                street_address = self.cleanded_data['street_address']
                city=self.cleanded_data['city']
                postal=self.cleanded_data['postal']
                country=self.cleanded_data['country']


                UserBank_account.objects.create(
                    user=my_user,
                    account_type=acc_type,
                    birth_date=birth,
                    gender=gender,
                    account_no=2310 + my_user.id
                )

                User_address.objects.create(
                    user=my_user,
                    street_address=street,
                    city=city,
                    postal=postal,
                    country=country
                )
            return my_user

        



