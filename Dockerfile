# Используйте официальный образ Python
FROM python:3.11

# Установите рабочую директорию
WORKDIR /app

# Скопируйте все файлы проекта в контейнер
COPY . .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Установите точку входа
ENTRYPOINT ["./docker-entrypoint.sh"]
