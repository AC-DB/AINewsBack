from datetime import datetime, timedelta, timezone
import jwt
from ainewsback.config import settings

class JWTUtils:
    @staticmethod
    def create_token(data: str) -> str:
        """生成JWT令牌"""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": data,
            "iat": now,
            "exp": expire,
            "jti": f"jwt_{data}_{now}",
            "iss": settings.CURRENT_ISSUER,
            "aud": settings.TOKEN_AUDIENCE,
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> dict:
        """验证JWT令牌并返回载荷"""
        try:
            payload = jwt.decode(
                jwt = token,
                key = settings.SECRET_KEY,
                algorithms = [settings.ALGORITHM],
                options = {
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_iss": True,
                    "verify_aud": True,
                    "require": ["sub", "iat", "exp", "jti", "iss", "aud"]
                },
                issuer = settings.ACCESS_TOKEN_ISSUER,
                audience = settings.CURRENT_ISSUER,
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token已过期")
        except jwt.MissingRequiredClaimError as e:
            raise ValueError(f"缺少必需的字段：{e.claim}")
        except jwt.InvalidIssuerError:
            raise ValueError("无效的颁发者")
        except jwt.InvalidAudienceError:
            raise ValueError("无效的受众")
        except jwt.InvalidTokenError:
            raise ValueError("无效的Token")

    @staticmethod
    def extract_data(token: str) -> dict:
        """从JWT中提取数据"""
        payload = JWTUtils.verify_token(token)
        return payload

