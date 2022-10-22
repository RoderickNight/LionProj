import string
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Sala(models.Model):
    nme_sala = models.CharField(max_length = 200)
    #usr = models.ForeignKey(Users)
    def __str__(self):
        return self.nme_sala