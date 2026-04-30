# Stage 1: Build Vue frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/client
COPY client/package.json client/package-lock.json* ./
RUN npm install
COPY client/ .
RUN npm run build

# Stage 2: Python backend + serve frontend
FROM python:3.12-slim
WORKDIR /app

# Install Node.js for hermes CLI compatibility
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY server/requirements.txt ./server/
RUN pip install --no-cache-dir -r server/requirements.txt

# Copy server code
COPY server/ ./server/

# Copy built frontend
COPY --from=frontend-build /app/client/dist ./client/dist

# Create hermes home directory
RUN mkdir -p /root/.hermes/memory /root/.hermes/skills /root/.hermes/sessions /root/.hermes/logs

ENV HERMES_HOME=/root/.hermes
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "server/main.py"]
