from django.shortcuts import render
from django.http import JsonResponse
from .models import CryptoPrice
import requests
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'index.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        try:
            User.objects.create_user(username=username, password=password)
            return redirect('login')  # Redirect to login page after successful signup
        except:
            return render(request, 'signup.html', {'error': 'Username already exists'})

    return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to home or another page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to home after logout

# Fetch data from API and display in the console
def fetch_api_data(request):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("API Data:", data)
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Failed to fetch data"}, status=500)

# Store API data (requires authentication)
@login_required
def store_data(request):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for crypto, details in data.items():
            price = details["usd"]
            CryptoPrice.objects.create(crypto_name=crypto, price=price, timestamp=datetime.now())
        print("Stored Data:", data)
        return JsonResponse({"message": "Data stored successfully!"})
    else:
        return JsonResponse({"error": "Failed to fetch data"}, status=500)

# Retrieve data (requires authentication)
@login_required
def retrieve_data(request):
    data = list(CryptoPrice.objects.values())
    print("Retrieved Data:", data)
    return JsonResponse(data, safe=False)
