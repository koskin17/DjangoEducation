from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm

def index(request):
    news = News.objects.all()  # Получаем все новости, отсортированные по дате создания в обратном порядке. Сотрировка берётся из модели, из класса Meta
    context = {
        'news': news,
        'title': 'Список категорий',
    }
    return render(request, template_name='news/index.html', context=context)
    # В функцию render мы передаём сам запрос, путь к файлу шаблона, а также можно передать переменные и их значения, которые потом будут доступны на странице (в html-шаблоне) по своим именам

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', { 'news': news, 'category': category})

def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {"news_item": news_item})

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST) # Так мы обращаемся к форме и забираем все данные, который она отправила методом POST
        # Можно отдельно проверять, прошла ли форма валидацию
        if form.is_valid():   # Есть метод is_bond, который позволяет проверить, были ли отправлена форма и заполнился ли объект из formsэтими данными
            # print(form.cleaned_data)    # Если форма проходит валидацию, то у неё появляется свойство cleaned_data - это словарь, из которого эти данные потом и сохраняются
            # news = News.objects.create(**form.cleaned_data) # В данном случае ** - это метод python для распаковки словарей. Т.е. title, content и все остальные поля будут автоматически присвоены соответствующим ключам. Это и есть сохранение новости. Здесь используется метод create потому что метода save() нет у форм, которые не связаны с моделями.
            # # Для форм, связанных с моделями, есть метод save(). При его использовании не нужно очищать данные (form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        # Если же данные приходят не POST, а GET, то просто создаётся новая пустая форма
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
