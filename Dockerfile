# Build stage
FROM node:20-alpine as builder
WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci
COPY client/ .
RUN npm run build

# Runtime stage
FROM python:3.11-slim
WORKDIR /app

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ .
COPY --from=builder /app/client/dist /app/static

ENV HERMES_DATA_PATH=/hermes-data
ENV JWT_SECRET=hermes-webui-pro-secret-key-2024
ENV LOGIN_PASSWORD=hermes2024

EXPOSE 8090

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]