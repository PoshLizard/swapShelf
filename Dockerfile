FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data && chmod 777 /app/data
ENV DATABASE_PATH=/app/data/swapshelf.db
ENV PORT=3000
EXPOSE 3000
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed && gunicorn --bind 0.0.0.0:3000 swapshelf.wsgi"]
