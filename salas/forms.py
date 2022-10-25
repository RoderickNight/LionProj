from turtle import textinput
from django import forms
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from salas.models import Reservacion

#formulario para revisar si puede eliminar reserva
class CreateCheckUserForm(forms.Form):
    id = forms.CharField(
        widget = forms.HiddenInput(
            attrs = {
                'class':'',
                'id': 'hid_id',
            }
        )
    )
    user = forms.CharField(
        label = 'Usuario',
        widget = forms.TextInput(
            attrs = {
                'class':'',
                'id': 'usr_elim',
                'placeholder':'Ingresa tu usuario',
                'required':True
            }
        )
    )
    passw = forms.CharField(
        label = 'Contraseña',
        widget = forms.PasswordInput(
            attrs = {
                'class':'',
                'id':'pass_elim',
                'placeholder':'Ingresa tu contraseña',
                'required':True
            }
        )
    ) 

#Formulario para añadir una reserva
class ReservarForm(forms.ModelForm):
    user = forms.CharField(
        label = 'Usuario',
        widget = forms.TextInput(
            attrs = {
                'class':'',
                'placeholder':'Ingresa tu usuario',
                'required':True
            }
        )
    )
    passw = forms.CharField(
        label = 'Contraseña',
        widget = forms.PasswordInput(
            attrs = {
                'class':'',
                'placeholder':'Ingresa tu contraseña',
                'required':True
            }
        )
    ) 
    class Meta:
        model = Reservacion
        fields = ('sala','hr_ini','hr_end')
        label = {
            'sala': 'Sala',
            'hr_ini': 'Elige la hora de comienzo',
            'hr_end': 'Elige la hora de termino'
        }
        widgets = {
            'sala': forms.Select(
                attrs = {
                    'class':'',
                    'placeholder':'Selecciona la sala',
                    'required':True
                }
            ),
            'hr_ini': forms.TimeInput(
                attrs = {
                    'class':'',
                    'type':'time',
                    'required':True
                }
            ),
            'hr_end': forms.TimeInput(
                attrs = {
                    'class':'',
                    'type':'time',
                    'required':True
                }
            )
        }

    #def clean_user(self):
    #    user = self.data['user']
    #    print(user)
    #    try:
    #        usr = User.objects.get(username = user)
    #    except ObjectDoesNotExist:
    #        print("kk")
    #        raise forms.ValidationError(_("El usuario no existe"))
    #    return user

