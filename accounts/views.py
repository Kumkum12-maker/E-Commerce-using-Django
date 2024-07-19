from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import Customer

def user_Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # email = request.POST.get('email')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.info(request, "username or password not valid, please try again...")
            
    return render(request, 'accounts/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone_field')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken...")
                return redirect('user_register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken...")
                return redirect('user_register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                data = Customer(user=user, phone_field=phone)
                data.save()
                our_user = authenticate(username=username, password=password)
                if our_user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            messages.info(request, "Password didn't match, please try again...")
            return render(request, 'accounts/register.html')
    else:
        return render(request, 'accounts/register.html')

def user_Logout(request):
    logout(request)
    return redirect('/')
