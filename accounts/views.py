from django.shortcuts import render,redirect
from django.views.generic  import CreateView,FormView
from django.contrib.auth.views import LoginView,LogoutView
from .forms import RegisterForm
from django.urls import reverse_lazy
# Create your views here.

class UserRegisterView(CreateView):
    form_class=RegisterForm
    template_name='accounts/register.html'
    context_object_name='reg_form'
    success_url= reverse_lazy('home')

    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request,*args,**kwargs)

class UserLoginView(LoginView):
    template_name='accounts/login.html'
    next_page='home'

    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request,*args,**kwargs)

class ProfileView(FormView):
    template_name='accounts/profile.html'
    form_class=RegisterForm
    success_url=reverse_lazy('profile')

    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
