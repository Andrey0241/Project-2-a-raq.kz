Вот пример `README.md` файла для вашего проекта:

```markdown
# MyApp

Это приложение на Python с использованием Flask и PostgreSQL для управления пользователями и объявлениями.

## Установка




1. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Настройте базу данных:**

   Убедитесь, что у вас установлен PostgreSQL и создана база данных. Используйте следующие параметры подключения:

   ```plaintext
   username: ROOT
   password: ROOT
   database name: Main
   ```

5. **Создайте таблицы:**

   Запустите приложение один раз, чтобы создать необходимые таблицы:

   ```bash
   python app.py
   ```

   После этого вы можете остановить сервер (Ctrl + C).

## Запуск приложения

Запустите приложение с помощью следующей команды:

```bash
python app.py
```

Приложение будет доступно по адресу [http://localhost:5000](http://localhost:5000).

## Использование API

### Регистрация пользователя

**POST** `/auth/users/`

Пример запроса:

```json
{
    "username": "test@gmail.com",
    "phone": "+7 700 698 5025",
    "password": "12345678",
    "name": "Далида Е.",
    "city": "Алматы"
}
```

### Вход пользователя

**POST** `/auth/users/login`

Пример запроса:

```plaintext
username=test@gmail.com&password=12345678
```

### Изменение данных пользователя

**PATCH** `/auth/users/me`

Необходим заголовок `Authorization: Bearer {token}`.

Пример запроса:

```json
{
    "phone": "+7 700 698 5025",
    "name": "Далида Е.",
    "city": "Алматы"
}
```

### Получение данных пользователя

**GET** `/auth/users/me`

Необходим заголовок `Authorization: Bearer {token}`.

### Создание объявления

**POST** `/shanyraks/`

Необходим заголовок `Authorization: Bearer {token}`.

Пример запроса:

```json
{
    "type": "rent",
    "price": 150000,
    "address": "Астана, Алматы р-н, ул. Нажимеденова, 16 – Сарыколь",
    "area": 46.5,
    "rooms_count": 2,
    "description": "Продается 1.5 комнатная квартира..."
}
```

### Получение объявления

**GET** `/shanyraks/{id}`

### Изменение объявления

**PATCH** `/shanyraks/{id}`

### Удаление объявления

**DELETE** `/shanyraks/{id}`

### Добавление комментария к объявлению

**POST** `/shanyraks/{id}/comments`

### Получение списка комментариев объявления

**GET** `/shanyraks/{id}/comments`

### Изменение текста комментария

**PATCH** `/shanyraks/{id}/comments/{comment_id}`

### Удаление комментария

**DELETE** `/shanyraks/{id}/comments/{comment_id}`

