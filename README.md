# AiMall 电商后端

> 基于 FastAPI 的 B2C 电商后端（京东/淘宝单店形态），把「用户 → 商品 → 购物车 → 下单 → 支付 → 库存」这条交易主链路做扎实，并包含秒杀模块体现高并发处理能力。
> 纯后端 API + Swagger 文档，不做前端。

---

## 技术栈

| 分类 | 选型 | 用途 |
| --- | --- | --- |
| 语言 | Python 3.11 | |
| Web 框架 | FastAPI 0.141 + uvicorn | 路由、依赖注入、自动生成 Swagger |
| ORM | SQLAlchemy 2.0（async）+ aiomysql | 异步访问 MySQL |
| 数据库 | MySQL 8.0 | 业务数据 |
| 缓存 | Redis 8.1 | 短信验证码（后续用于限流与秒杀） |
| 校验/配置 | Pydantic v2 + pydantic-settings | 出入参模型、配置管理 |
| 认证 | PyJWT（HS256）+ bcrypt | JWT 签发与校验、密码哈希 |
| 日志 | loguru | |
| 测试 | pytest | |

---

## 快速开始

### 1. 环境准备
- Python 3.11（本项目使用 conda 环境 `aimall`）
- MySQL 8.0 已启动，数据库 `ai_mall`，字符集必须为 **utf8mb4**
- Redis 已启动（默认 127.0.0.1:6379）

### 2. 安装依赖
```bash
conda activate aimall
pip install -r requirements.txt
```

### 3. 配置环境变量
在项目根目录创建 `.env`（已被 `.gitignore` 忽略，不会提交）：

```ini
DATABASE_URL=mysql+aiomysql://用户名:密码@127.0.0.1:3306/ai_mall?charset=utf8mb4
REDIS_URL=redis://127.0.0.1:6379/0?protocol=2
APP_ENV=dev
LOG_LEVEL=DEBUG
JWT_SECRET=至少32字节的随机字符串
JWT_EXPIRE_MINUTES=30
```

### 4. 建表
```bash
python -m app.scripts.init_db
```
> 开发期用 SQLAlchemy 的 `create_all` 建表；正式的表结构迁移计划接入 Alembic。

### 5. 启动服务
```bash
uvicorn app.main:app --reload
```
（也可以直接在 PyCharm 里运行 `app/main.py`，等价。）

### 6. 打开接口文档
http://127.0.0.1:8000/docs

---

## 项目结构

```
AiMall/
├── app/
│   ├── api/v1/          # 接口层（路由）：收参数、调 service、包响应
│   ├── services/        # 业务层：业务规则 + 所有数据库读写（事务在这里）
│   ├── models/          # ORM 模型：数据库表结构
│   ├── schemas/         # Pydantic 出入参模型（接口契约）
│   ├── core/            # 配置、异常、全局异常处理器、统一响应、安全（JWT/密码）
│   ├── db/              # engine / session / base / redis 连接
│   ├── scripts/         # 开发自检脚本（check_*）与建表脚本
│   ├── static/          # 静态页面
│   └── main.py          # 应用入口：创建 app、挂路由、注册异常处理器
├── docs/                # 设计决策记录
├── requirements.txt
└── .env                 # 本地配置（不提交）
```

---

## 分层与请求流转

```
HTTP 请求
  → api/v1/*.py     路由函数：校验入参、依赖注入、调用 service
  → services/*.py   业务逻辑：业务规则判断 + 数据库读写（事务在这里）
  → models/*.py     ORM 模型：映射到 MySQL 表
  ← services 抛 BizError 表示业务失败（由全局处理器翻译成统一响应）
  ← 路由把 ORM 对象转成 schemas 里的出参模型，包成 {code, message, data}
```

依赖方向是单向的：`api → services → models`。**services 不允许 import api**（那叫分层倒挂）。

---

## 已完成的模块

