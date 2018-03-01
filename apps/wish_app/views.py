from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Wishlist
from django.contrib import messages

def index(request):
    return render(request, "wish_app/index.html")

def register(request):
    speak = User.objects.register(request.POST)
    if speak[0]:
        request.session["user_id"] = speak[1].id
        messages.add_message(request, messages.SUCCESS, 'You successfully registered. Welcome!')
        return redirect("/dash")
    else:
        for error in speak[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def login(request):
    user = User.objects.login(request.POST)
    if user["is_valid"]:
        request.session["user_id"] = user["user"].id
        messages.add_message(request, messages.SUCCESS, 'Success! Welcome back!')
        return redirect("/dash")
    else:
        for error in user["errors"]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "You have successfully logged out of your account.")
    return redirect("/")

def dash(request):
    if "user_id" not in request.session:
        return redirect("/")
    data = {
		"user": User.objects.get(id=request.session["user_id"]),
        "wish": Wishlist.objects.all(),
        "wanted": Wishlist.objects.all().filter(others= request.session["user_id"]),
        "created": Wishlist.objects.filter(creator=request.session["user_id"])
	}
    return render(request, "wish_app/dash.html", data)

def info(request, wish_id):
    if "user_id" not in request.session:
        return redirect("/")
    data = {
        "user": User.objects.get(id=request.session["user_id"]),
        "wishes": Wishlist.objects.get(id=wish_id),
        "wanters": Wishlist.objects.get(id=wish_id).others.all()
    }
    return render(request, "wish_app/info.html", data)


def add(request):
    if "user_id" not in request.session:
        return redirect("/")
    data = {
            "user":User.objects.get(id=request.session['user_id']),
        }
    return render(request, "wish_app/add.html", data)

def new(request):
    wish = Wishlist.objects.itemcheck(request.POST, id=request.session['user_id'])
    if wish[0]:
        messages.add_message(request, messages.SUCCESS, 'New item added!')
        return redirect("/dash")
    else:
        for error in wish[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/add")

def want(request, id):
    newWant = Wishlist.objects.wishCheck(id, request.session["user_id"])
    if newWant[0]:
        return redirect("/dash")
    else:
        for error in newWant[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/dash")

def unwant(request, id):
    Wishlist.objects.unwishCheck(id, request.session["user_id"])
    return redirect("/dash")

def forget(request, id):
    a = Wishlist.objects.get(id=id).creator_id
    if request.session["user_id"] != a:
        return redirect("/dash")
    else:
        Wishlist.objects.filter(id=id).delete()
        return redirect("/dash")


