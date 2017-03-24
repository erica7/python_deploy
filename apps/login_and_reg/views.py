from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages

# INCOMPLETE: ADD ALIAS AND BIRTHDAY
# Login and Registration with validations. Validation errors should appear on the page. Logout feature.

# COMPLETE
# Display of quotes on Quotable Quotes and Favorites (specific per logged user) area. Favorites area should vary its contents per user.

# COMPLETE
# Adding of Quotes. Validation for empty entries should apply and should display error messages.

# COMPLETE
# Updating of Quotable quotes and Favorites contents upon clicking the Add Quote/Add to My List/Remove from My List options.

# COMPLETE
# Remove a quote from the Favorites area and moving the quote back to Quotable Quotes area.

# COMPLETE
# Individual user page which displays the quotes a particular user posted and the count of posts he/she made.

# INCOMPLETE
# You must be able to deploy your work to Amazon EC2 and provide the IP address or subdomain/domain name to where your work has been deployed.

def redirect_to_main(request):
    return redirect('/main')

def index(request):                                 # GET : RENDER
    return render(request, 'login_and_reg/index.html')

def register(request):                              # POST : REDIRECT
    if request.method == 'POST':
        results = User.objects.register(request.POST)
        if results[0] == False:
            for each in results[1]:
                messages.info(request, each)
            return redirect('/')
        elif results[0] == True:
            request.session['logged_in'] = True
            request.session['id'] = results[1]
            request.session['first_name'] = results[2]
            return redirect('/quotes')
        else:
            messages.info(request, "something went wrong")
            return redirect('/')

def login(request):                                 # POST : REDIRECT
    if request.method == 'POST':
        results = User.objects.login(request.POST)
        if results[0] == False:
            for each in results[1]:
                messages.info(request, each)
            return redirect('/')
        elif results[0] == True:
            request.session['logged_in'] = True
            request.session['id'] = results[1]
            request.session['first_name'] = results[2]
            return redirect('/quotes')
        else:
            messages.info(request, 'something went wrong')
            return redirect('/')

def quotes(request):                                # GET : RENDER
    results = Quote.objects.get_quotes(request)
    favorites = Quote.objects.get_favorites(request)
    context = {
                'quotes': results[1],
                'favorites': favorites[1]
              }
    return render(request, 'login_and_reg/quotes.html', context)

def logout(request):                                # POST : REDIRECT
    if request.method == 'POST':
        request.session.pop('id')
        request.session.pop('first_name')
        request.session['logged_in'] = False
    return redirect('/')

def create(request):                                # POST : REDIRECT
    if request.method == 'POST':
        results = Quote.objects.create_quote(request)
        if results[0] == False:
            for each in results[1]:
                messages.info(request, each)
            return redirect('/quotes')
        elif results[0] == True:
            return redirect('/quotes')
        else:
            messages.info(request, "something went wrong")
            return redirect('/quotes')
    return redirect('/quotes')

def favorite(request, id):                          # POST : REDIRECT
    if request.method == 'POST':
        results = Quote.objects.create_favorite(request, id)
    return redirect('/quotes')

def remove_favorite(request, id):                   # POST : REDIRECT
    if request.method == 'POST':
        results = Quote.objects.remove_favorite(request, id)
    return redirect('/quotes')

def users_page(request, id):
    users_quotes = User.objects.get_contributions(request, id)
    that_user = User.objects.get(id=id)
    contributions_count = User.objects.get_contributions_count(request, id)
    context = {
                'contributions': users_quotes[1],
                'that_user': that_user,
                'contributions_count': contributions_count[1]
            }
    return render(request, 'login_and_reg/user.html', context)
