from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.db.models import Count

import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def register(self, postData):
        errors = []
        # VALIDATE FIRST NAME
        if len(postData['first_name']) < 1:
            errors.append('First name cannot be empty.')
        elif len(postData['first_name']) <= 2:
            errors.append('First name must be at least two characters.')
        # VALIDATE LAST NAME
        if len(postData['last_name']) < 1:
            errors.append('Last name cannot be empty.')
        elif len(postData['last_name']) <= 2:
            errors.append('Last name must be at least two characters.')
        # VALIDATE EMAIL
        if len(postData['email']) < 1:
            errors.append('Email cannot be empty')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Email address must be valid.")
        else:
            try:
                user = User.objects.get(email=postData['email'])
            except MultipleObjectsReturned:
                errors.append("Email address has already been registered.")
            except:
                pass
        # VALIDATE PASSWORD
        if len(postData['password']) < 1:
            errors.append("Password cannot be empty.")
        elif len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters.")
        # VALIDATE PASSWORD CONFIRMATION
        if postData['password'] != postData['password_conf']:
            errors.append("Passwords must match.")

        if len(errors) > 0:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()) # creates hashed password to be saved in db
            new_user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed)
            print 'the new user is', new_user
            return (True, new_user.id, new_user.first_name)

    def login(self, postData):
        errors = []
        # VALIDATE EMAIL
        if len(postData['email']) < 1:
            errors.append('Email cannot be empty')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Email address must be valid.")
        # VALIDATE PASSWORD
        if len(postData['password']) < 1:
            errors.append("Password cannot be empty.")
        elif len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters.")

        if len(errors) > 0:
            return (False, errors)
        else:
            try:
                user = User.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors.append("Email or password is invalid. (email not found)")
                return (False, errors)
            except MultipleObjectsReturned:
                errors.append("Email or password is invalid. (more than one entry with that email)")
                return (False, errors)
            if user.password == bcrypt.hashpw(postData['password'].encode(), user.password.encode()):
                return (True, user.id, user.first_name)
            else:
                errors.append("Email or password is invalid. (password doesn't match)")
                return (False, errors)

    def get_favorites(self, postData):
        this_user = User.objects.get(id=postData.session['id'])
        this_users_favorites = this_user.favorite_quotes.all().values_list('id', flat=True)
        return (True, this_users_favorites)

    def get_contributions(self, postData, id):
        this_user = User.objects.get(id=id)
        this_users_contributions = this_user.my_contributions.all().annotate(Count('user_contributor'))
        return (True, this_users_contributions)

    def get_contributions_count(self, postData, user_id):
        this_user = User.objects.get(id=user_id)
        this_users_contributions = this_user.my_contributions.all().values_list('id', flat=True)
        return (True, this_users_contributions)

class QuoteManager(models.Manager):
    def get_quotes(self, postData):
        quotes = Quote.objects.order_by('-created_at').exclude(favorites__id = postData.session['id'])
        return (True, quotes)

    def get_favorites(self, postData):
        favorites = Quote.objects.order_by('-created_at').filter(favorites__id = postData.session['id'])
        return (True, favorites)

    def create_quote(self, postData):
        errors=[]

        # VALIDATE QUOTE
        if len(postData.POST['author']) < 1:
            errors.append('Author cannot be empty.')
            return (False, errors)

        # VALIDATE AUTHOR
        if len(postData.POST['quote']) < 1:
            errors.append('Quote cannot be empty.')
            return (False, errors)

        this_user = User.objects.get(id=postData.session['id'])
        quote = Quote.objects.create(quote=postData.POST['quote'], author=postData.POST['author'], user_contributor=this_user)
        return (True, quote)

    def create_favorite(self, postData, quote_id):
        this_quote = Quote.objects.get(id=quote_id)
        this_user = User.objects.get(id=postData.session['id'])
        this_quote.favorites.add(this_user)
        return (True)

    def remove_favorite(self, postData, quote_id):
        this_quote = Quote.objects.get(id=quote_id)
        this_user = User.objects.get(id=postData.session['id'])
        this_quote.favorites.remove(this_user)
        return (True)

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.first_name
    objects = UserManager()

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=90)
    user_contributor = models.ForeignKey(User, related_name="my_contributions")
    favorites = models.ManyToManyField(User, related_name="favorite_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.quote
    objects = QuoteManager()
