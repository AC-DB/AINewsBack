import uvicorn
from fastapi import FastAPI

from ainewsback.api.v1 import router
from ainewsback.config import settings
from ainewsback.middleware import AuthMiddleware


def create_app():
    _app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        contact=settings.ADMIN_CONTACT,
        license_info=settings.APP_LICENSE,
        debug=settings.DEBUG
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
