# create functtion that will search for a restaurant by name
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import LoginForm, RegisterForm

from Restaurant_Recommendation_WebSite.models import Restaurant


#################### USER AUTHENTICATION ####################
def home(request):
    return render(request, 'index.html', {})


def auth(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                # handle login logic
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error_message = 'Invalid login credentials'
                    return render(request, '../templates/auth.html', {'error_message': error_message})
        elif form_type == 'register':
            form = RegisterForm(request.POST)
            if form.is_valid():
                # handle registration logic
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                password_confirm = request.POST['password_confirm']

                # Validate form data
                if password != password_confirm:
                    return render(request, '../templates/auth.html', {'error': 'Passwords do not match'})

                if User.objects.filter(username=username).exists():
                    return render(request, '../templates/auth.html', {'error': 'Username already exists'})

                if User.objects.filter(email=email).exists():
                    return render(request, '../templates/auth.html', {'error': 'Email already exists'})
                # Create new user
                User.objects.create_user(username=username, email=email, password=password)
    else:
        form_type = 'login'
        login_form = LoginForm()
        register_form = RegisterForm()

    return render(request, 'auth.html', {
        'form_type': form_type,
        'login_form': LoginForm,
        'register_form': RegisterForm,
    })


# def register(request):
#     if request.method == 'POST':
#         # Get form data
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password_confirm = request.POST['password_confirm']
#
#         # Validate form data
#         if password != password_confirm:
#             return render(request, '../templates/auth.html', {'error': 'Passwords do not match'})
#
#         if User.objects.filter(username=username).exists():
#             return render(request, '../templates/auth.html', {'error': 'Username already exists'})
#
#         if User.objects.filter(email=email).exists():
#             return render(request, '../templates/auth.html', {'error': 'Email already exists'})
#
#         # Create new user
#         User.objects.create_user(username=username, email=email, password=password)
#
#         return redirect('login')
#
#     return render(request, '../templates/auth.html')
#

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             error_message = 'Invalid login credentials'
#             return render(request, '../templates/auth.html', {'error_message': error_message})
#     else:
#         return render(request, '../templates/auth.html')


def user_logout(request):
    logout(request)
    return redirect('index')


#################### END USER AUTHENTICATION ####################

####################### RESTAURANT SEARCH #######################

def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    restaurants = Restaurant.objects.filter(name__contains=search_text)
    return render(request, 'index.html', {'restaurants': restaurants})
