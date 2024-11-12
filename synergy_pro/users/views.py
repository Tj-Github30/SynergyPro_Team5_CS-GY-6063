from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # Automatically log the user in after signup
            print(f"User {user.username} created and logged in.")  # Debug line
            messages.success(request, "Account created successfully!")
            return redirect('users/registration/login.html')  # Redirect to the homepage after signup
    else:
        form = UserRegisterForm()
    return render(request, 'users/registration/signup.html', {'form': form})
