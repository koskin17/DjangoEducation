from django.db import models

class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Отличие от auto_now в том, что auto_now_add один раз фиксируем дату время, а auto_now - каждый раз, когда запись была обновлена и сохранена. Также обязательно надо поставить True (по умолчанию у поля стоит False)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    # В этом поле сохраняется путь к загруженному файлу. Отличие от FileField в том, что FileField позволяет загружать файлы любого типа,  а ImageField только изображения
    is_published = models.BooleanField(default=True)
