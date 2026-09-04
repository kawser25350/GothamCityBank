from django import forms
from .models import Transaction

class  TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['ammount','transaction_type']

    def __init__(self,*args,**kwargs):
        self.account=kwargs.get('account')
        kwargs.pop('account', None)
        super().__init__(*args,**kwargs)
        self.fields['transaction_type'].disabled=True
        self.fields['transaction_type'].widget=forms.HiddenInput()
    
    def save(self,commit=True):
        self.instance.account=self.account
        self.instance.update_balance=self.account.balance 
        return super().save(commit=commit)

class DepositeForm(TransactionForm):

    def clean_ammount(self):
        ammount=self.cleaned_data.get('ammount')
        min_deposite_ammount=100
        if ammount < 100 :
            raise forms.ValidationError(
                f'min deposite is {min_deposite_ammount}$'
            )
        return ammount

class WithdrawForm(TransactionForm):

    def clean_ammount(self):
        ammount=self.cleaned_data.get('ammount')
        min_withdraw_ammount=100
        max_withdraw_ammount=1000000
        current_balance=self.account.balance

        if ammount < min_withdraw_ammount:
            raise forms.ValidationError(
                f'minimum withdrawl balance should be greater than {min_withdraw_ammount}$'
            )
        if ammount > max_withdraw_ammount:
            raise forms.ValidationError(
                f'maximum withdrawl balance should be less than {max_withdraw_ammount}$'
            )
        if ammount > current_balance:
            raise forms.ValidationError(
                f'Insufficient Blance.current balance is {current_balance}$'
            )
        return ammount

class LoanRequstForm(TransactionForm):

    def clean_ammount(self):
        ammount=self.cleaned_data.get('ammount')
        max_loan=10000
        if ammount >  max_loan:
            raise forms.ValidationError(
                f'you can maximum {max_loan}$ loan only'
            )
        return ammount

class TransferMoneyForm(TransactionForm):
    receiver_account_no = forms.IntegerField(required=True, label='Receiver account number')
    
    class Meta:
        model=Transaction
        fields=['ammount','transaction_type','receiver_account_no']

    def clean_receiver_account_no(self):
        receiver_account_no = self.cleaned_data.get('receiver_account_no')
        if receiver_account_no == self.account.account_no:
            raise forms.ValidationError('You cannot transfer money to your own account.')
        return receiver_account_no

    def clean_ammount(self):
        ammount=self.cleaned_data.get('ammount')
        current_balance=self.account.balance

        if ammount==0 or ammount > current_balance:
            raise forms.ValidationError(
                f'Insufficient Blanance,{current_balance} or transfer ammount is to low'
            )
        

        
        return ammount

