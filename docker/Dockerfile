# Agentic Framework Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal for production)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV AGENTIC_FRAMEWORK_ROOT=/app
ENV ENVIRONMENT=production

# Create data and logs directories
RUN mkdir -p /app/data /app/logs

# Expose port for API (if needed)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from scripts.simple_env import setup_simple_env; setup_simple_env(); print('OK')" || exit 1

# Default command - run the comprehensive test suite
CMD ["python", "tests/complete_test.py"]
