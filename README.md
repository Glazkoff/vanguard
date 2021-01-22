# Авангард

## Как установить в virtualenv зависимости проекта 

```
pip install -r requirements.txt
python manage.py collectstatic
```

## Полезные ссылки

### Новые стили для административной панели 
[Разные шаблоны для админки джанго (есть бесплатные и с мобильной версией)](https://appseed.us/admin-dashboards/django?ref=dev) <br>
[Про переопределение стилей](https://stackoverflow.com/questions/7357057/overriding-admin-css-in-django) <br>
[Тоже про новые стили](https://medium.com/@brianmayrose/django-step-9-180d04a4152c) <br>

### Генерация документов
[Как генерировать документы по шаблонам](http://morozov.ca/django-pdf-msword-excel-templates.html) <br>
[Библиотека для генерации pdf ](https://www.reportlab.com/dev/opensource/) <br>
[python-docx-template](https://docxtpl.readthedocs.io/en/latest/) (насколько я поняла - может изменять готовые шаблоны документов, заполняя их нужными данными) <br>

### Интернационализация
[Официальная документация](https://docs.djangoproject.com/en/3.1/topics/i18n/)
[Django i18n: A beginner’s guide](https://lokalise.com/blog/django-i18n-beginners-guide/)
[A Quick Guide to Django i18n](https://phrase.com/blog/posts/quick-guide-django-i18n/)

### Валидация
[Официальная документация](https://docs.djangoproject.com/en/3.1/ref/models/instances/#validating-objects)

### Пример, который используется для вывода сотрудников 
```
class MyModelAdmin(admin.ModelAdmin):
def queryset(self, request):
qs = super(MyModelAdmin, self).queryset(request)
if request.user.is_superuser:
return qs
return qs.filter(author=request.user)
``` 
