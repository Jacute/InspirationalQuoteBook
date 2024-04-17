from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout as logoutUser, login as loginUser
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from app.models import CustomUser, PasswordResetRequest
from app.db import getQuotes, getRandomQuotes, getCategories, getAuthors, addQuote
from app.utils import validatePassword, validateEmail, validateQuote, \
    printResetEmail, sendResetEmail, moderateQuote

import re
import json


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


@login_required
def my_quotes(request: HttpRequest) -> HttpResponse:
    return render(request, 'my_quotes.html')


@login_required
def add_quote(request: HttpRequest) -> HttpResponse:
    return render(request, 'add_quote.html')


def login(request: HttpRequest) -> HttpResponse:
    errors = []
    username = None
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None
        if user and user.check_password(password):
            loginUser(request, user)
            return redirect('/')
        else:
            errors.append('Неправильный логин или пароль')
        
    return render(request, 'users/login.html', {'errors': errors, 'username': username})


def logout(request: HttpRequest) -> HttpResponse:
    logoutUser(request)
    return redirect('/')


def register(request: HttpRequest) -> HttpResponse:
    errors = []
    username, email = None, None
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        registerPossibility = True
        
        validateErrors = validatePassword(password) + validateEmail(email)
        if validateErrors:
            errors.extend(validateErrors)
            registerPossibility = False
        if password != confirm_password:
            errors.append("Пароли не совпадают")
            registerPossibility = False
        if CustomUser.objects.filter(username=username).exists():
            errors.append("Пользователь с данным именем уже существует")
            username = None
            registerPossibility = False
        if CustomUser.objects.filter(email=email).exists():
            errors.append("Пользователь с данной электронной почтой уже существует")
            email = None
            registerPossibility = False
        
        
        if registerPossibility:
            user = CustomUser.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            
            loginUser(request, user)
            
            return redirect('/')
    
    return render(request, 'users/register.html', {'errors': errors, 'username': username, 'email': email})


def password_reset(request: HttpRequest):
    errors = []
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            errors.append('Пользователь с данным адресом электронной почты отсутствует')
        else:
            token = get_random_string(64)
            PasswordResetRequest.objects.create(user=user, token=token)
            
            protocol = request.scheme
            hostname = request.get_host()
            
            reset_link = f"{protocol}://{hostname}/password_reset_confirm/{token}"
            
            if settings.DEBUG:
                printResetEmail(reset_link)
            else:
                sendResetEmail(email, reset_link)
            
            return render(request, 'users/password_reset_done.html')
            
    return render(request, 'users/password_reset_form.html', {'errors': errors})


def password_reset_confirm(request, token: str):
    errors = []
    
    try:
        reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        return render(request, 'errors/404.html', status=404)
    
    if reset_request.isExpired():
        reset_request.delete()
        return render(request, 'users/password_reset_expired.html')
    
    if request.method == 'POST':
        changePasswordPossibility = True
        
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        errors.extend(validatePassword(password))
        if errors:
            changePasswordPossibility = False
        if password != confirm_password:
            errors.append("Пароли не совпадают")
            changePasswordPossibility = False
            
        if changePasswordPossibility:
            
            user = reset_request.user
            user.set_password(password)
            user.save()
            
            loginUser(request, user)
            reset_request.delete()
            
            return render(request, 'users/password_reset_complete.html')
    return render(request, 'users/password_reset_confirm.html', {"errors": errors})


@csrf_exempt
def api_get(request: HttpRequest, table: str, quote_type: str) -> JsonResponse:
    data = {}
    
    if request.method == 'GET':
        if table == 'quotes':
            
            category = request.GET.get('category') or ''
            author = request.GET.get('author') or ''
            query = request.GET.get('query') or ''
            
            if quote_type == 'authors':
                data['status'] = 'OK'
                data['data'] = getAuthors(category)
            elif quote_type == 'categories':
                data['status'] = 'OK'
                data['data'] = getCategories(author)
            elif quote_type == 'query':
                data['status'] = 'OK'
                data['data'] = getQuotes(author, category, query)
            elif quote_type == 'my':
                suggesterAuthor = request.user.username
                data['data'] = getQuotes(suggesterAuthor=suggesterAuthor, isPub=False)
            else:
                data['status'] = 'BAD'
    else:
        data['status'] = 'UNKNOWN METHOD'
    return JsonResponse(data, safe=False)


@csrf_exempt
def api_put(request: HttpRequest, table: str) -> JsonResponse:
    if request.method == 'PUT':
        if table == 'quotes':
            try:
                record = json.loads(request.body.decode())
                
                author = record['author']
                quote = record['quote']
                categories = [i.lower() for i in record['categories']]
                
                if not author or not quote or not categories:
                    raise Exception()

            except Exception as e:
                return JsonResponse({'status': 'BAD', 'errors': ['Некорректный запрос']}, safe=False)
            
            errors = validateQuote(author, quote, categories)
            
            if errors:
                return JsonResponse({'status': 'BAD', 'errors': errors}, safe=False)
            
            if not settings.DEBUG and moderateQuote(author.lower(), quote.lower(), categories):
                try:
                    record = {
                        'quote': quote,
                        'quoteAuthor': author,
                        'suggesterAuthor': request.user,
                        'categories': categories
                    }
                    addQuote(record, True)
                except Exception as e:
                    print("Error:", e)
                return JsonResponse({'status': 'OK'}, safe=False)
            elif settings.DEBUG:
                try:
                    record = {
                        'quote': quote,
                        'quoteAuthor': author,
                        'suggesterAuthor': request.user,
                        'categories': categories
                    }
                    addQuote(record, True)
                except Exception as e:
                    print("Error:", e)
                return JsonResponse({'status': 'OK'}, safe=False)
            return JsonResponse({'status': 'BAD', 'errors': ['Ваша цитата не прошла модерацию']}, safe=False)
        
        return JsonResponse({'status': 'UNKNOWN TABLE'}, safe=False)
    
    return JsonResponse({'status': 'UNKNOWN METHOD'}, safe=False)