- [x] **M1 地基**：分层架构、数据库连接、统一响应与全局异常处理、日志
- [x] **M2 用户域**：短信验证码（Redis）、注册、登录、JWT 签发与解析、鉴权依赖、获取/修改个人资料
- [x] **M3.1 分类域**：分类创建与列表、`parent_id` 自关联树
- [ ] **M3.2 商品域**：SPU / SKU（进行中）
- [ ] M4 购物车
- [ ] M5 订单域：下单事务、库存预占/扣减/释放、状态机、超时关闭、幂等
- [ ] M6 支付域：回调验签、幂等
- [ ] M7 秒杀：Redis + Lua 原子扣减、MQ 削峰、限流
- [ ] M8 打磨：缓存、索引、压测 QPS、Docker + Nginx 部署

---

## 接口清单

### 用户域

| 方法 | 路径 | 说明 | 需要登录 |
| --- | --- | --- | --- |
| POST | `/api/v1/users/sms/code` | 发送短信验证码（开发期为假短信，打印到日志） | 否 |
| POST | `/api/v1/users/register` | 注册（需带 `sms_code`） | 否 |
| POST | `/api/v1/users/login` | 登录，返回 JWT | 否 |
| GET | `/api/v1/users/me` | 获取当前登录用户 | 是 |
| PATCH | `/api/v1/users/me` | 修改个人资料（昵称） | 是 |

### 商品域

| 方法 | 路径 | 说明 | 需要登录 |
| --- | --- | --- | --- |
| POST | `/api/v1/categories` | 创建分类 | 是 |
| GET | `/api/v1/categories` | 分类列表（按 sort、id 升序） | 否 |

> 需要登录的接口在请求头带 `Authorization: Bearer <token>`。
> 在 Swagger 里点右上角 🔒 Authorize，把登录返回的 `token` 原文粘进去即可。

---

## 统一响应与错误码

所有接口一律返回 HTTP 200，用响应体里的 `code` 表达业务结果：

```json
{ "code": 0, "message": "success", "data": {} }
```

- `code = 0`：成功
- `code != 0`：业务失败，`message` 是给用户看的原因
- HTTP 状态码只表示「请求有没有被正常处理完」；**业务成没成看 code**

错误码按业务域分段：

| 段 | 归属 | 已用 |
| --- | --- | --- |
| `0` | 成功 | — |
| `1xxx` | 通用 | `1`（默认业务错误） |
| `2xxx` | 用户域 | `2002` token 错误；`2003` 未登录；`2004` token 无效；`2005` 用户不存在 |
| `3xxx` | 商品域 | `3001` 同级已存在同名分类；`3002` 父分类不存在；`3003` 分类不存在；`3004` 商品创建失败 |
| `4xxx` | 订单域 | 规划中 |

---

## 设计要点

- **业务错误返回 HTTP 200**，用 `code` 表达业务结果，避免业务失败污染 500 告警
- **金额用 `Decimal` / `NUMERIC(10,2)`**，不用 float（二进制浮点存不准小数）
- **价格与库存只存 SKU，SPU 不带价格**；列表页起售价用 `min(sku.price)` 聚合，不落库
- **分类用 `parent_id` 自关联存一棵树**，一级分类的 `parent_id` 为 NULL
- **查重 + `IntegrityError` 兜底是两道闸门**：前者给准确提示，后者防并发
- **资源归属从凭证推导，不由客户端指定**：改资料用 `PATCH /me`，路径里不出现 user_id

详细的设计取舍、踩坑记录与面试问答见 [docs/design-decisions.md](docs/design-decisions.md)。

---

## 开发约定

- **提交信息**用 Conventional Commits：`feat:` / `fix:` / `docs:` / `chore:` / `test:` / `refactor:`
- **分支**：单人开发，直接在 `master` 上提交，不引入开发分支；改用 **tag 标记里程碑**，
  保留可随时回退的节点（多人协作时才需要 `feat/xxx` 分支 + PR）
- **不提交 `.env`**（已由 `.gitignore` 忽略）
- **文档维护**：每完成一个里程碑或新增一批接口，同步更新本文件 ——
  ①「已完成的模块」打勾；②「接口清单」补新接口；③「设计要点」补新的取舍。
  详细设计记录追加到 `docs/design-decisions.md`
