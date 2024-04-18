from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    subject = models.CharField(max_length=10, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    #teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Было
    teachers = models.ManyToManyField(Teacher, related_name='students')  # Стало
    group = models.CharField(max_length=10, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return self.name
    
# Загрузка данных в модели прямиком из файла .json
# python manage.py loaddata school.json

# После загрузки произведена смена поля teachers (class Student) с ForeignKey на связь ManyToManyField, изменения применены, в БД появляется новая промежуточная таблица school_student_teachers,
# а поле отношения teacher_id у Student которое было при ForeignKey удалится.

# Необходимо в новой промежуточной таблице school_student_teachers самостоятельно добавить отношения student_id к teacher_id