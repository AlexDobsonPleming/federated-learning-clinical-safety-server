# Dockerfile

# 1. Start from the official slim Python image
FROM python:3.10-slim

# 2. Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create and set the working directory
WORKDIR /app

# 4. Install system dependencies for psycopg2 (Postgres driver) and build tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/

# 6. Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of the application code
COPY . /app/

# 8. Apply database migrations automatically at container start
ENTRYPOINT ["sh", "-c", "python manage.py migrate --noinput && exec \"$@\"", "--"]

# 9. Default command: run the Django development server
CMD ["gunicorn", "federated_learning_clinical_safety_server.wsgi:application", "--bind", "0.0.0.0:8000"]

# Copy your entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

# Make it executable
RUN chmod +x /app/docker-entrypoint.sh

# set it as the default entrypoint—otherwise Compose’s entrypoint will override it
ENTRYPOINT ["/app/docker-entrypoint.sh"]