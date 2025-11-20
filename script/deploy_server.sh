#!/bin/bash

# 服务器部署脚本
set -e

IMAGE_NAME="ainewsback"
IMAGE_TAG="latest"
DOCKER_USER="acdb24"
FULL_IMAGE="$DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG"
COMPOSE_FILE="docker-compose.server.yml"

echo "==> 拉取最新镜像: $FULL_IMAGE"
docker pull "$FULL_IMAGE"

echo "==> 停止旧服务"
docker compose -f "$COMPOSE_FILE" down

echo "==> 启动服务"
docker compose -f "$COMPOSE_FILE" up -d

echo "==> 查看运行状态"
docker compose -f "$COMPOSE_FILE" ps

echo "==> 查看后端日志（Ctrl+C 退出）"
docker compose -f "$COMPOSE_FILE" logs -f backend