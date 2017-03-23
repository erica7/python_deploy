from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# request.session:
    # session_messages: any errors or feedback to users   - replacing with messges framework
    # logged_in: true or false
    # user: first name of logged in user


def index(request):                                 # GET : RENDER
    return render(request, 'login_and_reg/index.html')

def register(request):                              # POST : REDIRECT
    results = User.objects.register(request.POST)
    if results[0] == False:
        for each in results[1]:
            messages.info(request, each)
        return redirect('/')
    elif results[0] == True:
        request.session['logged_in'] = True
        request.session['user'] = results[1]
        return redirect('/success')
    else:
        messages.info(request, "something went wrong")
        return redirect('/')

def login(request):                                 # POST : REDIRECT
    results = User.objects.login(request.POST)
    if results[0] == False:
        for each in results[1]:
            messages.info(request, each)
        return redirect('/')
    elif results[0] == True:
        request.session['logged_in'] = True
        request.session['user'] = results[1]
        return redirect('/success')
    else:
        messages.info(request, 'something went wrong')
        return redirect('/')

def success(request):                               # GET : RENDER
    return render(request, 'login_and_reg/success.html')

def logout(request):                                # POST : REDIRECT
    request.session.pop('user')
    request.session['logged_in'] = False
    return redirect('/')
