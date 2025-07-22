from django.db import models

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование")
    content = models.TextField(blank=True, verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # Отличие от auto_now в том, что auto_now_add один раз фиксируем дату и время, а auto_now - каждый раз, когда запись была обновлена и сохранена. Также обязательно надо поставить True (по умолчанию у поля стоит False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото", blank=True)
    # В этом поле сохраняется путь к загруженному файлу. Отличие от FileField в том, что FileField позволяет загружать файлы любого типа,  а ImageField только изображения
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name = 'Категория') # Модель можно указать двумя способами: ссылкой на модель (но только в том случае, если эта модель объявлена раньше, перед указанием foreign key в другой модели) или указав имя модели - 'Category'. null=True поставлен из-за того, что category и связь с category были добавлены после того, как в БД уже были добавлены новости без категории.
    
     # Создание класса, который позволяет изменять различные поля в админ.панели
    class Meta:
        verbose_name = 'Новость'    # Это правильный перевод или наименование единственного числа объекта модели, с которой мы работаем
        verbose_name_plural = 'Новости' # Это правильный перевод или наименование множественного числа объектов модели, с которой мы работаем
        ordering = ['-created_at'] # Это параметр сортировки объектов модели, с которой мы работаем ("-" означает, что в обратном порядке)

    def __str__(self):
        return self.title
    

class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name = 'Наименование категории') # При наличии db_index поле индексируется и поиск полей в этой таблице / модели становится более быстрым

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title', )

    def __str__(self):
        return self.title
