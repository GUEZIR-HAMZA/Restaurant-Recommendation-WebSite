import http.client

from django.contrib import messages
from django.contrib.auth import login, logout
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

            try:
                user = Users.objects.get(username=username)
                messages.error(request, 'Username already exists.', extra_tags='danger')
                return redirect('register')
            except Users.DoesNotExist:
                pass

            try:
                user = Users.objects.get(email=email)
                messages.error(request, 'Email already exists.', extra_tags='danger')
                return redirect('register')
            except Users.DoesNotExist:
                pass

            # user = Users.objects.create(username=username, email=email, password=password)
            # login(request, user)
            messages.success(request, 'Account created successfully.', extra_tags='success')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Users.objects.get(username=username, password=password)
        except Users.DoesNotExist:
            user = None

        if user is not None:
            request.session['user_id'] = user.id
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username and/or password.', extra_tags='danger')
            return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    request.session.clear()  # Clear the session data
    return redirect('home')


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
