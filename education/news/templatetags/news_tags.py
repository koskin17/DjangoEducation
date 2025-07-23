# Создаём пользовательские / свои собсвтенные теги.
from django import template

from news.models import Category

# Регистрируем наш template тег, чтобы всё работало
register = template.Library()


# Теперь создаём функцию, которая будет возвращать наши категории, которая и будет тем самым пользовательским тегом
# Также важно использовать декоратор. Можно без скобок, но в скобки можно передать новое название функции (вместо get_categories) в виде параметра name = '')
# Это и есть собственный, кастомный simple_tag
@register.simple_tag(name='list_categories')
def get_categories():
    """ Функция возвращает список категорий"""

    return Category.objects.all()

# Создаём inclusion_tag
# Сначала регистрируем декоратором шаблон, который мы создаём предварительно
@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='World'):    # Можно передавать дополнительные параметры (def show_categories(arg1='Hello', arg2='World')
    categories = Category.objects.all()
    return {"categories": categories, "arg1": arg1, "arg2": arg2}   # При передачи доп. параметров в функцию return должен выглядеть с из возвратом, чтобы увидеть их значения return {"categories": categories, "arg1": arg1, "arg2": arg2}