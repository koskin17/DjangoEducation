from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered    #TODO: удалить


from .models import News, Category

# Это класс-редактор, который позволяет настроить отображением полей в админ.панели
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo', 'category', 'created_at', 'updated_at', 'is_published') # Настройка полей, которые будут отображаться в админке по конкретному приложению
    # Класс-конструктор тоже должен быть обязательно зарегистрирован, как и сама модель.
    list_display_links = ('id', 'title', 'category') # Перечень полей, которые являются ссылка на записи
    search_fields = ('title', 'content') # Перечень полей, по которым можно осуществлять поиск
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

# Это класс-редактор, который позволяет настроить отображением полей в админ.панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title') # Настройка полей, которые будут отображаться в админке по конкретному приложению
    # Класс-конструктор тоже должен быть обязательно зарегистрирован, как и сама модель.
    list_display_links=('id', 'title') # Перечень полей, которые являются ссылка на записи
    search_fields=('title',) # Перечень полей, по которым можно осуществлять поиск

# admin.site.register(News, NewsAdmin)   # Регистрация приложения, которое создано, в админ.панели сайта, а также класса-конструктора. Очень важно соблюдать последовательность регистрации: сначала сама модель, а только потом класс-конструктор для неё
# admin.site.register(Category, CategoryAdmin)
