from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy # Суть reverse_lazy в том, что он постоение ссылки будет использовано только тогда, когда до этого момента дойдёт очередь

from .models import News, Category
from .forms import NewsForm


class HomeNews(ListView):   # В этом классе мы будем переопределять некоторые атрибуты, которые есть у родительских классов
    model = News    # Здесь определялется модель, с которой мы будем работать. По сути это замена строки news = News.objects.all()
    # Если мы хотим работать со своим шаблоном, а не с шаблоном news_list, который ищет django автоматически, и если мы хотим работать не с объектом ObjectList, а хотим работать с объектом News, то просто переопределяются другие атрибуты класса
    template_name = 'news/home_news_list.html'  # Так указывается новое имя шаблона, с которым мы хотим работать
    context_object_name = 'news' # Так указывается другой объект, данные из которого мы хотим получать
    # extra_context = {'title': 'Главная'}    # Это атрибут для переопределения дополнительных полей на странице, которая рендерится автоматически. Его рекомендуется использовать только для статичных данных. Для списков, для динамически обновляющихся данных надо использовать get_context_data, который описан ниже.

    def get_context_data(self, **kwargs):   # Этот метод используется для переопределения динамически изменяющихся данных
        context = super().get_context_data(**kwargs)  # Определяем переменую context и берём из неё то, что возвращает нам родительский метод. Так мы сохранили все данные, которые до переопределения метода были
        context['title'] = 'Главная страница'
        # В результате мы взяли всё, чтобы было в контексте и дополнили своими данными, т.е. переопределили контекст, который будет передаваться в шаблон 
        return context
    
    def get_queryset(self): #Тут мы поправляем деволтный запрос, который отправляет и выбирает всё, на запрос, который фильтрует данные по признаку. В данном случае выбираются новости, которые опубликованы.
        return News.objects.filter(is_published = True)
    
class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news+list.html'  #Также переопределяем шаблон, который будет использоваться в качестве страницы
    context_object_name = 'news'
    allow_empty = False # Это специальный атрибут класса, который показывает пустые списки. По умолчанию он установлен в True. Поставив в False запрещается показ пустых списков, т.е. если, к примеру, категория пустая, т.е. в ней нет новостей, то сама категория не будет показываться, а будет просто ошибка 404, т.е. нет такой страницы с категорией, которая пустая, т.е. и категории как-бы нет.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self): # Для получения новостей только одной категории надо использовать параметр category_id, который есть в объекте self. Т.е. мы добавляет к фильтру ещё и фильтрацию по category_id
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published = True)
        ## 🔍 Почему используется `self.kwargs['category_id']`?
        # Когда ты описал маршрут:
        # ```python
        # path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
        # Django формирует URL с **именованным параметром** `category_id`.
        # 🔧 Когда пользователь открывает `/category/3/`:
        # - Django извлекает `category_id=3` из URL
        # - И передаёт его в класс `NewsByCategory`
        # - Внутри класса ты получаешь его через:
        # ```python
        # self.kwargs['category_id']
        # ```

        # 📦 `kwargs` — это словарь именованных параметров из URL.  
        # Если бы ты описал `path('category/<int:id>/', ...)`, то был бы `self.kwargs['id']`.
        # ---
        # ## 🧠 Откуда берутся эти `kwargs`?
        # Они формируются автоматически Django'ом на основе `urls.py`.  
        # Когда ты пишешь `<int:category_id>`, ты фактически создаёшь `category_id`, доступный как `kwargs['category_id']`.

# После внедрения метода ListView этот метод стал не нужен и я его просто не удалил.
# def index(request):
#     news = News.objects.all()  # Получаем все новости, отсортированные по дате создания в обратном порядке. Сотрировка берётся из модели, из класса Meta
#     context = {
#         'news': news,
#         'title': 'Список категорий',
#     }
#     return render(request, template_name='news/index.html', context=context)
#     # В функцию render мы передаём сам запрос, путь к файлу шаблона, а также можно передать переменные и их значения, которые потом будут доступны на странице (в html-шаблоне) по своим именам

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', { 'news': news, 'category': category})

class ViewNews(DetailView):  # Этот класс используется для отображения одной новости
    model = News  # Здесь указывается модель, с которой мы будем работать
    context_object_name = 'news_item'  # Здесь указывается имя объекта, который будет передаваться в шаблон. По умолчанию это object, но мы переименовываем его в news_item, чтобы было понятнее
    # template_name   = 'news/news_detail.html' # Это написано как напоминание о том,  что в качестве шаблона можно использовать свой шаблон, а не тот, который по умолчанию ищет Django. Если не указать, то будет использоваться шаблон news/news_detail.html
    # pk_url_kwarg = 'news_id'  # Здесь указывается, что в качестве идентификатора новости будет использоваться параметр news_id из URL. Это нужно для того, чтобы Django знал, какой именно объект нужно получить из базы данных. В противном случае он будет пытаться использовать первичный ключ (pk) модели, который по умолчанию называется 'pk'.
    # pk_url_kwarg - это параметр, который используется для получения объекта по его первичному ключу (pk) из URL.
    # pk - это первичный ключ, который используется для идентификации объекта в базе данных

class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')    # Тут полностью переопределяется url от того, который по умолчанию. Важно помнить, что функцию reverse вообще нельзя использовать в данном случае - только reverse_lazy

# Функция ниже была создана до внедрения классов-контроллеров
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST) # Так мы обращаемся к форме и забираем все данные, который она отправила методом POST
#         # Можно отдельно проверять, прошла ли форма валидацию
#         if form.is_valid():   # Есть метод is_bond, который позволяет проверить, были ли отправлена форма и заполнился ли объект из formsэтими данными
#             # print(form.cleaned_data)    # Если форма проходит валидацию, то у неё появляется свойство cleaned_data - это словарь, из которого эти данные потом и сохраняются
#             # news = News.objects.create(**form.cleaned_data) # В данном случае ** - это метод python для распаковки словарей. Т.е. title, content и все остальные поля будут автоматически присвоены соответствующим ключам. Это и есть сохранение новости. Здесь используется метод create потому что метода save() нет у форм, которые не связаны с моделями.
#             # # Для форм, связанных с моделями, есть метод save(). При его использовании не нужно очищать данные (form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         # Если же данные приходят не POST, а GET, то просто создаётся новая пустая форма
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
