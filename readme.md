# FastAPI hotels backend
![Static Badge](https://img.shields.io/badge/Coverage-93%25-brightgreen)
## О проекте
Проект представляет собой backend веб-приложения для поиска и бронирования отелей. Целью проекта является разработка fullstack приложения для работы с современными технологиями используемыми при разработке веб-приложений. Ссылка на фронтенд тут

## Features

- Поиск и бронирование отелей
- Асинхронное API разработанное на **FastAPI**
- Интерактивная документация **Swagger**
- Аутентификация и авторизация на основе **JWT токенов**
- Обработка фоновых задач с помощью **Celery**
- Отображение фоновых задач в веб-интерфейсе с помощью **Flower**
- Кэширование данных с помощью **Redis**
- Мониторинг состояния приложения в реальном времени благодаря **Prometheus** и **Grafana**
- Веб-интерфейс админки
- Контейнеризация с помощью **Docker** и **docker-compose**
- Уведомления об ошибках в telegram администратора
- Фронтенд приложение на **React**

## Скриншоты приложения
Так как сейчас довольно трудно найти полностью бесплатный хостинг для разворачивания докер контейнеров я не деплоил приложение. Поэтому для демонстрации прилагаю скриншоты

1. Документация API
<img width="1920" alt="swagger-example" src="https://github.com/krevedkin/fastapi_hotels/assets/70909877/d1f96497-a8f4-422c-9fae-59bbd1d15ead">

2. Интерфейс панели администратора
<img width="1022" alt="admin-example" src="https://github.com/krevedkin/fastapi_hotels/assets/70909877/519eff34-884d-486a-8a18-342a54a42a21">

3. Интерфейс Flower для отслеживания состояния Celery задач
<img width="1919" alt="flower-example" src="https://github.com/krevedkin/fastapi_hotels/assets/70909877/e7c912ab-4800-4415-9e4c-bd00f940a524">

4. Dashboard Grafana для мониторинга состояния приложения
<img width="1920" alt="dashboard-example" src="https://github.com/krevedkin/fastapi_hotels/assets/70909877/c91be75b-4a02-445b-8c0e-500608cf154f">

5. Пример главной страницы frontend приложения, больше скриншотов тут
<img width="1917" alt="forntend-example-home" src="https://github.com/krevedkin/fastapi_hotels/assets/70909877/ebc1bdab-472a-4a35-9003-2c2c773713c9">

## Установка
Для установки потребуется **poetry** а также **Docker** и **docker-compose**.

Для локальной разработки вне контейнера 
после клонирования репозитория, находясь в корне проекта, запустить :
```
poetry install
```
После установки зависимостей необходимо собрать образы :
```
docker compose build
```
... и запустить контейнеры:
```
docker compose up
```
После загрузки загрузки контейнеров приложение будет запущено, документация **Swagger** доступна по адресу:

http://localhost:8000/docs

Панель администратора доступна по адресу:

http://localhost:8000/admin

Мониторинг доступен по адресу:

http://localhost:3001/

Порты можно для подключения на хост-машине можно изменить в **docker-compose.yml**

## Настройка дашборда Grafana
<img width="1920" alt="dashboard-example" src="https://github.com/krevedkin/fastapi_hotels/assets/70909877/591d3006-d2a8-4116-a046-df1d68c98060">

Для отображения дэшборда в корне проекта подготовлен файл **grafana-dashboard.json**

После открытия Grafana на порту **3031** появится форма авторизации.
Дефолтные значения

- username: **admin**
- password: **admin**

После ввода данных будет предложено изменить пароль, для разработки можно оставить **admin**

Далее необходимо провести следующие действия:

1. В левой части интерфейса нажать на шестеренку для открытия меню настоек
2. Выбрать пункт **Data sources**
3. В появившемся окне нажать кнопку **Add new data source**
4. Выбрать **Prometheus**
5. Ввести url например http://prometheus:9090 где prometheus это имя контейнера в **docker-compose.yml**
6. Нажать **Save & Test**
7. Далее снова перейти на вкладку **Data sources**
8. Нажать на созданный дэшборд
9. В появившемся окне выбрать вкладку **Dashboards** 
10. Импортировать один из предложенных дашбордов, например Prometheus stats
11. В левой части страницы выбрать пункт меню Dashboards
12. Перейти в только что импортированный дашборд
13. В правом верхнем углу нажать на шестеренку для открытия **Dasboard settings**
14. В левой части выбрать **JSON Model**
15. В появившемся окне сделать поиск сочетанием клавиш **cmd+F** по слову **uid**
16. Скопировать значение **uid** и временно сохранить его где-нибудь.
17. В корне проекта открыть файл **grafana-dashboard.json**
18. Найти все поля **uid** и заменить значение, на то которое мы сохранили ранее.
19. Вновь перейти в браузер и открыть **Dashboards -> FastAPI Hotels - Бронирование отелей**
20. Выбрать **Dasboard settings** (правый верхний угол)
21. Открыть **JSON Model** и передать туда файл **grafana-dashboard.json** либо можно скопировать содержимое файла и вставить в форму, после чего нажать **Save changes**
22. **Dasboard** готов

### Важно!
В файле **prometheus.yml** указаны настройки **prometheus** если контейнер с **FastAPI** был переименован, то также необходимо указать это в:
```
static_configs:
      - targets: ['имя_контейнера:8000']
```
И для корректной работы дашборда в файле **grafana-dashboard.json** поля **expr** должны содержать **job=\"web\"** где web - **job_name** из **prometheus.yml**
```
global:
  scrape_interval: 15s

  external_labels:
    monitor: 'codelab-monitor'

scrape_configs:
  - job_name: 'prometheus'

    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'web' <-----------ВОТ ЭТО ИМЯ!
    scrape_interval: 5s

    static_configs:
      - targets: ['web:8000']
```

## Запуск тестов

Для тестрирования подготовлен отдельный файл **docker-compose.test.yaml**

Для запуска контейнеров сделать:
```
docker compose -f docker-compose.test.yaml build
docker compose -f docker-compose.test.yaml up
```

Это создаст среду для прогона тестов.

Для запуска тестов использовать команду:
```
docker compose -f docker-compose.test.yaml exec test_web pytest
```
где **test_web** имя тестового контейнера **FastAPI**.

Для того чтобы не прописывать постоянно длинную команду можно создать таску в **VScode** например:

```
{
            "label": "test docker-compose down",
            "type": "shell",
            "command": "docker-compose",
            "args": [
                "-f",
                "docker-compose.test.yaml",
                "down",
            ],
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "run tests in docker",
            "type": "shell",
            "command": "docker-compose",
            "args": [
                "-f",
                "docker-compose.test.yaml",
                "exec",
                "test_web",
                "pytest",
                "-v",
                "-s",
                "--cov-report",
                "html",
                "--cov",
                ".",
                "-m",
                "images",
                "--disable-warnings"
            ],
            "group": {
                "kind": "test",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": []
        }
```
После чего тесты можно будет запускать нажатием **CMD+SHIFT+P**  и выбрать **Tasks: Run Test Task**

В поле **args** можно перечислить необходимые параметры для запуска **pytest** например указать какие тесты будут запущены, с помощью ***"-m" "название группы тестов"*** доступные имена групп:
- **auth**
- **images**
- **hotels**
- **bookings**
- **rooms**

Для проверки покрытия кода тестами можно добавить в таску аргументы:
```
"--cov-report",
"html",
"--cov",
".",
```
Это создаст директорию **htmlcov** в корне проекта, открыв файл **index.html** можно оценить процент покрытия кода тестами.


При запуске тестов запускается фикстура **conftest.prepare_database** база данных тестового контейнера полностью зачищается и заполняется данными из **.sql** файлов директории **mock_data**, а также там содержится тестовое изображение. Все эти файлы необходимы для успешного прогона тестов.


### Отправка уведомлений об ошибках в telegram

Для этого необходимо получить токен для бота у BotFater в telegram, после чего сохранить токен в .env файл, а также указать chat_id администратора которому должны приходить уведомления в модуле **middleware.py**

Пример вывода сообщений от бота:
<img width="762" alt="telegram-example" src="https://github.com/krevedkin/fastapi_hotels/assets/70909877/1d2e92bc-a8ab-4031-8016-454c735eca2a">


