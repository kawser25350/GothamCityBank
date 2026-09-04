from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView,View
from accounts.models import UserBank_account
from .models import Transaction
from django.urls import reverse_lazy
from .forms import DepositeForm,WithdrawForm,LoanRequstForm,TransferMoneyForm
from .models import Transaction
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import UserBank_account
from datetime import datetime
from django.db import transaction as db_transaction

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.

def transaction_email(user,ammount,mail_type):
    subject = f'GothamCity Bank - {mail_type} confirmation'
    
    context = {
        'user': user,
        'ammount': ammount,
        'subject': mail_type,
    }
    
    html_message = render_to_string(
        'transactions/transaction_messages.html',
        context,
    )

    send_email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(html_message),
        from_email=settings.MAILERS['default']['OPTIONS']['username'],
        to=[user.email],
    )

    send_email.attach_alternative(html_message, 'text/html')
    send_email.send()


class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    model=Transaction
    template_name='transactions/transactions.html'
    success_url=reverse_lazy('home')
    title=' '

    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            request.user.account
        except UserBank_account.DoesNotExist:
            messages.error(request,'Your user has no bank account. Please create a complete account first.')
            return redirect('home')
        return super().dispatch(request,*args,**kwargs)

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']=self.title
        return context

class DepositeView(TransactionCreateMixin):
    form_class=DepositeForm
    title='Deposit'

    def get_initial(self):
        initial = {'transaction_type':'Deposite'}
        return initial
    
    def form_valid(self,form):
        ammount=form.cleaned_data.get('ammount')
        account=self.request.user.account
        account.balance+=ammount
        account.save(update_fields=['balance'])

        messages.success(self.request,f"{ammount}$ Deposite Successfull.")
        transaction_email(self.request.user,ammount,"Deposite")
        return super().form_valid(form)

class WithdrawView(TransactionCreateMixin):
    form_class=WithdrawForm
    title='Withdraw'

    def get_initial(self):
        initial = {'transaction_type':'Withdraw'}
        return initial
    
    def form_valid(self,form):
        ammount=form.cleaned_data.get('ammount')
        account=self.request.user.account
        account.balance-=ammount
        account.save(update_fields=['balance'])

        messages.success(self.request,f"{ammount}$ Withdraw Successfull.")
        transaction_email(self.request.user,ammount,"Withdraw")
        return super().form_valid(form)

class LoanRequstView(TransactionCreateMixin):
    form_class=LoanRequstForm
    title='Loan'

    def get_initial(self):
        initial = {'transaction_type':'Loan'}
        return initial
    
    def form_valid(self,form):
        ammount=form.cleaned_data.get('ammount')
        current_taken_loan=Transaction.objects.filter(account=self.request.user.account,transaction_type='Loan',approval=True,paid=False).count()

        if current_taken_loan >= 3:
            return HttpResponse('you have already taken 3 loan.currenlty you are not eligible.')

        messages.success(self.request,f"{ammount}$ Loan Request Successfull.")
        transaction_email(self.request.user,ammount,"Loan Request")
        return super().form_valid(form)

class TransferMoneyView(TransactionCreateMixin):

    form_class=TransferMoneyForm
    title='Transfer money'

    def get_initial(self):
        initial = {'transaction_type':'TransferMoney'}
        return initial

    def form_valid(self,form):
        ammount=form.cleaned_data['ammount']
        receiver_account_no=form.cleaned_data['receiver_account_no']
        account=self.request.user.account
        
        
        try:
            receiver_account = UserBank_account.objects.get(account_no=receiver_account_no)
            
            receiver_account.balance+=ammount
            account.balance-=ammount

            receiver_account.save(update_fields=['balance'])
            account.save(update_fields=['balance'])

        except UserBank_account.DoesNotExist:
            form.add_error('receiver_account_no', 'Receiver account does not exist.')
            return self.form_invalid(form)

        form.instance.receiver_account_no = receiver_account_no
        messages.success(self.request, f"${ammount} transfer successful.")
        transaction_email(self.request.user,ammount,"Transfer Money")
        return super().form_valid(form)

class TransactionReportView(LoginRequiredMixin,ListView):
    model=Transaction
    template_name='transactions/transactions_report.html'
    context_object_name='reports'
    
    def get_queryset(self):
        queryset=super().get_queryset()

        trans=Transaction.objects.filter(account=self.request.user.account)

        start_time=self.request.GET.get('start_time')
        end_time=self.request.GET.get('end_time')
        transaction_type=self.request.GET.get('transaction_type')
        if start_time and end_time:
            start_time=datetime.strptime(start_time, '%Y-%m-%d').date()
            end_time=datetime.strptime(end_time, '%Y-%m-%d').date()
            trans=trans.filter(timestamp__date__gte=start_time,timestamp__date__lte=end_time)

        if transaction_type:
            trans=trans.filter(transaction_type=transaction_type)

        return trans

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_time'] = self.request.GET.get('start_time', '')
        context['end_time'] = self.request.GET.get('end_time', '')
        context['transaction_type'] = self.request.GET.get('transaction_type', '')
        context['transaction_types'] = Transaction._meta.get_field('transaction_type').choices
        return context


class LoanPaymentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        with db_transaction.atomic():
            loan = get_object_or_404(
                Transaction.objects.select_for_update(),
                pk=pk,
                account=request.user.account,
                transaction_type='Loan',
            )
            account = request.user.account

            if not loan.approval:
                messages.error(request, 'This loan has not been approved yet.')
            elif loan.paid:
                messages.info(request, 'This loan has already been paid.')
            elif loan.ammount > account.balance:
                messages.error(request, 'Insufficient balance to pay this loan.')
            else:
                account.balance -= loan.ammount
                account.save(update_fields=['balance'])
                loan.paid = True
                loan.save(update_fields=['paid'])
                messages.success(request, f'${loan.ammount} loan payment successful.')

        return redirect('transaction_report')


