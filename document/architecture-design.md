# 成绩数据可视化系统架构设计文档

## 1. 系统架构概述

### 1.1 整体架构
本系统采用现代化的前后端分离架构，基于微服务设计理念，确保系统的可扩展性、可维护性和高性能。

```mermaid
graph TB
    subgraph "客户端层"
        A[Web浏览器] --> B[Vue.js前端应用]
    end
    
    subgraph "网关层"
        B --> C[Nginx反向代理]
        C --> D[API网关]
    end
    
    subgraph "应用层"
        D --> E[用户服务]
        D --> F[文件服务]
        D --> G[数据处理服务]
        D --> H[图表服务]
    end
    
    subgraph "数据层"
        E --> I[PostgreSQL主库]
        F --> J[MinIO对象存储]
        G --> K[Redis缓存]
        H --> L[PostgreSQL从库]
    end
    
    subgraph "基础设施层"
        M[Docker容器]
        N[Kubernetes集群]
        O[监控告警]
        P[日志收集]
    end
```

### 1.2 技术选型对比

| 组件类型 | 当前技术 | 推荐技术 | 选择理由 |
|---------|---------|---------|---------|
| 前端框架 | Vue 3 | Vue 3 + TypeScript | 保持现有技术栈，增加类型安全 |
| 状态管理 | Vuex 4 | Pinia | 更好的TypeScript支持，更简洁的API |
| 后端框架 | Tornado | FastAPI | 更好的性能，自动API文档，类型提示 |
| 数据库 | 文件存储 | PostgreSQL | 关系型数据，ACID特性，高性能 |
| 缓存 | 无 | Redis | 提升性能，会话管理 |
| 文件存储 | 本地文件 | MinIO | 分布式存储，S3兼容 |
| 容器化 | 无 | Docker | 环境一致性，部署便利 |

## 2. 前端架构设计

### 2.1 目录结构
```
front/
├── src/
│   ├── components/          # 通用组件
│   │   ├── common/         # 基础组件
│   │   ├── charts/         # 图表组件
│   │   └── upload/         # 上传组件
│   ├── views/              # 页面组件
│   │   ├── dashboard/      # 仪表板
│   │   ├── data-manage/    # 数据管理
│   │   ├── charts/         # 图表页面
│   │   └── system/         # 系统管理
│   ├── store/              # 状态管理
│   │   ├── modules/        # 模块化store
│   │   └── index.ts
│   ├── api/                # API接口
│   │   ├── user.ts
│   │   ├── file.ts
│   │   └── chart.ts
│   ├── utils/              # 工具函数
│   │   ├── request.ts      # HTTP请求封装
│   │   ├── auth.ts         # 认证工具
│   │   └── validate.ts     # 验证工具
│   ├── types/              # TypeScript类型定义
│   └── assets/             # 静态资源
├── public/
├── tests/                  # 测试文件
└── package.json
```

### 2.2 组件设计原则
- **单一职责**: 每个组件只负责一个功能
- **可复用性**: 通用组件可在多处使用
- **可测试性**: 组件易于单元测试
- **类型安全**: 使用TypeScript确保类型安全

### 2.3 状态管理设计
```typescript
// store/modules/user.ts
export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    token: '',
    permissions: []
  }),
  actions: {
    async login(credentials) { /* ... */ },
    async logout() { /* ... */ },
    async getUserInfo() { /* ... */ }
  }
})

// store/modules/file.ts
export const useFileStore = defineStore('file', {
  state: () => ({
    fileList: [],
    uploadProgress: 0,
    currentFile: null
  }),
  actions: {
    async uploadFile(file) { /* ... */ },
    async getFileList() { /* ... */ },
    async deleteFile(id) { /* ... */ }
  }
})
```

## 3. 后端架构设计

### 3.1 目录结构
```
backend/
├── app/
│   ├── api/                # API路由
│   │   ├── v1/
│   │   │   ├── auth.py     # 认证相关
│   │   │   ├── files.py    # 文件管理
│   │   │   ├── data.py     # 数据处理
│   │   │   └── charts.py   # 图表生成
│   │   └── deps.py         # 依赖注入
│   ├── core/               # 核心配置
│   │   ├── config.py       # 配置管理
│   │   ├── security.py     # 安全相关
│   │   └── database.py     # 数据库连接
│   ├── models/             # 数据模型
│   │   ├── user.py
│   │   ├── file.py
│   │   └── task.py
│   ├── services/           # 业务逻辑
│   │   ├── auth_service.py
│   │   ├── file_service.py
│   │   ├── data_service.py
│   │   └── chart_service.py
│   ├── utils/              # 工具函数
│   │   ├── excel_parser.py
│   │   ├── chart_generator.py
│   │   └── data_processor.py
│   └── schemas/            # Pydantic模型
├── tests/                  # 测试文件
├── migrations/             # 数据库迁移
├── requirements.txt
└── main.py
```

