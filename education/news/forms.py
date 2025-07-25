from django import forms
from .models import Category


class NewsForm(forms.Form): # Формы всегда наследуются от родительского класса forms.Form или forms.Modelforms, в зависимости от того, какая форма и привязан ли она к модели или нет. В данном случае создаётся форма, которая не привязан к модели и все поля в форме отдельно, конкретно прописываются. Если же форма привязан к модели, то все поля в форме проставляются django автоматически.
    title = forms.CharField(max_length=150, required=True)
    content = forms.CharField()
    is_published = forms.BooleanField()
    category = forms.ModelChoiceField(queryset=Category.objects.all()) # Это поле с возможностью выбора, т.е. со списком. Указывается модель, данные из которой будут доступны для выбора