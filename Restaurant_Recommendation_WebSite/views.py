from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from Restaurant_Recommendation_WebSite.forms import RegistrationForm, LoginForm
from Restaurant_Recommendation_WebSite.models import Restaurant, Users


#################### USER AUTHENTICATION ####################
def home(request):
    restaurants = Restaurant.objects.all()
    context = {'restaurants': list(restaurants)}
    return render(request, 'restaurants/home.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create a new user
            user = Users.objects.create(username=username, email=email, password=password)
            # Log the user in
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the URL name of your home page
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


#################### END USER AUTHENTICATION ####################

####################### RESTAURANT SEARCH #######################

def search(request, search_text):
    try:
        restaurants = Restaurant.objects.filter(name__contains=search_text)
    except Restaurant.DoesNotExist:
        error_message = 'No restaurants found matching your search criteria.'
        return render(request, 'restaurants/home.html', {'error_message': error_message})
    else:
        return render(request, 'restaurants/home.html', {'restaurants': restaurants})


# def restaurant_list(request):
#     restaurants = Restaurant.objects.all()
#     context = {'restaurants': restaurants}
#     return render(request, 'home.html', context)


def restaurant_details(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    context = {'restaurant': restaurant}
    return render(request, 'restaurants_details/restaurant_details.html', context)
