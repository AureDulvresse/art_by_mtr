from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Customer
from accounts.forms import LoginForm, RegisterForm




def login_page(request) -> HttpResponse:

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
        
            try:
                user = form.get_user()
                login(request, user)
                return redirect("store:home")
            except:
                form.add_error(None, "Identifiant ou mot de passe incorrect")
                messages.error(request, "Identifiant ou mot de passe incorrect")
                
        else:

            print(form, form.errors)
    else:
        form = LoginForm()

    return render(request, "accounts/pages/login.html", {'form': form})

@login_required
def logout_page(request) -> HttpResponse:
    logout(request)
    return redirect("store:home")


def register_page(request) -> HttpResponse:

    if request.method == "POST":
        form = RegisterForm(request.POST)


        if form.is_valid():

            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            pwd = form.cleaned_data.get("password")
            
            Customer.objects.create_user(
                username = username,
                email = email,
                first_name = first_name,
                last_name = last_name, 
                password=pwd
            )
            
            request.POST = {}

            messages.info(request, "Inscription réussit")

            return redirect("accounts:login")
        
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    
    return render(request, "accounts/register.html", {"form": form})

@login_required
def show(request) -> HttpResponse:
    return render(request, "accounts/profile.html", {})

@login_required
def update(request) -> HttpResponse:
    
    if request.method == "POST":
        form = request.POST
        first_name = form.get("first_name")
        last_name = form.get("last_name")
        username = form.get("username")
        email = form.get("email")

        user = get_object_or_404(Customer, pk = request.user.pk)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect("accounts:profile")


@login_required
def destroy(request) -> HttpResponse:

    Customer = get_object_or_404(Customer, pk = request.user.pk)
    logout(request)
    Customer.delete()

    return redirect("chat:home")
    