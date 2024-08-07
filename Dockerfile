FROM python:3.10.12

# Set environment variables
ENV PYTHONBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install dependencies
RUN apt update && apt upgrade -y && apt install -y build-essential libssl-dev

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copy the application code
COPY . /app/

# Copy and make the entrypoint script executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command to run the application
# CMD ["gunicorn", "--timeout", "120", "-k", "gevent", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "Hoinky.asgi"]
CMD ["daphne", "-u", "/tmp/daphne.sock", "--bind", "0.0.0.0", "--port", "8000", "Hoinky.asgi:application"]
