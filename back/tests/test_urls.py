from django.test import SimpleTestCase
from django.urls import reverse, resolve
from salas.views import *

class TestUrls(SimpleTestCase):

    testid = 25

    def test_salas_info_url_is_resolved(self):
        url=reverse('salas_info')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, retSalas)
    
    def test_add_url_is_resolved(self):
        url=reverse('add')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, createReserv)

    def test_rform_url_is_resolved(self):
        url=reverse('rform')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, mostrarForm)

    def test_eform_url_is_resolved(self):
        url=reverse('eform',args=[self.testid])
        #print(resolve(url))
        self.assertEquals(resolve(url).func, mostrarFormElim)

    def test_sub_url_is_resolved(self):
        url=reverse('sub')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, elimReserv)