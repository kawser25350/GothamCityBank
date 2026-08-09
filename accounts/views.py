from django.shortcuts import render
from django.views.generic  import CreateView
from .forms import RegisterForm
# Create your views here.

class UserRegisterView(CreateView):
    form_class=RegisterForm
    template_name='accounts/register.html'
    context_object_name='reg_form'
    success_url='home'
