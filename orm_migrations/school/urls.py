from django.urls import path

from school.views import students_list

# Добавим дебагер для отладки
import debug_toolbar
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path('', students_list, name='students'),
    path('__debug__/', include(debug_toolbar.urls)),  # Джанго отладчик в браузере
]
