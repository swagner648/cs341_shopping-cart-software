from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Customer


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            customer = Customer()
            customer.User = request.user
            customer.Address = form.cleaned_data.get('Address')
            customer.City = form.cleaned_data.get('City')
            customer.State = form.cleaned_data.get('State')
            customer.ZIP = form.cleaned_data.get('ZIP')
            customer.save()
            return redirect('home:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
