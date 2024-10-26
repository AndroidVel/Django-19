from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *


def main_page(request):
    return render(request, 'main_page.html')


def shop(request):
    games = Game.objects.all()
    context = {
        'games': games
    }
    return render(request, 'shop.html', context)


def cart(request):
    return render(request, 'cart.html')


def fill_inputs(dict_, username, password, repeat_password, age):
    dict_['username'] = username
    dict_['password'] = password
    dict_['repeat_password'] = repeat_password
    dict_['age'] = int(age)


def sign_up_by_django(request):
    info = {'error': '', 'username': '', 'password': '', 'repeat_password': '', 'age': 0}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        info['form'] = form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
                fill_inputs(info, username, password, repeat_password, age)
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18'
                fill_inputs(info, username, password, repeat_password, age)
            elif Buyer.objects.filter(name=username):
                info['error'] = 'Пользователь уже существует'
                fill_inputs(info, username, password, repeat_password, age)
            else:
                Buyer.objects.create(name=username, age=age, balance=0)
                return HttpResponse(f'Приветствуем, {username}!')
        else:
            form = UserRegister()
    return render(request, 'registration_page.html', info)
