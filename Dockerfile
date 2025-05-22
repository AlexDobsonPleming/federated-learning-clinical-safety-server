FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build-time tools and dos2unix
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libpq-dev dos2unix \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Copy all app code AND your entrypoint script
COPY . /app/

# Normalize line endings and make it executable
RUN dos2unix /app/docker-entrypoint.sh \
  && chmod +x /app/docker-entrypoint.sh

# This is the one and only entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# You can still have a default CMD if you like, but your script
# ends by exec’ing runserver, so CMD is actually ignored.
CMD ["gunicorn", "federated_learning_clinical_safety_server.wsgi:application", "--bind", "0.0.0.0:8000"]
