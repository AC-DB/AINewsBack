import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import Optional
import httpx
from ainewsback.core.config import settings


class DingTalkRobot:
    """钉钉机器人工具类"""

    def __init__(self, webhook_url: str, secret: Optional[str] = None):
        """
        初始化钉钉机器人

        Args:
            webhook_url: 钉钉机器人 webhook 地址
            secret: 加签密钥(可选,推荐使用)
        """
        self.webhook_url = webhook_url
        self.secret = secret

    def _get_signed_url(self) -> str:
        """生成加签后的 URL"""
        if not self.secret:
            return self.webhook_url

        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')

        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256
        ).digest()

        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        return f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"

    async def send_text(self, content: str, at_mobiles: Optional[list] = None,
                       at_all: bool = False) -> tuple[bool, str]:
        """
        发送文本消息

        Args:
            content: 消息内容
            at_mobiles: @的手机号列表
            at_all: 是否@所有人

        Returns:
            (是否成功, 消息)
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }

        return await self._send_request(data)

    async def send_markdown(self, title: str, text: str,
                           at_mobiles: Optional[list] = None,
                           at_all: bool = False) -> tuple[bool, str]:
        """
        发送 Markdown 消息

        Args:
            title: 消息标题
            text: Markdown 格式的消息内容
            at_mobiles: @的手机号列表
            at_all: 是否@所有人

        Returns:
            (是否成功, 消息)
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }

        return await self._send_request(data)

    async def _send_request(self, data: dict) -> tuple[bool, str]:
        """发送请求到钉钉"""
        try:
            url = self._get_signed_url()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0
                )

                result = response.json()

                if result.get("errcode") == 0:
                    return True, "发送成功"
                else:
                    error_msg = result.get("errmsg", "未知错误")
                    return False, f"发送失败: {error_msg}"

        except httpx.TimeoutException:
            return False, "发送超时"
        except Exception as e:
            return False, f"发送异常: {str(e)}"


class VerificationNotifier:
    """验证码通知服务"""

    def __init__(self):
        self.robot = DingTalkRobot(
            webhook_url=settings.DINGTALK_WEBHOOK_URL,
            secret=settings.DINGTALK_SECRET
        )

    async def send_verification_code(self, mobile: str, code: str,
                                    scene: str = "login") -> tuple[bool, str]:
        """
        发送验证码通知

        Args:
            mobile: 手机号
            code: 验证码
            scene: 场景(login/register/reset_password)

        Returns:
            (是否成功, 消息)
        """
        scene_map = {
            "login": "登录",
            "register": "注册",
            "reset_password": "重置密码"
        }

        scene_text = scene_map.get(scene, "操作")

        # 文本消息
        content = f"【验证码通知】\n手机号: {mobile}\n验证码: {code}\n场景: {scene_text}\n有效期: {settings.CODE_EXPIRE_SECONDS // 60}分钟"

        return await self.robot.send_text(content)

    async def send_markdown_code(self, mobile: str, code: str,
                                scene: str = "login") -> tuple[bool, str]:
        """发送 Markdown 格式的验证码通知"""
        scene_map = {
            "login": "登录",
            "register": "注册",
            "reset_password": "重置密码"
        }

        scene_text = scene_map.get(scene, "操作")

        title = "验证码通知"
        text = f"""### {title}
> **手机号:** {mobile}  
> **验证码:** `{code}`  
> **场景:** {scene_text}  
> **有效期:** {settings.CODE_EXPIRE_SECONDS // 60}分钟  
"""

        return await self.robot.send_markdown(title, text)