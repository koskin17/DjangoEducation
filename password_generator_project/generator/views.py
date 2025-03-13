from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('Hello there frend!')

def eggs(request):
    return HttpResponse('<h1>Eggs are so tasty!</h1>')