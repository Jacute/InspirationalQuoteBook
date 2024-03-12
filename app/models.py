from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=256, unique=True)
    email = models.EmailField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'username'
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return f'CustomUser(username={self.username}, email={self.email})'


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    requested_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'password_reset'
    
    def __str__(self):
        return f'PasswordResetRequest(user={self.user.username}, token={self.token}, requested_at={self.requested_at})'
    
    def isExpired(self):
        expirationTime = self.requested_at + timezone.timedelta(days=1)
        
        return timezone.now() > expirationTime


class Quote(models.Model):
    quote = models.TextField()
    quote_author = models.CharField(max_length=64)
    suggester_author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, default=None, null=True)
    status = models.IntegerField(default=2) # 0 - rejected, 1 - publicated, 2 - on moderation
    pub_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'quotes'
    
    def __str__(self):
        return f'Quote(quote={self.quote}, quote_author={self.quote_author}, suggester_author={self.suggester_author}, pub_date={self.pub_date})'


class Category(models.Model):
    category = models.CharField(max_length=64)
    
    class Meta:
        db_table = 'categories'
        
    def __str__(self):
        return f'Category(category={self.category})'


class QuoteCategory(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.SET_NULL, default=None, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=None, null=True)
    
    class Meta:
        db_table = 'quote_category'
    
    def __str__(self):
        return f'QuoteCategory(quote_id={self.quote}, category_id={self.category})'