from django.contrib import admin
from django.db import transaction
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=['account','ammount','update_balance','transaction_type','approval']

    def save_model(self,request,obj,form,change):
        old_approval = False
        if change:
            old_approval = Transaction.objects.get(pk=obj.pk).approval

        with transaction.atomic():
            super().save_model(request,obj,form,change)

            if obj.approval and obj.transaction_type == 'Loan' and not old_approval:
                obj.account.balance += obj.ammount
                obj.account.save(update_fields=['balance'])
                obj.update_balance = obj.account.balance
                obj.save(update_fields=['update_balance'])






