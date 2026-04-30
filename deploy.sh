#!/bin/bash
set -e

echo "🚀 部署 Hermes WebUI Pro..."

cd /vol1/1000/docker/hermes/hermes-webui-pro

echo "⏹️  停止容器..."
docker compose down

echo "🔨 构建镜像..."
docker compose build --no-cache

echo "▶️  启动容器..."
docker compose up -d

echo "⏳ 等待启动..."
sleep 10

echo "🔍 检查状态..."
docker compose ps

echo "🧪 测试 API..."
curl -s http://localhost:8090/api/health || echo "API 测试失败"

echo "✅ 部署完成！"
echo "🌐 访问: http://$(hostname -I | awk '{print $1}'):8090"
echo "🔑 密码: hermes2024"