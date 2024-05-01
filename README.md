# Тренировочный проект "Parsers"

# Разработчик: Печурин Кирилл

## Предварительная настройка

##### Создать файл ``.env.dev`` в корне проекта в соответствии с `.env.src` в корне проекта
##### Создать файл ``.env.dev`` в frontend/ в соответствии с `.env.src` в frontend/
##### Создать файл ``.env.dev`` в backend/ в соответствии с `.env.src` в backend/

##### Ознакомиться с проектом

## Скрипты

#### Сборка и запуск контейнеров

```
docker-compose --env-file .env.dev up -d --build
```

#### Сайт доступен по `localhost:8081`

#### Загрузка первоначальных данных

```
docker-compose exec backend python3 loaddata.py fixtures/init_data.json
```

#### Для корректной работы со storage и static

```
docker-compose exec backend python3 create_dirs.py
```


## Дополнительные скрипты для корректной работы с mongodb

## Дополнительные скрипты для работы с mongodb

### Вход в контейнер

```
docker exec -it ds-parsers-mongodb bash
```

### Переход к mongo

```
mongo
```

### Проверка на создание пользователя
#### Версия mongodb поддерживает создание пользователя через env-переменные. Но пользователь может создастся не сразу

```
db.auth("<username>", "<password>");
```

### Если authentication failed. 
- Выйти из контейнера: `exit;`
- Удалить все контейнеры: `docker-compose down -v` 
- Заново запустить сборку, зайти в контейнер и проверить через аутентификацию

#### БД создается не сразу, а только тогда, когда запишутся первые данные

### Просмотр всех БД

```
show dbs
```

## Структура проекта
- backend
  - app - Все, что связано с самим приложением
    - dependences - Зависимости
    - exception_handlers - Обработчики ошибок
    - models - Модели 
    - routers - роуты
  - fixtures - начальные данные
    - bootstrap - загрузка начальных данных
  - management - менеджмент проекта
    - commands - команды для менеджмента
  - src - исходники
    - biz - бизнес логика (сервисы, ошибки)
    - bootstrap - подгрузка приложения
    - cel - работа с celery
    - parsers - блок парсинга
    - utils - утилиты
  - static
  - storage
  - .env.backend - переменные
  - .env.src - исходный файл, как должны выглядеть переменные
  - .gitignore
  - create_dirs.py - создание папок
  - Dockerfile
  - geckodriver.log - логи работы с парсингом
  - loaddata.py - загрузка начальных данных
  - main.py - главный файл приложения
  - requirements.txt - зависимости
- frontend
  - src - исходники
    - bootstrap - подгрузка приложения
    - services - сервисы
  - templates - шаблоны
  - views - вьюхи
  - .env.frontend - переменные
  - .env.src - исходный файл, как должны выглядеть переменные
  - Dockerfile
  - main.py - главный файл приложения
  - requirements.txt - зависимости
- mongodb
  - mongo-init.js - создание пользователя
- nginx
  - nginx-setup.conf - конфиг nginx
