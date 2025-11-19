import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from ainewsback.api.v1 import router
from ainewsback.core.config import settings
from ainewsback.core.reids import AsyncRedisClient
from ainewsback.middleware import AuthMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logging.info("应用启动，初始化 Redis 连接...")
    redis_client = await AsyncRedisClient.get_client()
    try:
        await redis_client.ping()
        logging.info("Redis 连接成功")
    except Exception as e:
        logging.error(f"Redis 连接失败: {e}")

    yield

    # 关闭时
    logging.info("应用关闭，清理资源...")
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
    # 注册路由
    _app.include_router(router)

    return _app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=True if settings.APP_ENV == "dev" else False)
