from http.client import responses
import time

from datetime import datetime, timedelta
from typing import List
from urllib import response
from wsgiref import headers
from xmlrpc.client import ResponseError
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.core import serializers
from .forms import CreateCheckUserForm, ReservarForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from salas.models import Reservacion, Sala

# Create your views here.

#test func
def hello(request):
    if request.method == "GET":
        return render(request, 'index.html' ,{
            'form': CreateCheckUserForm()
        })
    elif request.method == "POST":
        return render(request, 'index.html')

#regresa la información referente a las salas
def retSalas(request):  
    data = []
    salas = Sala.objects.all()
    for s in salas:
        darray = []
        reserv = Reservacion.objects.filter(sala=s)
        for r in reserv:
            temp = {
                'id':r.id,
                'usr':r.usr.username,
                'hr_ini': r.hr_ini,
                'hr_end': r.hr_end
            }
            darray.append(temp)
        rec = {
            'sala': {'nme_sala':s.nme_sala,'ocupied':s.ocupied},
            'reserva': darray,
        }
            
        data.append(rec)
    return JsonResponse(data,safe = False)

#regresa la plantilla del formulario de reserva
def mostrarForm(request):
    return render(request, 'component/form.html',{
        'modalForm':ReservarForm
    })

#regresa la plantilla del formulario de eliminar
def mostrarFormElim(request, id_res):
    print(id_res)
    return render(request, 'component/elimForm.html',{
        'Form':CreateCheckUserForm(initial = {'id': id_res, 'user':'', 'passw':''})
    })

#crear una nueva reserva
def createReserv(request):
    err_flag, err_msg = checks(request)

    if(err_flag):
        return HttpResponseBadRequest(err_msg,headers={'mensaje':err_msg})
    user = get_object_or_404(User,username = request.POST.get('user'))
    if(request.method == 'POST'):
        Reservacion.objects.create(
            sala_id = request.POST.get('sala'),
            usr_id = user.id,
            hr_ini = request.POST.get('hr_ini'),
            hr_end = request.POST.get('hr_end'),
        )
    response = redirect('/')
    return response

#eliminar reserva
def elimReserv(request):
    print("aca")
    try:
        res=Reservacion.objects.get(id=request.POST['id'])
        print("hola")
    except ObjectDoesNotExist:
        print("fallo id")
        print(request.POST['id'])
        return HttpResponseBadRequest('La reservacion no existe',headers={'mensaje':'La reservacion no existe'})

    err_flag, err_msg = checks_Usr(request)
        
    if(err_flag):
        return HttpResponseBadRequest(err_msg,headers={'mensaje':err_msg})

    res.delete()
    
    response = redirect('/')
    return response

#validaciones de usuario
def checks_Usr(request):
    try:
        usr = User.objects.get(username = request.POST.get('user'))
    except ObjectDoesNotExist:
        print("adno en el fallo")
        return True, "El usuario no existe"

    if(not check_password(request.POST.get('passw'),usr.password)):
        #raise forms.ValidationError("Contraseña erronea")
        return True, "Contraseña erronea"

    return False, '' 

#validaciones del formulario para altas de reservas
def checks(request):
    initime = datetime.strptime(request.POST['hr_ini'], '%H:%M')
    endtime = datetime.strptime(request.POST['hr_end'], '%H:%M')
    duration = endtime - initime

    #horario de limite 2hrs
    if(duration > timedelta(seconds=2*3600)):
        #raise forms.ValidationError("El horario debe ser menor a dos horas")
        return True, "El horario debe ser menor a dos horas"

    if(initime > endtime):
        #raise forms.ValidationError("Las hora de termino debe ser despues de la de inicio")
        return True, "Las hora de termino debe ser despues de la de inicio"

    tflag, tmsg = checks_Usr(request)
    if(tflag):
        return tflag, tmsg

    cmpdata = Reservacion.objects.filter(sala_id=request.POST.get('sala'))

    #revisar que no se solapen los horarios
    initime = initime.time()
    endtime = endtime.time()
    for data in cmpdata:
        tempindate = data.hr_ini
        tempendate = data.hr_end
        if((tempindate == initime) and (tempendate == endtime)):
            print("works")
            return True, "Este horario esta ocupado"
        if((tempindate < initime)and(tempendate > initime)):
            #raise forms.ValidationError("Este horario esta ocupado")
            return True, "Este horario esta ocupado"
        if((tempindate < endtime)and(tempendate > endtime)):
            #raise forms.ValidationError("Este horario esta ocupado")
            return True, "Este horario esta ocupado"
    return False, ""
