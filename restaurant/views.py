from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer

def index(request):
    return render(request, 'index.html', {})
    
class MenuItemView(generics.ListCreateAPIView):
    queryset= MenuItem.objects.all()
    serializer_class= MenuItemSerializer
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset= MenuItem.objects.all()
    serializer_class= MenuItemSerializer