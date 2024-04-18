from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'

    # используйте .order_by('') параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    
    # Установить pip install django-debug-toolbar(полная инструкция в Python_Django) для анализа числа SQL запросов, выбрать оптимальный результат для задачи с отношением ManyToManyField
    
    #stud_obj = Student.objects.order_by('name')  # Обычное обращение к БД, SQL queries = 4 (3.75ms)
    stud_obj = Student.objects.prefetch_related('teachers')  # обращение с минимальным числом SQL запросов в связке таблиц ManyToManyField (документация prefetch_related()), SQL queries = 2 (2.18ms)
    context = {'object_list':stud_obj}

    return render(request, template, context)
