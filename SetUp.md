## Развёртывание проекта:
+ Клонировать репозиторий и перейти в него в командной строке:
```shell script
git clone git@github.com:Furturnax/django_testing.git
```

```shell script
cd django_testing/
```

+ Cоздать и активировать виртуальное окружение (Windows/Bash):
```shell script
python -m venv venv
```

```shell script
source venv/Scripts/activate
```

+ Установить зависимости из файла requirements.txt:
```shell script
python -m pip install --upgrade pip
```

```shell script
pip install -r requirements.txt
```

<br>

## Тестирование проекта:
### Unittest
+ Перейти в директорию проекта `ya_note`:
```shell script
cd ya_note/
```
+ Запустить тесты:
```shell script
python manage.py test
```

### Pytest
+ Перейти в директорию проекта `ya_news`:
```shell script
cd ya_news/
```
+ Запустить тесты:
```shell script
pytest
```
