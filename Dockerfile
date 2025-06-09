# Используем официальный Python-образ
FROM python:3.10-slim

# Установим ODBC Driver 17 и зависимости
RUN apt-get update && \
    apt-get install -y curl gnupg apt-transport-https unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установим Python-зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app
WORKDIR /app

# Запускаем FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
