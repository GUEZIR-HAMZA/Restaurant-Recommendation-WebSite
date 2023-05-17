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


# def register_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             # Create a new user
#             user = Users.objects.create(username=username, email=email, password=password)
#             # Log the user in
#             login(request, user)
#             return redirect('home')  # Replace 'home' with the URL name of your home page
#     else:
#         form = RegistrationForm()
#     return render(request, 'auth/register.html', {'form': form})
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')
            elif Users.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')
            else:
                user = Users.objects.create(username=username, email=email, password=password)
                login(request, user)
                return redirect('home')
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
                return redirect('home')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


#################### END USER AUTHENTICATION ####################

####################### RESTAURANT SEARCH #######################


def search_view(request):
    search_text = request.GET.get('q', '')  # Retrieve the search term from the request

    try:
        restaurants = Restaurant.objects.filter(
            name__icontains=search_text)  # Perform case-insensitive search for restaurants matching the name
    except Restaurant.DoesNotExist:
        error_message = 'No restaurants found matching your search criteria.'
        return render(request, 'restaurants/home.html', {'error_message': error_message})
    else:
        return render(request, 'restaurants/home.html', {'restaurants': restaurants})


#################### END RESTAURANT SEARCH ####################

#################### RESTAURANT DETAILS ####################

def restaurant_details(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    context = {'restaurant': restaurant}
    return render(request, 'restaurants_details/restaurant_details.html', context)


def add_review(request, restaurant_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        user = request.user
        restaurant.reviews.create(user=user, rating=rating, comment=comment)
        return redirect('restaurant_details', restaurant_id=restaurant_id)
    return render(request, 'restaurants_details/add_review.html')


#################### END RESTAURANT DETAILS ####################
