from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Імпортуйте ваші моделі тут
from app.models import Base

# Це Alembic Config об'єкт, який надає доступ
# до значень в .ini файлі, що використовується.
config = context.config

# Інтерпретуємо конфігураційний файл для логування в Python.
# Цей рядок налаштовує логгери.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Додайте ваш об'єкт MetaData тут для підтримки 'autogenerate'
target_metadata = Base.metadata

# Інші значення з конфігурації, визначені потребами env.py,
# можуть бути отримані так:
# my_important_option = config.get_main_option("my_important_option")
# ... і так далі.


def run_migrations_offline() -> None:
    """Запуск міграцій в режимі 'offline'.

    Це налаштовує контекст лише з URL і без Engine,
    хоча Engine також можна використовувати тут.
    Пропускаючи створення Engine, ми навіть не потребуємо наявності DBAPI.

    Виклики до context.execute() тут виводять на екран вказаний рядок.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск міграцій в режимі 'online'.

    У цьому сценарії ми створюємо Engine
    і асоціюємо з ним з'єднання з контекстом.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
