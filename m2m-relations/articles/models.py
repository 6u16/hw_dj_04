from django.db import models


# Класс тэга:
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):  # Добавление этой функции позволит отображать имена объектов, а не TagObject(1...)
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    tags = models.ManyToManyField(Tag, related_name='tag')    # Связь многие ко многим, так как в article может быть множество tag и один и тот же tag может быть во многих article
                                                                # Так же реализуется через промеж.таблицу и каскадное удаление стоит по умолчанию.
                                                                # related_name='tag' - так мы можем из самого article тоже обратиться к tag и посмотреть article

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


# Создадим промежуточную таблицу для указания цели статьи
class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')  # Внешний ключ связанный с Article, обращаться можно через scopes
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')  # Внешний ключ связанный с Tag, обращаться можно через scopes
    is_main = models.BooleanField(verbose_name='Основной тег')  # Булевое значениие, главный ли tag
# В этой таблице ручками вбиваем набор tag которые относятся к article и в поле is_main(bool) указываем какой тег главный


# До регистрации миграций нужно будет установить python -m pip install Pillow, требуется для ImageField
# python manage.py makemigrations
# python manage.py migrate
# python manage.py loaddata articles.json  - Загрузка данных в БД