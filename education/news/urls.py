from django.urls import path

from .views import *

urlpatterns = [
    # path('', index, name='home'),    # Из-за того, что в корневом файле views.py есть include со списком маршрутов и path с 'news/' был отброшен, то здесь мы указываем пустую строку, а потом функцию, которую вызываем
    path('', HomeNews.as_view(), name='home'),    # Это маршрут для переопределнного класса HomeNews
    # path('category/<int:category_id>/', get_category, name='category'),  # Это маршрут до применения ListView
    path('category/<int:category_id>/', NewsByCategory.as_view(extra_context={'title':'Какой-то тайтл'}), name='category'), # В данном случае extra_content - это просто пример того, как в метод as_view ещё можно передавать дополнительные параметры
    ## 🔧 Что такое `.as_view()` и зачем оно?
    # Это встроенный **метод класса `ListView`**, который:
    # - преобразует класс в **функцию-представление**, которую Django может вызвать
    # - подключает `get_queryset`, `template_name`, `context_object_name`
    # - обрабатывает запрос (`GET`, `POST`, `kwargs`) и возвращает `HttpResponse`
    # 📘 Без `.as_view()` Django не сможет “понять”, что ты передаёшь именно представление — оно должно быть функцией.
    # ---
    # ## 📎 Под капотом
    # Вот что делает Django при обработке запроса:
    # 1. Получает URL: `/category/3/`
    # 2. Находит маршрут: `path('category/<int:category_id>/', NewsByCategory.as_view())`
    # 3. Вызывает:  
    # ```python
    # view_instance = NewsByCategory()
    # view_function = view_instance.dispatch(request, *args, **kwargs)
    # ```
    # 4. Передаёт `category_id=3` → доступно как `self.kwargs['category_id']`
    # path('news/<int:news_id>/', view_news, name='view_news'), # Это старый маршрут, который был до применения класса DetailView
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', add_news, name='add_news'),
]