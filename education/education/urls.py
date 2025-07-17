"""
URL configuration for education project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# Функция include позволяет подключать списки маршрутов из приложений, которые хранятся в файлах urls.py в самих приложения


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls'), name='news'), # Если используется список маршрутов (include), то django отбрасыввет не только домен, но и первый параметр, 'news/' в данном случае. Т.е. в итоге получается пустая строка.
]

# Эта строка добавлена для того, чтобы в режиме DEBUG (он автоматически включен при разработке на локальной машине выше в переменной DEBUG) иметь прямой досуп к загружаемым изображениемя. При вырузке на сервер это уже будет обрабатывать сам сервер.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
