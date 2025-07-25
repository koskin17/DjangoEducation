from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .models import News, Category
from .forms import NewsForm


class HomeNews(ListView):   # В этому классе мы будем переопределять некоторые атрибуты, которые есть у родительских классов
    model = News    # Здесь определялется модель, с которой мы будем работать. По сути это замена строки news = News.objects.all()
    # Если мы хотим работать со своим шаблоном, а не с шаблоном news_list, который ищет django автоматически, и если мы хотим работать не с объектом ObjectList, а хотим работать с объектом News, то просто переопределяются другие атрибуты класса
    template_name = 'news/home_news_list.html'  # Так указывается новое имя шаблона, с которым мы хотим работать
    context_object_name = 'news' # Так указывается другой объект, данные из которого мы хотим получать
    # extra_context = {'title': 'Главная'}    # Это атрибут для переопределения дополнительных полей на странице, которая рендерится автоматически. Его рекомендуется использовать только для статичных данных. Для списков, для динамически обновляющихся данных его использовать не рекомендуется.

    def get_context_data(self, **kwargs):   # Этот метод используется для переопределения динамически изменяющихся данных
        context = super().get_context_data(**kwargs)  # Определяем переменую context и берём из неё то, что возвращает нам родительский метод. Так мы сохранили все данные, которые до переопределения метода были
        context['title'] = 'Главная страница'
        # В результате мы взяли всё, чтобы было в контексте и дополнили своими данными, т.е. переопределили контекст, который будет передаваться в шаблон 
        return context
    
    def get_queryset(self): #Тут мы поправляем деволтный запрос, который отправляет и выбирает всё, на запрос, который фильтрует данные по признаку. В данном случае выбираются новости, которые опубликованы.
        return News.objects.filter(is_published = True)

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
