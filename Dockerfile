# /home/siisi/e-commerce/Dockerfile

# 1. Base image
FROM python:3.12.0

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Create work directory
WORKDIR /app

# 4. Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 6. Copy project code
COPY . /app/

# 7. Collect static files
RUN python manage.py collectstatic --noinput

# 8. Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# 9. Default command
CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8005"]
