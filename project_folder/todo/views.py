from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from .models import Todo
from django.http import HttpResponse
from django.utils import timezone


def index(request):
    todos = []
    if request.user.is_authenticated:
        todos = Todo.objects.filter(doer=request.user)

    return render(request, "todo/index.html", {"user": request.user, "todos": todos})

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # A04 Insecure Design - Doesn't check if user already exists
        # fix: check that username is unique

        # if User.objects.filter(username=username).exists():
            # return render(request, "todo/register.html", {"error": "Username already exists"})

        user = User(username=username, password=password)
        user.save()

        # A02 Cryptographic Failures - Password isn't hashed but instead is
        # saved in text format
        # fix: use ready and secure create_user -function

        # user = User.objects.create_user(username=username, password=password)
        # user.save()

        return redirect("index")
    
    return render(request, "todo/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:

        # A02 Cryptographic Failures - Secure authentication isn't used
        # fix: check if user exists and autenticate if exists

        # user_exists = User.objects.filter(username=username).exists()
        # if user_exists:
            # user = authenticate(request, username=username, password=password)
        
            try:
                user = User.objects.get(username=username)
                if user.password != password:
                    return render(request, "todo/login.html", {"error": "Wrong password"})
    
            except User.DoesNotExist:
                return render(request, "todo/login.html", {"error": "User doesn't exist"})

            else:
                login(request, user)
                return redirect("index")

        # A07 Identification and Authentication Failures - Error leaks sensitivce information
        # and enables user enumeration attack
        # fix: use the same message for all outcomes

        # user = authenticate(request, username=username, password=password)

        # if user is not None:
            # login(request, user)
            # return redirect("index")
        # else:
            # return render(request, "todo/login.html", {"error": "Invalid credentials"})
        
    return render(request, "todo/login.html")

def create_todo(request):
    if request.method == "POST":
        todo_note = request.POST.get("todo_note")
        if todo_note:
            Todo.objects.create(doer = request.user, todo_note = todo_note, pub_date = timezone.now())
        return redirect("/")
    return render(request, "todo/create_todo.html")

def delete_todo(request):
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        if todo_id:
            Todo.objects.filter(id=todo_id).delete()
            
            # A01 Broken Access Control - one can view or edit someone else's account,
            # in this case delete others todos
            # fix: verify todos ownership and filter todos by user
            
            # Todo.objects.filter(id=todo_id, doer=request.user).delete()

    return redirect("/")

def logout_view(request):
    logout(request)
    return redirect("/")