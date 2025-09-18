FROM python:3.10-alpine

# Upgrade pip
# RUN python -m pip install --upgrade pip

# Install packages
RUN apk add --update --no-cache supervisor

# Install dependencies
RUN pip install uvicorn fastapi loguru

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .

# Copy flag
COPY flag /flag.txt

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 1337

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]