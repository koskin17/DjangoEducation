from django.shortcuts import render
from django.http import HttpResponse

from .models import News, Category

def index(request):
    news = News.objects.all()  # Получаем все новости, отсортированные по дате создания в обратном порядке. Сотрировка берётся из модели, из класса Meta
    context = {
        'news': news,
        'title': 'Список категорий',
    }
    return render(request, template_name='news/index.html', context=context)
    # В функциб render мы передаём сам запрос, путь к файлу шаблона, а также можно передать переменные и их значения, которые потом будут доступны на странице (в html-шаблоне) по своим именам

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', { 'news': news, 'category': category})

def view_news(request, news_id):
    news_item = News.objects.get(pk=news_id)
    return render(request, 'news/view_news.html', {"news_item": news_item})

