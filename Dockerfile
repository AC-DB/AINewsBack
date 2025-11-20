# Dockerfile
# 多阶段构建：builder 阶段安装依赖并构建包，final 阶段只包含运行时文件
FROM python:3.13-slim AS builder

LABEL authors="A-bcd"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 安装系统依赖，用于编译扩展（必要时可删减）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc git libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先复制元数据以便缓存依赖安装
COPY pyproject.toml pyproject.toml
# lock 文件一并复制，例如 poetry.lock 或 pip-tools 导出的 requirements.txt，可提高缓存命中率
COPY poetry.lock poetry.lock

# 复制全部源代码（如需排除可用 .dockerignore）
COPY . .

# 升级 pip 并安装包（通过 pyproject 安装项目）
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir .

# 运行时镜像：仅拷贝需要的内容
FROM python:3.13-slim AS final
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# 把已安装的依赖从 builder 复制过来（镜像 Python 版本必须一致）
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
# 可执行文件
COPY --from=builder /usr/local/bin /usr/local/bin
# 复制应用代码
COPY --from=builder /app /app

# 暴露容器内端口
EXPOSE 8080

# 启动命令
CMD ["uvicorn", "ainewsback.main:app", "--host", "0.0.0.0", "--port", "8080"]