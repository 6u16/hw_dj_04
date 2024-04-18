from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


# Потребуется добавить дополнительную проверку при сохранении объекта. Для этого в объекте Inline можно переопределить атрибут formset, который должен указывать на
# специальный класс типа BaseInlineFormSet, нужный для обработки списка однотипных форм, каждая для своей связи. Примером с
# переопределением метода clean, указанного в качестве formset класса:
class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            form.cleaned_data
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
            raise ValidationError('Основной тег может быть только один')
        return super().clean()  # вызываем базовый код переопределяемого метода


# Создание инлайн модели для встраивания отображения в текущую модель ДРУГОЙ ТАБЛИЦЫ
class TagArticleInline(admin.TabularInline):  # TabularInline, StackedInline - отличаются только внешним видом
    model = Scope  # модель, для которой инлайн встраивается = OrderPosition
    extra = 3  # Параметр добавляющий строки в новой таблице ADD ORDERS + -> ORDER POSITIONS
    formset = RelationshipInlineFormset
# Инлайн сделали и переходим в настроика отображения нашей модели OrderAdmin

@admin.action(description="Редактировать статью")  # Не разобрался как добавить действие редактирования статьи!!!
def change_article(modeladmin, request, queryset):
    queryset.update()
    
    
@admin.register(Tag)  # С помощью декоратора зарегистрируем управление 
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']  # настроика отображения в браузере
    list_filter = ['name']  # у нас появится окно фильтра
    

@admin.register(Article)  # С помощью декоратора свяжем с моделью Order
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','text','published_at','image']  # настроика отображения в браузере
    inlines = [TagArticleInline]  # Указываем какие встраиваемые(инлайн) позиции будем отображать
    actions = [change_article]
    