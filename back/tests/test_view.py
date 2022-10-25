from multiprocessing.connection import Client
from unittest import TestCase

import json
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from salas.models import Sala, Reservacion
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.salas_url = reverse('salas_info')
        self.rform_url = reverse('rform')
        self.eform_url = reverse('eform',args=[12])
        self.add_url = reverse('add')
        self.eli_url = reverse('sub')
        self.sala1 = Sala.objects.create(
            nme_sala='hola',
            ocupied = False
        )
        self.user1 = User.objects.create(
            username = "prueba",
            password = make_password("qsxwdcefv"),
            is_superuser = False,
        )
        self.resvtest = Reservacion.objects.create(
            sala_id = self.sala1.id,
            usr_id = self.user1.id,
            hr_ini = '14:00',
            hr_end = '14:30',
        )
        

    def test_retSalas_GET(self):

        response = self.client.get(self.salas_url)

        self.assertEquals(response.status_code, 200)
        print("salas_info retorna un JSON %s" % response.content)
    
    def test_rform_GET(self):
        response = self.client.get(self.rform_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'component/form.html')

    def test_eform_GET(self):
        response = self.client.get(self.eform_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'component/elimForm.html')

    def test_add_POST_add_new_resrv(self):
        response = self.client.post(self.add_url,{
            'user':self.user1.username,
            'passw':'qsxwdcefv',
            'sala':self.sala1.id,
            'hr_ini':'15:00',
            'hr_end':'16:30'
        })

        self.assertEquals(response.status_code, 302)

    def test_sub_POST_rmv_resrv(self):
        response = self.client.post(self.eli_url,{
            'id': self.resvtest.id,
            'user':self.user1.username,
            'passw':'qsxwdcefv',
        })
        print(response.serialize_headers())
        self.assertEquals(response.status_code, 302)