# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app
# Copy code
COPY . .

# Cài đặt dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000
# Chạy FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]