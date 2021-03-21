from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import *
import bcrypt


# Create your views here.D
def index(request):
    return render(request, 'index.html')


def home(request):
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'quotes': Quote.objects.all()
    }
    return render(request, 'home.html', context)


def register(request):
    errors = User.objects.basic_validation(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        user_values = {}
        user_fields = [
            'first_name', 'last_name', 'email_address',
            'password', 'confirm_password'
        ]
        for field in user_fields:
            user_values[field] = request.POST[field]
        try:
            user = User.objects.create(
                first_name=user_values[user_fields[0]], last_name=user_values[user_fields[1]],
                email_address=user_values[user_fields[2]],
                password=bcrypt.hashpw(user_values[user_fields[4]].encode(), bcrypt.gensalt()).decode(),
            )
            request.session['userid'] = user.id
            return redirect('/home/')
        except IntegrityError:
            messages.error(request, 'That email address is already registered')
            return redirect('/')


def login(request):
    email = request.POST['email_address']
    if not User.objects.filter(email_address=email):
        messages.error(request, "Email Address does not exist")
        return redirect('/')
    else:
        user = User.objects.get(email_address=email)
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            return redirect('/home/')
        else:
            messages.error(request, "Invalid Email Address and Password combination")
            return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def add_quote(request):
    errors = Quote.objects.basic_validation(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/home/')
    else:
        user = User.objects.get(id=request.session['userid'])
        Quote.objects.create(
            author=request.POST['author'], quotation=request.POST['quote'],
            posted_by=user
        )
    return redirect('/home/')


def delete_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    if quote.posted_by.id == request.session['userid']:
        quote.delete()
        return redirect('/home/')
    else:
        messages.error(request, "Invalid user session id. You have been signed out.")
        return redirect('/logout/')


def like_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['userid'])
    Like.objects.create(liked_by=user, quote=quote)
    return redirect('/home/')


def view_user(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'view_user.html', context)


def my_account(request, user_id):
    if user_id == request.session['userid']:
        context = {
            'user': User.objects.get(id=request.session['userid']),
        }
        return render(request, 'my_account.html', context)
    else:
        messages.error(request, "Invalid user session id. You have been signed out.")
        return redirect('/logout/')


def update_account(request):
    errors = User.objects.basic_validation(request.POST, False)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect(f"/myaccount/{request.session['userid']}")
    else:
        user_values = {}
        user_fields = ['first_name', 'last_name', 'email_address']
        for field in user_fields:
            user_values[field] = request.POST[field]
        try:
            user = User.objects.get(id=request.session['userid'])
            user.first_name = user_values[user_fields[0]]
            user.last_name = user_values[user_fields[1]]
            user.email_address = user_values[user_fields[2]]
            user.save()
            return redirect('/home/')
        except IntegrityError:
            messages.error(request, 'That email address is already registered')
            return redirect('/')
