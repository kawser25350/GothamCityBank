from django.db import models
from accounts.models import UserBank_account
from .constrants import transaction_type
from django.contrib.auth.models import User
# Create your models here.
class Transaction(models.Model):
    account=models.ForeignKey(UserBank_account,on_delete=models.CASCADE,related_name='account')
    ammount=models.IntegerField()
    update_balance=models.DecimalField(decimal_places=2,max_digits=12)
    transaction_type=models.CharField(max_length=100,choices=transaction_type)
    receiver_account_no=models.IntegerField(null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    approval=models.BooleanField(default=False)
    paid=models.BooleanField(default=False)

    class Meta:
        ordering=['timestamp']

    def __str__(self):
        return f"{self.transaction_type} - {self.ammount}"