from .db import addQuotes

from os import environ
from dotenv import load_dotenv

import json
import re

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from django.db.models import Q

from django.middleware.csrf import get_token

"""from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity"""

from .models import Quote
from .db import addQuote


def jsonToDict(filename: str) -> dict:
    with open(f'app/uploads/{filename}', 'r') as f:
        data = json.load(f)
    
    return data


def loadBase():
    dct = jsonToDict('base.json')
    addQuotes(dct)


def validatePassword(password):
    errors = []

    if len(password) < 8:
        errors.append('Пароль должен содержать не менее 8 символов')
    if not re.match('.*[0-9].*', password):
        errors.append('Пароль должен содержать цифры')
    if not re.match('.*[a-z].*', password):
        errors.append('Пароль должен содержать буквы в нижнем регистре')
    if not re.match('.*[A-Z].*', password):
        errors.append('Пароль должен содержать буквы в верхнем регистре')

    return errors


def emailIsReal(email):
    
    # TODO: email checking
    
    return True


def validateEmail(email):
    errors = []
    
    if not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append('Электронная почта не соответствует формату')
    elif not emailIsReal(email):
        errors.append('Данная электронная почта не существует')
    
    return errors


def validateQuote(author, quote, categories):
    errors = []
    
    if not re.match(r'^[А-Яа-яЁё\. ]{8,}$', author):
        errors.append('Автор не соответствует правильному формату')
    if not re.match(r'^[А-Яа-яЁё\,\.\-\!\? ]{8,}$', quote):
        errors.append('Цитата не соответствует правильному формату')
    
    for categorie in categories:
        if not re.match(r'^[А-Яа-я]{3,}$', categorie):
            errors.append(f'Категория "{categorie}" не соответствует правильному формату')
    
    return errors
    


def sendResetEmail(email, reset_link):
    subject = 'Восстановление пароля'
    message = render_to_string('users/password_reset_email.html', {"reset_link": reset_link})
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def printResetEmail(reset_link):
    print(render_to_string('users/password_reset_email.html', {"reset_link": reset_link}))


def compareStrings(text1, text2):
    """vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])

    similarity = cosine_similarity(vectors)
    
    return similarity[0][1] * 100"""
    
    return 75


def repeatModeration(quote):
    quotes = Quote.objects.filter(Q(status=1) | Q(status=2)).values_list('quote', flat=True)
    
    for i in quotes:
        if compareStrings(quote, i) > 80:
            return False
    return True


def banwordModeration(author, quote, categories):
    if BANWORDS:
        for banword in BANWORDS:
            if banword in author or banword in quote or banword in ' '.join(categories):
                return False
    return True


def moderateQuote(author, quote, categories):
    if repeatModeration(quote) and banwordModeration(author, quote, categories):
        return True
    else:
        return False

try:
    with open('banwords.txt', 'r') as f:
        BANWORDS = f.read().split('\n')
except Exception:
    BANWORDS = None