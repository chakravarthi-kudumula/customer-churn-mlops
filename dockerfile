# 1. Base image (lightweight Python)
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Copy necessary things only (including model/)
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY app/ ./app/
COPY artifacts/ ./artifacts/

# 6. Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# 7. Expose FastAPI port
EXPOSE 8000

# 8. Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]