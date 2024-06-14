from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Customer


class AuthController:

    def login_page(request) -> HttpResponse:

        if request.method == "POST":
            identifiant = request.POST.get("username")
            pwd = request.POST.get("password")
            user = authenticate(request, username=identifiant, password=pwd)

            if user is not None:
                login(request, user)
                return redirect("store:home")
            else:
                messages.info(request, "Identifiant ou mot de passe incorrect")

        return render(request, "accounts/pages/login.html")

    @login_required
    def logout_page(request) -> HttpResponse:
        logout(request)
        return redirect("store:home")
	
	
    def register_page(request) -> HttpResponse:
		
        if request.method == "POST":
            form = request.POST
            first_name = form.get("first_name")
            last_name = form.get("last_name")
            username = form.get("username")
            email = form.get("email")
            pwd = request.POST.get("password")
			
            Customer.objects.create_user(
                username = username,
                email = email,
                first_name = first_name,
                last_name = last_name, 
                password=pwd
            )
			
            request.POST = {}

            return redirect("accounts:login")
		
        return render(request, "accounts/pages/register.html")


class UserController:

    @login_required
    def show(request) -> HttpResponse:

        context = {}

        return render(request, "accounts/pages/index.html", context)
    


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

            return redirect("accounts:myAccount")

    @login_required
    def destroy(request) -> HttpResponse:

        user = get_object_or_404(Customer, pk = request.user.pk)
        logout(request)
        user.delete()

        return redirect("store:home")