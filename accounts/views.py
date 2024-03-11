from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username=username, password=password)
        login(request, new_user)
        return redirect('index')
    return render(request, 'accounts/signup.html')


def login_user(request):
    error_msg = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        error_msg = True
    return render(request, 'accounts/login.html', {'error_msg': error_msg})


def logout_user(request):
    logout(request)
    return redirect('index')
