import re
from django.http.response import Http404, HttpResponse
from django.shortcuts import render,redirect, HttpResponse
from django.contrib import	messages
from .models import User
import bcrypt

# Create your views here.
def login(request):
    return render(request, "index.html")

def process_login(request):
    if request.method =="POST":
        user = User.objects.filter(email= request.POST["email"])
        if user:
            temp_user = user[0]
            if bcrypt.checkpw(request.POST["password"].encode(), temp_user.password.encode()):
                request.session["logged_user"] = temp_user.id
                return redirect("/success")
        messages.error(request, "El email y/o contraseña ingresados no son correctos. Por favor intente nuevamente")
    
    return redirect("/")
def success(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Para acceder a esta página, por favor regístrese y/o ingrese con su usuario")
        return redirect('/')
    context = {
        "logged_user" : User.objects.get(id= request.session["logged_user"]),
    }
    return render(request, "welcome.html", context)

def create_user(request):
    if request.method == "POST":
        # llamada a funcion para validaciones en la capa del modelo
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # método para hacer hash del password
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hash_password)
        # registro del usuario en la bdd
        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            birth_date=request.POST["birth_date"],
            password = hash_password
            )
        request.session['logged_user'] = new_user.id

        return redirect('/success')
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")
