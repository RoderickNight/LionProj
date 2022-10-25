from email.policy import default
import string
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sala(models.Model):
    nme_sala = models.CharField(max_length = 200)
    ocupied = models.BooleanField(default = False)
    def __str__(self):
        return self.nme_sala

class Reservacion(models.Model):
    sala = models.ForeignKey(Sala, on_delete = models.CASCADE)
    usr = models.ForeignKey(User, on_delete = models.CASCADE)
    hr_ini = models.TimeField(null = True)
    hr_end = models.TimeField(null = True)
    def __str__(self):
        return self.sala.nme_sala + "-" + self.usr.username