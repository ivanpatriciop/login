from django.db import models
from django.db.models.fields import DateTimeField
import re
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# Validaciones (se coloca antes que las clases de modelo)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors= {}
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "El nombre debe ser mayor a 2 caracteres"
            
        if len(postData["first_name"]) < 2:
            errors["last_name"] = "El apellido debe ser mayor a 2 caracteres"
            
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Dirección de correo no válida"
            
        repeated_email = User.objects.filter(email = postData["email"])
        if len(repeated_email) > 0:
            errors["email_repetido"] = "La dirección de correo electrónica ya se encuentra registrada"
            
        if len(postData["password"]) < 8:
            errors["longitud_password"] = "La longitud del password debe ser de al menos 8 caracteres"
            
        if postData["password"] != postData["password_confirm"]:
            errors["password_no_coincide"] = "Las contraseñas ingresadas no coinciden."
            
        if datetime.strptime(postData["birth_date"], '%Y-%m-%d') > datetime.now():
            errors["fecha_incorrecta"] = "La fecha seleccionada no puede ser mayor que le fecha actual."
        
        birth_date = datetime.strptime(postData["birth_date"], '%Y-%m-%d')
        edad = relativedelta(datetime.now(), birth_date)
        if edad.years < 13:
            errors["edad"]= "Debe ser mayor de 13 años para poder registrarse"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    birth_date = models.DateField()
    password =models.CharField(max_length=250)
    created_at = DateTimeField(auto_now_add = True)
    modified_at =DateTimeField(auto_now=True)
    objects = UserManager()
