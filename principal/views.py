from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('mainPage')

class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('mainPage')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
         return redirect('mainPage')
        return super(RegisterPage, self).get(*args, **kwargs)
     
class mainPage(View, LoginRequiredMixin):
    template_name = 'mainPage.html'

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return render(request, self.template_name, {})