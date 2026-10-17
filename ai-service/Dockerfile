FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 NLTK_DATA=/usr/local/share/nltk_data
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && python -m nltk.downloader -d /usr/local/share/nltk_data stopwords
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
