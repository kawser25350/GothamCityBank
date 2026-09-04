from decimal import Decimal

from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserBank_account
from .admin import TransactionAdmin
from .models import Transaction


class LoanApprovalAdminTests(TestCase):
	def setUp(self):
		user = User.objects.create_user(username='loan-user', password='password')
		self.account = UserBank_account.objects.create(
			user=user,
			account_type='Savings',
			account_no=123456,
			birth_date='1990-01-01',
			gender='Male',
			balance=Decimal('100.00'),
		)
		self.transaction_admin = TransactionAdmin(Transaction, admin.site)

	def test_approval_credits_account_once(self):
		loan = Transaction.objects.create(
			account=self.account,
			ammount=50,
			update_balance=self.account.balance,
			transaction_type='Loan',
		)

		self.transaction_admin.save_model(None, loan, None, True)
		self.account.refresh_from_db()
		self.assertEqual(self.account.balance, Decimal('100.00'))

		loan.approval = True
		self.transaction_admin.save_model(None, loan, None, True)
		self.account.refresh_from_db()
		loan.refresh_from_db()
		self.assertEqual(self.account.balance, Decimal('150.00'))
		self.assertEqual(loan.update_balance, Decimal('150.00'))

		self.transaction_admin.save_model(None, loan, None, True)
		self.account.refresh_from_db()
		self.assertEqual(self.account.balance, Decimal('150.00'))
