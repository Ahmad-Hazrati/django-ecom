from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserProfileForm, ChangePasswordForm, UserInfoForm
from django import forms 
from django.db.models import Q


def category(request, cat):
    # Replace hyphens with spaces
    cat = cat.replace('-', ' ')
    # Grab the category from the url
    try:
        # Lookup the category
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    
    except:
        messages.success(request, ("The requested catogory doesn't exist."))
        return redirect('home')
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about (request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in successfully"))
            return redirect('home')
        else:
            messages.error(request, ("Whoops! Seems there was occurred an error, please try again."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out successfully."))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Account has been created successfully. Please fill out your user information."))
            return redirect('update_info')
        else:
            messages.error(request, ("Whoops! Seems there was occurred an error, please try again."))
            return redirect('register')
    else :
        return render(request, 'register.html', {'form':form})

def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_form = UserProfileForm(request.POST or None, instance=current_user)
        
        if profile_form.is_valid():
            profile_form.save()
            
            login(request, current_user)
            messages.success(request, "You have updated your profile successfully!")
            return redirect('home')
        return render(request, "update_profile.html", {'profile_form': profile_form})
    
    else:
        messages.success(request, "You must be login to update your profile!")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user 
        # Did the user fill out the form
        if request.method == 'POST':
             form = ChangePasswordForm(current_user, request.POST)
             # Is the form valid
             if form.is_valid():
                 form.save()
                 messages.success(request, "Your password has been updated successfully. Please login again.")
                 return redirect('login')
             else:
                 for error in list(form.errors.values()):
                     messages.error(request, error)
             
        else:
            form = ChangePasswordForm(current_user)
    else:
        messages.success(request, "You must be login to change your passord.")
        
    return render(request, 'update_password.html', {'form': form})


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, "Your Info has been updated successfully!")
            return redirect('home')
        return render(request, "update_info.html", {'form': form})
    
    else:
        messages.success(request, "You must be login to update your profile!")
        return redirect('home')
    
    
def search(request):
    # Determin if the form is filled
    if request.method == 'POST':
        searched = request.POST['search']
        # Query the products database model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # If search result is null
        if not searched:
            messages.success(request, "The item searched is not found.")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {})