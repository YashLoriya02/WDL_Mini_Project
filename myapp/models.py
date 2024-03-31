from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=100)

# backend/myapp/views.py
from rest_framework import generics
from .models import Data
from .serializers import DataSerializer

class DataListCreate(generics.ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
