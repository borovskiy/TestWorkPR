FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Устанавливаем uv
RUN pip install uv

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости через uv
RUN uv sync --frozen --no-cache

# Копируем весь код
COPY . .

# Устанавливаем PYTHONPATH для корректных импортов
ENV PYTHONPATH=/app:/app/app

# Команда запуска (предполагается, что ваш app в папке app/)
CMD ["uv", "run", "python", "-m", "app.main"]
