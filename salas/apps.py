import time
import socket
import re
import sys
from datetime import datetime
from threading import Thread
from django.apps import AppConfig


class UpdatingThread(Thread):
    ###
    # hilo que mantendra actualizado al crud
    # dando de baja a las reservaciones caducadas
    # y cambiando el estado de las salas para saber si estan
    # actualmente ocupadas
    ###
    def run(self):
        from salas.models import Sala, Reservacion
        while(True):
            #print(datetime.now().time())
            if check_server('localhost',8000):
                break
            n = datetime.now().time()
            reservaciones = Reservacion.objects.all()
            for res in reservaciones:
                if((res.hr_ini <= n) and (res.hr_end >= n)) and not res.sala.ocupied:
                    res.sala.ocupied = True
                    res.sala.save()
                if(res.hr_end < n):
                    res.sala.ocupied = False
                    res.sala.save()
                    res.delete()
            salas = Sala.objects.all()
            for s in salas:
                r = Reservacion.objects.filter(sala = s)
                if not r:
                    s.ocupied = False
                    s.save()
            #print(n)
            time.sleep(1) #repetir cada segundo
    
#Funcion que permitira terminar el hilo una vez se cierre el servidor
def check_server(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex(('127.0.0.1', 8000))

    if result == 0:
        #print('socket is open')
        s.close()
        return False
        
    #print('socket is closed')
    s.close()
    return True
        


class SalasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salas'

    def ready(self):
        from salas.models import Sala,Reservacion
        UpdatingThread().start()


