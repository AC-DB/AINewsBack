# AI新闻资讯后端

## 项目结构

> 参照的项目结构示例：

```text
AINewsBackFastAPI/
│
├── app/
│   ├── main.py              # 程序入口（FastAPI对象、路由引入等）
│   ├── api/                 # API 路由分组
│   │    ├── v1/
│   │    │    ├── endpoints/ # 细分API模块(如users.py、items.py)
│   │    │    └── __init__.py
│   │    └── __init__.py
│   ├── core/                # 项目核心配置与启动逻辑（如settings.py、security.py等）
│   ├── models/              # Pydantic/ORMar/SQLAlchemy等数据库模型
│   ├── schemas/             # Pydantic数据序列化/校验用schema
│   ├── crud/                # 业务层（数据库的增删查改动画）
│   ├── services/            # 业务逻辑、服务类（如发邮件、外部API交互）
│   ├── utils/               # 通用工具方法
│   ├── tests/               # 单元与集成测试
│   └── __init__.py
├── .env                     # 本地环境变量
├── .env.example             # 示范环境变量
├── README.md
├── .gitignore
└── LICENSE
```