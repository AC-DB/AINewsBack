from typing import Iterable, List, Set

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ainewsback.schemas.base import resp
from ainewsback.utils.jwt import JWTUtils


class AuthMiddleware(BaseHTTPMiddleware):
    """认证中间件: 验证请求是否携带有效 JWT"""

    def __init__(self, app,
                 exclude_paths: Iterable[str] | None = None) -> None:
        """
        Args:
            app: FastAPI 应用实例
            exclude_paths: 无需认证的路径
        """
        super().__init__(app)
        # 存储为集合便于快速精确匹配和前缀匹配
        default_paths: List[str] = [
            "/user/api/v1/login/*",
            "/",
            "/info",
            "/docs",
            "/redoc",
            "/openapi.json",
        ]
        path = exclude_paths or default_paths

        self._prefix_paths: List[str] = []
        self._exclude_paths: Set[str] = set()

        for path in path:
            if path.endswith("*"):
                self._prefix_paths.append(path[:-1])
            else:
                self._exclude_paths.add(path)

    def _is_excluded(self, path: str) -> bool:
        if path in self._exclude_paths:
            return True
        return any(path.startswith(prefix) for prefix in self._prefix_paths)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if self._is_excluded(path):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            return JSONResponse(
                status_code=401,
                content=resp(code=401, message="没有Authorization").model_dump()
            )

        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return JSONResponse(
                status_code=401,
                content=resp(code=401, message="没有bearer信息").model_dump()
            )

        try:
            payload = JWTUtils.verify_token(token)
        except ValueError:
            return JSONResponse(
                status_code=401,
                content=resp(code=401, message="未授权").model_dump()
            )

        # 将解析后的载荷附加到请求上下文
        request.state.jwt_payload = payload
        return await call_next(request)
