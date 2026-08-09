from django.db import models
from django.contrib.auth.models import User
from .constrants import account_choice,Gender_Type
# Create your models here.


class UserBank_account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="UserBank_account")
    account_type=models.CharField(max_length=100,choices=account_choice)
    account_no=models.IntegerField(unique=True)
    birth_date=models.DateField()
    gender=models.CharField(max_length=20,choices=Gender_Type)
    intitial_deposit=models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(default=0.0,max_digits=12,decimal_places=2)

    def __str__(self):
        return f"{self.account_no}"

class User_address(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=120)
    city=models.CharField(max_length=100)
    postal=models.CharField(max_length=5)
    country=models.CharField(max_length=140)