### 3.2 分层架构设计

#### 3.2.1 控制器层 (API Layer)
```python
# api/v1/files.py
from fastapi import APIRouter, Depends, UploadFile
from services.file_service import FileService

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile,
    file_service: FileService = Depends()
):
    return await file_service.upload_file(file)

@router.get("/")
async def get_files(
    file_service: FileService = Depends()
):
    return await file_service.get_file_list()
```

#### 3.2.2 服务层 (Service Layer)
```python
# services/file_service.py
class FileService:
    def __init__(self, db: Session, storage: StorageService):
        self.db = db
        self.storage = storage
    
    async def upload_file(self, file: UploadFile):
        # 文件验证
        self._validate_file(file)
        
        # 保存到存储
        file_path = await self.storage.save_file(file)
        
        # 保存到数据库
        db_file = File(
            filename=file.filename,
            file_path=file_path,
            file_size=file.size
        )
        self.db.add(db_file)
        self.db.commit()
        
        return db_file
    
    def _validate_file(self, file: UploadFile):
        # 文件类型验证
        # 文件大小验证
        # 文件内容验证
        pass
```

#### 3.2.3 数据访问层 (Repository Layer)
```python
# repositories/file_repository.py
class FileRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, file_data: dict) -> File:
        db_file = File(**file_data)
        self.db.add(db_file)
        self.db.commit()
        return db_file
    
    def get_by_id(self, file_id: int) -> File:
        return self.db.query(File).filter(File.id == file_id).first()
    
    def get_list(self, skip: int = 0, limit: int = 100) -> List[File]:
        return self.db.query(File).offset(skip).limit(limit).all()
```

### 3.3 数据处理模块设计

#### 3.3.1 数据处理工厂模式
```python
# utils/data_processor.py
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

class WeightedCalculator(DataProcessor):
    def __init__(self, weights: dict):
        self.weights = weights
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        # 加权计算逻辑
        pass

class NormalizationProcessor(DataProcessor):
    def __init__(self, min_score: float, max_score: float):
        self.min_score = min_score
        self.max_score = max_score
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        # 归一化处理逻辑
        pass

class DataProcessorFactory:
    @staticmethod
    def create_processor(processor_type: str, **kwargs) -> DataProcessor:
        if processor_type == "weighted":
            return WeightedCalculator(kwargs.get("weights"))
        elif processor_type == "normalize":
            return NormalizationProcessor(
                kwargs.get("min_score"), 
                kwargs.get("max_score")
            )
        else:
            raise ValueError(f"Unknown processor type: {processor_type}")
```

#### 3.3.2 图表生成策略模式
```python
# utils/chart_generator.py
from abc import ABC, abstractmethod

class ChartGenerator(ABC):
    @abstractmethod
    def generate(self, data: pd.DataFrame, options: dict) -> str:
        pass

class LineChartGenerator(ChartGenerator):
    def generate(self, data: pd.DataFrame, options: dict) -> str:
        # 生成折线图
        pass

class BarChartGenerator(ChartGenerator):
    def generate(self, data: pd.DataFrame, options: dict) -> str:
        # 生成柱状图
        pass

class RadarChartGenerator(ChartGenerator):
    def generate(self, data: pd.DataFrame, options: dict) -> str:
        # 生成雷达图
        pass

class ChartGeneratorFactory:
    _generators = {
        "line": LineChartGenerator,
        "bar": BarChartGenerator,
        "radar": RadarChartGenerator,
    }
    
    @classmethod
    def create_generator(cls, chart_type: str) -> ChartGenerator:
        generator_class = cls._generators.get(chart_type)
        if not generator_class:
            raise ValueError(f"Unknown chart type: {chart_type}")
        return generator_class()
```

## 4. 数据库设计

### 4.1 数据库架构
```mermaid
erDiagram
    User ||--o{ File : uploads
    User ||--o{ Task : creates
    File ||--o{ Task : processes
    Task ||--o{ Chart : generates
    
    User {
        int id PK
        string username
        string email
        string password_hash
        string role
        datetime created_at
        datetime updated_at
    }
    
    File {
        int id PK
        string filename
        string original_name
        string file_path
        int file_size
        string file_type
        int upload_user_id FK
        datetime created_at
    }
    
    Task {
        int id PK
        string task_type
        string status
        json input_files
        json output_files
        json parameters
        int created_by FK
        datetime created_at
        datetime updated_at
    }
    
    Chart {
        int id PK
        string chart_type
        string title
        json chart_data
        json chart_options
        string file_path
        int task_id FK
        datetime created_at
    }
```

