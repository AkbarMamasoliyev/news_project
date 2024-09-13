from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('<h2>Tizimga kirildi')
                else:
                    return HttpResponse('<h2>Bu foydalanuvhi active holatda emas')
            else:
                return HttpResponse('<h2>Username yoki parol xato')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def user_profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile/user_profile.html', context)
