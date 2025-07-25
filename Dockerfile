
# Stage 1: Install frontend
FROM node:20 AS frontend-build
WORKDIR /app
COPY dashboard/frontend ./
RUN npm install && npm run build

# Stage 2: Python backend
FROM python:3.11-slim
WORKDIR /app

# Backend dependencies. Review the requirements.txt before prod.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and built frontend
COPY . ./
COPY --from=frontend-build /app/dist ./dashboard/frontend/dist

# Expose FastAPI port
EXPOSE 8000

# Start API
CMD ["uvicorn", "dashboard.app:app", "--host", "0.0.0.0", "--port", "8000"]
