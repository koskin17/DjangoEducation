from django.db import models
from django.urls import reverse  # Импортируем reverse, чтобы получить URL по имени маршрута. Этот метод сразу формирует строку с URL. Если нужно отложить построение URL (например, в атрибутах класса), используют reverse_lazy — он вычисляет ссылку позже, когда она реально понадобится.   

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование")
    content = models.TextField(blank=True, verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # Отличие от auto_now в том, что auto_now_add один раз фиксируем дату и время, а auto_now - каждый раз, когда запись была обновлена и сохранена. Также обязательно надо поставить True (по умолчанию у поля стоит False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото", blank=True)
    # В этом поле сохраняется путь к загруженному файлу. Отличие от FileField в том, что FileField позволяет загружать файлы любого типа,  а ImageField только изображения
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name = 'Категория') # Модель можно указать двумя способами: ссылкой на модель (но только в том случае, если эта модель объявлена раньше, перед указанием foreign key в другой модели) или указав имя модели - 'Category'. null=True поставлен из-за того, что category и связь с category были добавлены после того, как в БД уже были добавлены новости без категории.
    
     # Создание класса, который позволяет изменять различные поля в админ.панели
    class Meta:
        verbose_name = 'Новость'    # Это правильный перевод или наименование единственного числа объекта модели, с которой мы работаем
        verbose_name_plural = 'Новости' # Это правильный перевод или наименование множественного числа объектов модели, с которой мы работаем
        ordering = ['-created_at'] # Это параметр сортировки объектов модели, с которой мы работаем ("-" означает, что в обратном порядке)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_id": self.pk})
    

class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name = 'Наименование категории') # При наличии db_index поле индексируется и поиск полей в этой таблице / модели становится более быстрым

    def get_absolute_url(self): # Название этого метода должно быть именно таким, чтобы Django мог его распознать и использовать для получения URL-адреса объекта и это договорённость между разработчиками Django. Этот метод возвращает URL-адрес для конкретного объекта модели, который будет использовать. Также django автоматически ищет этот метод и если находит его, то в админ.панели автоматически появляется кнопка "смотреть на сайте", которая ведёт на соответствующую страницу на сайте. При другом названии метода кнопки не будет.
        return reverse('category', kwargs={"category_id": self.pk}) # Главное отличе этой фукнции от template tag в том, что она строит ссылку в python-файлах, а template tag - в html-шаблонах. Здесь мы используем имя маршрута 'category' и передаем параметр category_id, который равен первичному ключу (pk) текущего объекта категории. В результате функция reverse вернет URL-адрес для этой категории, который можно использовать в шаблонах или других частях приложения.

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title', )

    def __str__(self):
        return self.title
