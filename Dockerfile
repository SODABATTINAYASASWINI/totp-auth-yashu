############################
# Stage 1: Builder
############################
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


############################
# Stage 2: Runtime
############################
FROM python:3.11-slim

# Set timezone to UTC
ENV TZ=UTC

WORKDIR /app

# Install cron + timezone data
RUN apt-get update \
    && apt-get install -y --no-install-recommends cron tzdata \
    && ln -snf /usr/share/zoneinfo/UTC /etc/localtime \
    && echo UTC > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY . .

# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose API port
EXPOSE 8080

# Start cron + API server
CMD cron && python app.py
