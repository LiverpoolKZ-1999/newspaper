FROM python:3.10-buster
LABEL maintainer="nayapbergen@gmail.com"

# Ensure consistent and compatible architecture
RUN export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Environment variables to prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Install build dependencies and clean up in a single RUN command to minimize layers
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    libev-dev \
    gcc \
    htop \
    wkhtmltopdf \
    && pip install --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the requirements file first to leverage Docker's caching mechanism
COPY ./requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create static and media directories
RUN mkdir -p /static /media

# Copy the application code
COPY . /app

# Expose the desired port
EXPOSE 8011

# Copy entrypoint scripts and make them executable
COPY entrypoints /scripts/
RUN chmod +x /scripts/*
