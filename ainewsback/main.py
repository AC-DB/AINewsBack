import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from ainewsback.api.v1 import router
from ainewsback.core.config import settings
from ainewsback.core.logger import setup_logging
from ainewsback.core.reids import AsyncRedisClient
from ainewsback.middleware import AuthMiddleware
from ainewsback.middleware.logging_middleware import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时

    # 初始化日志
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"应用启动 - 环境: {settings.APP_ENV}")
    logger.info(f"当前时间: 2025-11-19 00:17:00 UTC")
    logger.info(f"当前用户: AC-DB")

    logger.info("应用启动，初始化 Redis 连接...")
    redis_client = await AsyncRedisClient.get_client()
    try:
        await redis_client.ping()
        logger.info("Redis 连接成功")
    except Exception as e:
        logger.error(f"Redis 连接失败: {e}")

    yield

    # 关闭时
    logger.info("应用关闭，清理资源...")
    await AsyncRedisClient.close()

def create_app():
    _app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        contact=settings.ADMIN_CONTACT,
        license_info=settings.APP_LICENSE,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    # 认证中间件
    _app.add_middleware(AuthMiddleware)
    # 日志中间件
    _app.add_middleware(LoggingMiddleware)
    # 注册路由
    _app.include_router(router)

    return _app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=True if settings.APP_ENV == "dev" else False,
                log_config=None)
