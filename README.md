
# Coffee Backend API ☕

## 📌 Описание
Проект представляет собой backend-сервис для кофейни, реализованный на FastAPI.  
Функциональность включает регистрацию и верификацию пользователей, оформление заказов, корзину, меню, а также фильтрацию и пагинацию.

---

## 🚀 Возможности

### 👤 Управление пользователями
- Регистрация и вход с использованием JWT
- Верификация по коду (выводится в консоль)
- Автоматическая очистка неподтвержденных пользователей через 2 дня (реализовано через Celery)

### 📦 Управление заказами
- Создание и просмотр заказов
- CRUD-операции
- Привязка к пользователю и корзине

### 📋 Меню
- Категории и позиции меню
- CRUD-операции
- Привязка товаров к категориям

### 🛒 Корзина
- Добавление, удаление и обновление товаров
- Привязка к пользователю
- Создание заказа из корзины

### 🔍 Фильтрация и пагинация
- Поиск по названию (меню, категории)
- Пагинация (`limit`, `offset`)

---

## ⚙️ Технологии
- **Python 3.12**
- **FastAPI**
- **SQLAlchemy (async)**
- **Alembic**
- **PostgreSQL**
- **JWT (auth)**
- **Celery + Redis**
- **Docker + Docker Compose**

---

## 📂 Установка и запуск

### 1. Клонируй репозиторий:
```bash
git clone https://github.com/your-username/coffee-backend.git
cd coffee-backend
```

### 2. Запуск с помощью Docker:
```bash
docker-compose up --build
```

### 3. Применить миграции:
```bash
docker-compose exec backend alembic upgrade head
```

---

## 🧪 Тестирование
```bash
pytest
```

---

## 🛠️ Структура проекта (упрощённо)
```
├── app
│   ├── api                # FastAPI routers
│   ├── core               # Configuration, settings, security
│   ├── db                 # DB session, initialization, Alembic
│   ├── models             # SQLAlchemy models
│   ├── schemas            # Pydantic schemas
│   ├── services           # Business logic
│   ├── main.py            # FastAPI entry point
│   └── tasks.py           # Background task logic
│
├── celery_worker.py        # Celery app & routes
├── celery_beat_schedule.py # Celery Beat schedule config
├── docker-compose.yml      # Docker Compose config
├── Dockerfile              # Dockerfile for the app
├── .env                    # Environment variables
├── alembic.ini             # Alembic migration config
├── requirements.txt        # Project dependencies
├── README.md               # This file
└── venv/                   # Local virtual environment (excluded in Docker)
```

---

## 🧹 Очистка неподтвержденных пользователей
Фоновая задача Celery автоматически удаляет пользователей, которые не подтвердили регистрацию в течение 2 дней.

---

## 📬 Верификация
Код подтверждения выводится в консоль (эмуляция email/SMS отправки).
---

