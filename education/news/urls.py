from django.urls import path

from .views import *

urlpatterns = [
    path('', index),    # Из-за того, что в корневом файле views.py есть include со списком маршрутов и path с 'news/' был отброшен, то здесь мы указываем пустую строку, а потом функцию, которую вызываем
]