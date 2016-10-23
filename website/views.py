from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

from .forms import RegistrationForm
from exams.models import Class


def home(request):
    return render(request, 'website/home.html')


def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            login(request, User.objects.latest('id'))

            return redirect('website:profile')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def profile(request):
    return render(request, 'registration/profile.html')
