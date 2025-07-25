from django import forms
from .models import Category
from .models import News
import re
from django.core.exceptions import ValidationError


# class NewsForm(forms.Form): # Формы всегда наследуются от родительского класса forms.Form или forms.Modelforms, в зависимости от того, какая форма и привязан ли она к модели или нет. В данном случае создаётся форма, которая не привязан к модели и все поля в форме отдельно, конкретно прописываются. Если же форма привязан к модели, то все поля в форме проставляются django автоматически. Все поля в формам в django по умолчанию имеют статут requiered = True, т.е. если поле не обязательное, то надо отдельно дополнительно прописывать requiered = False
#     """ Это класс для формы, которая не связана с моделью """

#     title = forms.CharField(max_length=150, label='Заголовок:', widget=forms.TextInput(attrs={'class': 'form-control'})) # widget - это способ передачи атрибутов для поля, в том числе и класса из bootstrap
#     content = forms.CharField(label='Текст новости:', widget=forms.Textarea(attrs={'class': 'form-control'})) # Также можно изменить дополнительные параметры, которые bootstrap сам накладывает. Например изменить число строк: "rows": 5, написав это словарём в attrs
#     is_published = forms.BooleanField(label='Опубликовано?', initial=True) # Атрибут initial - это изначальное состояние поля. В данном случае галочка будет стоять "по умолчанию"
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберите категорию', widget=forms.Select(attrs={'class': 'form-control'})) # Это поле с возможностью выбора, т.е. со списком. Указывается модель, данные из которой будут доступны для выбора. Атрибут empty_label убирает тире по умолчания "------" и можно назначить свой текст

class NewsForm(forms.ModelForm): #Если форма связана с моделью, то она наследуется от класса ModelForm
    """ Эта форма связана с моделью """

    class Meta:
        model = News # Указывается модель, с которой эта форма должна быть связана
        # fields = '__all__' # Если написать '__all__', то в форме будут представлены все поля из модели. Если же надо отобрать конкретные, то нужно перечислить нужные поля. Но настоятельно рекомендуется всегда перечислять все поля, которые нужны, даже если нужны все поля из модели
        fields = ['title', 'content', 'is_published', 'category']
        # Для укахание дополнительных параметров для полей формы используется параметр widgetsm в котором в виде словаря указываются поля и нужные для него парамтры.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):   # Пользовательские валидаторы всегда называются с clean_ и потом название поля, которое валидируется
        title = self.cleaned_data['title']  # Тут мы получаем значение из словаря по ключу title (очищенный) из объекта (self)
        if re.match(r'\d', title):   # Если в начале строки title будут найдены цифры, то такая строка нам не подходит
            raise ValidationError('Название не должно начинаться с цифры!')
        return title
