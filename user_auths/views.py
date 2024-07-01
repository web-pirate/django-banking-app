from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from user_auths.models import User
from user_auths.forms import UserRegisterForm

def RegisterView(request):
    if request.method == "POST": 
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully.")
            new_user = authenticate(username = form.cleaned_data.get('email'), 
                                    password=form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect("core:index")
    elif request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("core:index")
    else:
        form = UserRegisterForm()
    context = {
        "signup_form": form
    }
    return render(request, "user_auths/sign-up.html", context)

def LoginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in successfully.")
                return redirect("core:index")
            else: 
                messages.warning(request, "Username or password is incorrect.")
                return redirect("user_auths:sign-in")
        except: 
                messages.warning(request, "User does not exist.")
    return render(request, "user_auths/sign-in.html")


def LogoutView(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("user_auths:sign-in")
