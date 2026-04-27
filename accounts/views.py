from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .forms import RegisterForm, LoginForm, EditForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = RegisterForm()
        
    return render(request, "accounts/register.html", context={"form": form})

class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy('accounts:login')
    
    def get_object(self, queryset=None):
        return self.request.user


@login_required(login_url="/accounts/login/")
def profile(request):
    return render(request, "accounts/profile.html")

class CustomLoginView(LoginView):
    model = User
    form_class = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:profile')
    
