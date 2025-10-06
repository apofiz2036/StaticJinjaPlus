FROM ubuntu:22.04

# Установим питон, venv и git
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip git \
    && rm -rf /var/lib/apt/lists/*

# Задаём рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальной код
COPY . .

# Запускаем
CMD ["python3", "main.py"]