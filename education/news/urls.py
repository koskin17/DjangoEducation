from django.urls import path

from .views import *

urlpatterns = [
    # path('', index, name='home'),    # Из-за того, что в корневом файле views.py есть include со списком маршрутов и path с 'news/' был отброшен, то здесь мы указываем пустую строку, а потом функцию, которую вызываем
    path('', HomeNews.as_view(), name='home'),    # Это маршрут для переопределнного класса HomeNews
    path('category/<int:category_id>/', get_category, name='category'),
    path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/add-news/', add_news, name='add_news'),
]