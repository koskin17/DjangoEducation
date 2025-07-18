from django.shortcuts import render
from django.http import HttpResponse

from .models import News

def index(request):
    news = News.objects.all()  # Получаем все новости, отсортированные по дате создания в обратном порядке. Сотрировка берётся из модели, из класса Meta
    return render(request, 'news/index.html', {'news': news, 'title': 'Список новостей'})
    # В функциб render мы передаём сам запрос, путь к файлу шаблона, а также можно передать переменные и их значения, которые потом будут доступны на странице (в html-шаблоне) по своим именам