### 4.2 索引设计
```sql
-- 用户表索引
CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_user_email ON users(email);

-- 文件表索引
CREATE INDEX idx_file_user_id ON files(upload_user_id);
CREATE INDEX idx_file_created_at ON files(created_at);

-- 任务表索引
CREATE INDEX idx_task_user_id ON tasks(created_by);
CREATE INDEX idx_task_status ON tasks(status);
CREATE INDEX idx_task_created_at ON tasks(created_at);

-- 图表表索引
CREATE INDEX idx_chart_task_id ON charts(task_id);
CREATE INDEX idx_chart_type ON charts(chart_type);
```

## 5. 安全架构设计

### 5.1 认证和授权
```python
# core/security.py
from jose import JWTError, jwt
from passlib.context import CryptContext

class SecurityService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
```

### 5.2 文件安全
```python
# utils/file_validator.py
class FileValidator:
    ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    @classmethod
    def validate_file(cls, file: UploadFile) -> bool:
        # 检查文件扩展名
        if not cls._check_extension(file.filename):
            raise ValueError("不支持的文件类型")
        
        # 检查文件大小
        if not cls._check_size(file.size):
            raise ValueError("文件大小超过限制")
        
        # 检查文件内容
        if not cls._check_content(file):
            raise ValueError("文件内容不合法")
        
        return True
    
    @classmethod
    def _check_extension(cls, filename: str) -> bool:
        return Path(filename).suffix.lower() in cls.ALLOWED_EXTENSIONS
    
    @classmethod
    def _check_size(cls, size: int) -> bool:
        return size <= cls.MAX_FILE_SIZE
    
    @classmethod
    def _check_content(cls, file: UploadFile) -> bool:
        # 使用python-magic检查文件真实类型
        # 扫描恶意内容
        return True
```

## 6. 性能优化设计

### 6.1 缓存策略
```python
# services/cache_service.py
import redis
from typing import Optional, Any

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
    
    async def get(self, key: str) -> Optional[Any]:
        value = self.redis_client.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: Any, expire: int = 3600):
        self.redis_client.setex(key, expire, json.dumps(value))
    
    async def delete(self, key: str):
        self.redis_client.delete(key)
    
    def cache_key(self, prefix: str, *args) -> str:
        return f"{prefix}:{':'.join(map(str, args))}"
```

### 6.2 异步任务处理
```python
# services/task_service.py
from celery import Celery

celery_app = Celery("data_analysis")

@celery_app.task
def process_data_async(file_id: int, processor_type: str, options: dict):
    # 异步数据处理
    file_service = FileService()
    data_service = DataService()
    
    # 读取文件
    file_data = file_service.get_file_data(file_id)
    
    # 处理数据
    result = data_service.process_data(file_data, processor_type, options)
    
    # 保存结果
    data_service.save_result(result)
    
    return {"status": "completed", "result_id": result.id}
```

## 7. 监控和日志设计

### 7.1 应用监控
```python
# core/monitoring.py
from prometheus_client import Counter, Histogram, generate_latest

# 定义监控指标
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

class MonitoringMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # 处理请求
            await self.app(scope, receive, send)
            
            # 记录指标
            duration = time.time() - start_time
            REQUEST_COUNT.labels(
                method=scope["method"],
                endpoint=scope["path"]
            ).inc()
            REQUEST_DURATION.observe(duration)
```

### 7.2 日志设计
```python
# core/logging.py
import logging
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
```

## 8. 部署架构

### 8.1 Docker化部署
```dockerfile
# Dockerfile.frontend
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```dockerfile
# Dockerfile.backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 8.2 Docker Compose配置
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./front
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/dbname
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=data_analysis
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

## 9. 总结

本架构设计文档提供了一个完整的现代化前后端分离系统架构，主要特点包括：

1. **模块化设计**: 清晰的分层架构，便于维护和扩展
2. **技术现代化**: 采用最新的技术栈，提升开发效率
3. **安全可靠**: 完善的安全机制和错误处理
4. **高性能**: 缓存、异步处理等性能优化措施
5. **可观测性**: 完善的监控和日志系统
6. **容器化**: Docker化部署，环境一致性

通过这个架构设计，可以将现有的单体应用重构为一个标准化的、可扩展的、易维护的现代化系统。