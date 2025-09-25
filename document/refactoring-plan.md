# 成绩数据可视化系统重构计划

## 1. 重构概述

### 1.1 重构目标
将现有的单体应用重构为标准化的前后端分离系统，提升代码质量、系统性能和可维护性。

### 1.2 重构原则
- **渐进式重构**: 分阶段进行，确保系统稳定运行
- **向后兼容**: 保持现有功能不变，确保用户体验
- **测试驱动**: 每个重构步骤都有对应的测试
- **文档同步**: 及时更新文档，保持一致性

### 1.3 重构范围
- 前端架构现代化
- 后端架构重构
- 数据库设计优化
- API接口标准化
- 部署流程自动化

## 2. 重构阶段规划

### 2.1 第一阶段：基础设施搭建（2周）

#### 2.1.1 项目结构重组
**目标**: 建立标准化的项目目录结构

**任务清单**:
- [ ] 创建新的项目目录结构
- [ ] 设置前端TypeScript环境
- [ ] 配置后端FastAPI项目
- [ ] 设置数据库连接
- [ ] 配置开发环境

**具体步骤**:
```bash
# 1. 创建新的项目结构
mkdir -p data-analysis-system/{frontend,backend,docs,deploy}

# 2. 前端项目初始化
cd frontend
npm create vue@latest . --typescript --router --pinia --eslint --prettier

# 3. 后端项目初始化
cd ../backend
pip install fastapi uvicorn sqlalchemy alembic redis celery
```

**验收标准**:
- 项目结构清晰，符合最佳实践
- 开发环境可以正常启动
- 基础配置文件完整

#### 2.1.2 数据库设计和迁移
**目标**: 设计新的数据库结构，迁移现有数据

**任务清单**:
- [ ] 设计数据库表结构
- [ ] 创建数据库迁移脚本
- [ ] 编写数据迁移工具
- [ ] 测试数据迁移

**数据库表设计**:
```sql
-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 文件表
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 任务表
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    input_files JSONB,
    output_files JSONB,
    parameters JSONB,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 图表表
CREATE TABLE charts (
    id SERIAL PRIMARY KEY,
    chart_type VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    chart_data JSONB,
    chart_options JSONB,
    file_path VARCHAR(500),
    task_id INTEGER REFERENCES tasks(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**验收标准**:
- 数据库表创建成功
- 现有数据成功迁移
- 数据完整性验证通过

#### 2.1.3 基础API框架搭建
**目标**: 建立标准化的API框架

**任务清单**:
- [ ] 设置FastAPI项目结构
- [ ] 配置数据库连接
- [ ] 实现基础中间件
- [ ] 设置API文档

**代码示例**:
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import auth, files, data, charts

app = FastAPI(
    title="数据分析系统API",
    description="成绩数据可视化系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(files.router, prefix="/api/v1/files", tags=["文件管理"])
app.include_router(data.router, prefix="/api/v1/data", tags=["数据处理"])
app.include_router(charts.router, prefix="/api/v1/charts", tags=["图表生成"])
```

**验收标准**:
- API服务正常启动
- Swagger文档可访问
- 基础路由响应正常

### 2.2 第二阶段：核心功能迁移（4周）

#### 2.2.1 用户认证系统（1周）
**目标**: 实现完整的用户认证和授权系统

**任务清单**:
- [ ] 用户注册和登录API
- [ ] JWT token生成和验证
- [ ] 权限控制中间件
- [ ] 前端登录页面重构

**后端实现**:
```python
# api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from services.auth_service import AuthService
from schemas.user import UserCreate, UserLogin, Token

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, auth_service: AuthService = Depends()):
    return await auth_service.register(user_data)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, auth_service: AuthService = Depends()):
    return await auth_service.login(credentials)

@router.get("/me")
async def get_current_user(token: str = Depends(security)):
    return await auth_service.get_current_user(token)
```

**前端实现**:
```typescript
// stores/auth.ts
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem('token') || '',
    isAuthenticated: false
  }),

  actions: {
    async login(credentials: LoginForm) {
      try {
        const response = await authApi.login(credentials)
        this.token = response.access_token
        this.user = response.user
        this.isAuthenticated = true
        localStorage.setItem('token', this.token)
        return response
      } catch (error) {
        throw error
      }
    },

    async logout() {
      this.user = null
      this.token = ''
      this.isAuthenticated = false
      localStorage.removeItem('token')
    }
  }
})
```

**验收标准**:
- 用户可以正常注册和登录
- JWT token正确生成和验证
- 权限控制正常工作
- 前端状态管理正确

#### 2.2.2 文件管理系统（1周）
**目标**: 重构文件上传和管理功能

**任务清单**:
- [ ] 文件上传API重构
- [ ] 文件列表和详情API
- [ ] 文件删除和重命名功能
- [ ] 前端文件管理界面

**后端实现**:
```python
# api/v1/files.py
from fastapi import APIRouter, Depends, UploadFile, File
from services.file_service import FileService
from schemas.file import FileResponse, FileList

router = APIRouter()

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    file_service: FileService = Depends()
):
    return await file_service.upload_file(file)

@router.get("/", response_model=FileList)
async def get_files(
    skip: int = 0,
    limit: int = 100,
    file_service: FileService = Depends()
):
    return await file_service.get_file_list(skip, limit)

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    file_service: FileService = Depends()
):
    return await file_service.delete_file(file_id)
```

**前端实现**:
```vue
<!-- components/FileUpload.vue -->
<template>
  <div class="file-upload">
    <el-upload
      class="upload-demo"
      drag
      :action="uploadUrl"
      :headers="uploadHeaders"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击上传</em>
      </div>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const uploadUrl = ref('/api/v1/files/upload')
const uploadHeaders = ref({
  Authorization: `Bearer ${authStore.token}`
})

const beforeUpload = (file: File) => {
  const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  const isLt50M = file.size / 1024 / 1024 < 50

  if (!isExcel) {
    ElMessage.error('只能上传Excel文件!')
    return false
  }
  if (!isLt50M) {
    ElMessage.error('文件大小不能超过50MB!')
    return false
  }
  return true
}

const handleSuccess = (response: any) => {
  ElMessage.success('文件上传成功!')
  // 刷新文件列表
}

const handleError = (error: any) => {
  ElMessage.error('文件上传失败!')
}
</script>
```

**验收标准**:
- 文件上传功能正常
- 文件列表显示正确
- 文件操作功能完整
- 错误处理完善

#### 2.2.3 数据处理功能迁移（2周）
**目标**: 将现有的13个数据处理功能迁移到新架构

**任务清单**:
- [ ] 重构加权计算功能
- [ ] 重构归一化处理功能
- [ ] 重构数据合并功能
- [ ] 重构图表生成功能
- [ ] 实现异步任务处理

**数据处理服务重构**:
```python
# services/data_service.py
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class DataProcessor(ABC):
    @abstractmethod
    async def process(self, data: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
        pass

class WeightedCalculator(DataProcessor):
    async def process(self, data: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
        weights = options.get('weights', {})
        result_data = data.copy()
        
        # 加权计算逻辑
        weighted_sum = 0
        total_weight = 0
        
        for column, weight in weights.items():
            if column in data.columns:
                weighted_sum += data[column] * weight
                total_weight += weight
        
        if total_weight > 0:
            result_data['加权成绩'] = weighted_sum / total_weight
        
        return result_data

class NormalizationProcessor(DataProcessor):
    async def process(self, data: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
        min_score = options.get('min_score', 60)
        max_score = options.get('max_score', 100)
        columns = options.get('columns', [])
        
        result_data = data.copy()
        
        for column in columns:
            if column in data.columns:
                col_min = data[column].min()
                col_max = data[column].max()
                
                if col_max > col_min:
                    normalized = (data[column] - col_min) / (col_max - col_min)
                    result_data[f'归一化_{column}'] = normalized * (max_score - min_score) + min_score
        
        return result_data

class DataProcessorFactory:
    _processors = {
        'weighted': WeightedCalculator,
        'normalize': NormalizationProcessor,
    }
    
    @classmethod
    def create_processor(cls, processor_type: str) -> DataProcessor:
        processor_class = cls._processors.get(processor_type)
        if not processor_class:
            raise ValueError(f"Unknown processor type: {processor_type}")
        return processor_class()
```

**异步任务处理**:
```python
# tasks/data_tasks.py
from celery import Celery
from services.data_service import DataService
from services.file_service import FileService

celery_app = Celery('data_analysis')

@celery_app.task
def process_data_task(file_id: int, processor_type: str, options: dict):
    try:
        # 获取文件数据
        file_service = FileService()
        data = file_service.get_file_data(file_id)
        
        # 处理数据
        data_service = DataService()
        result = data_service.process_data(data, processor_type, options)
        
        # 保存结果
        result_file = data_service.save_result(result)
        
        return {
            'status': 'success',
            'result_file_id': result_file.id
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
```

**验收标准**:
- 所有数据处理功能正常工作
- 异步任务处理稳定
- 处理结果准确
- 错误处理完善

### 2.3 第三阶段：图表功能重构（3周）

#### 2.3.1 图表生成引擎重构（2周）
**目标**: 重构图表生成功能，提升性能和可扩展性

**任务清单**:
- [ ] 重构图表生成器
- [ ] 实现图表模板系统
- [ ] 优化图表渲染性能
- [ ] 添加图表交互功能

**图表生成器重构**:
```python
# services/chart_service.py
from abc import ABC, abstractmethod
from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Pie, Radar, Scatter
import json

class ChartGenerator(ABC):
    @abstractmethod
    def generate(self, data: pd.DataFrame, options: dict) -> dict:
        pass

class LineChartGenerator(ChartGenerator):
    def generate(self, data: pd.DataFrame, options: dict) -> dict:
        chart = Line(init_opts=opts.InitOpts(
            width=options.get('width', '800px'),
            height=options.get('height', '600px'),
            theme=options.get('theme', 'white')
        ))
        
        x_axis = data[options['x_column']].tolist()
        chart.add_xaxis(x_axis)
        
        for y_column in options['y_columns']:
            y_data = data[y_column].tolist()
            chart.add_yaxis(
                series_name=y_column,
                y_axis=y_data,
                is_smooth=options.get('smooth', True)
            )
        
        chart.set_global_opts(
            title_opts=opts.TitleOpts(title=options.get('title', '折线图')),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(orient="horizontal", pos_top="5%"),
        )
        
        return {
            'chart_html': chart.render_embed(),
            'chart_options': chart.options
        }

class BarChartGenerator(ChartGenerator):
    def generate(self, data: pd.DataFrame, options: dict) -> dict:
        chart = Bar(init_opts=opts.InitOpts(
            width=options.get('width', '800px'),
            height=options.get('height', '600px'),
            theme=options.get('theme', 'white')
        ))
        
        x_axis = data[options['x_column']].tolist()
        chart.add_xaxis(x_axis)
        
        for y_column in options['y_columns']:
            y_data = data[y_column].tolist()
            chart.add_yaxis(
                series_name=y_column,
                y_axis=y_data
            )
        
        chart.set_global_opts(
            title_opts=opts.TitleOpts(title=options.get('title', '柱状图')),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(orient="horizontal", pos_top="5%"),
        )
        
        return {
            'chart_html': chart.render_embed(),
            'chart_options': chart.options
        }

class ChartGeneratorFactory:
    _generators = {
        'line': LineChartGenerator,
        'bar': BarChartGenerator,
        'pie': PieChartGenerator,
        'radar': RadarChartGenerator,
        'scatter': ScatterChartGenerator,
    }
    
    @classmethod
    def create_generator(cls, chart_type: str) -> ChartGenerator:
        generator_class = cls._generators.get(chart_type)
        if not generator_class:
            raise ValueError(f"Unknown chart type: {chart_type}")
        return generator_class()
```

**前端图表组件**:
```vue
<!-- components/ChartRenderer.vue -->
<template>
  <div class="chart-container">
    <div class="chart-toolbar">
      <el-button-group>
        <el-button @click="exportChart('png')">导出PNG</el-button>
        <el-button @click="exportChart('pdf')">导出PDF</el-button>
        <el-button @click="fullscreen">全屏</el-button>
      </el-button-group>
    </div>
    <div ref="chartRef" class="chart-content"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

interface Props {
  chartData: any
  chartOptions: any
  chartType: string
}

const props = defineProps<Props>()
const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

onMounted(() => {
  initChart()
})

watch(() => props.chartData, () => {
  updateChart()
}, { deep: true })

const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
    updateChart()
  }
}

const updateChart = () => {
  if (chartInstance && props.chartOptions) {
    chartInstance.setOption(props.chartOptions)
  }
}

const exportChart = (format: string) => {
  if (chartInstance) {
    const url = chartInstance.getDataURL({
      type: format,
      pixelRatio: 2,
      backgroundColor: '#fff'
    })
    
    const link = document.createElement('a')
    link.download = `chart.${format}`
    link.href = url
    link.click()
  }
}

const fullscreen = () => {
  if (chartRef.value) {
    chartRef.value.requestFullscreen()
  }
}
</script>
```

**验收标准**:
- 所有图表类型正常生成
- 图表交互功能完整
- 导出功能正常工作
- 性能满足要求

#### 3.3.2 前端图表页面重构（1周）
**目标**: 重构前端图表展示页面

**任务清单**:
- [ ] 重构图表配置界面
- [ ] 实现图表预览功能
- [ ] 添加图表模板选择
- [ ] 优化用户体验

**验收标准**:
- 图表配置界面友好
- 预览功能实时更新
- 模板选择丰富
- 操作流程顺畅

### 2.4 第四阶段：系统优化和部署（2周）

#### 2.4.1 性能优化（1周）
**目标**: 优化系统性能，提升用户体验

**任务清单**:
- [ ] 实现Redis缓存
- [ ] 优化数据库查询
- [ ] 前端性能优化
- [ ] 添加CDN支持

**缓存实现**:
```python
# services/cache_service.py
import redis
import json
from typing import Optional, Any
from functools import wraps

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        value = self.redis_client.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, expire: int = 3600):
        self.redis_client.setex(key, expire, json.dumps(value, default=str))
    
    def delete(self, key: str):
        self.redis_client.delete(key)
    
    def cache_key(self, prefix: str, *args) -> str:
        return f"{prefix}:{':'.join(map(str, args))}"

def cache_result(prefix: str, expire: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_service = CacheService()
            cache_key = cache_service.cache_key(prefix, *args, **kwargs)
            
            # 尝试从缓存获取
            cached_result = cache_service.get(cache_key)
            if cached_result:
                return cached_result
            
            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            cache_service.set(cache_key, result, expire)
            return result
        return wrapper
    return decorator
```

**验收标准**:
- 页面加载时间 < 3秒
- API响应时间 < 1秒
- 缓存命中率 > 80%
- 内存使用合理

#### 2.4.2 部署自动化（1周）
**目标**: 实现自动化部署流程

**任务清单**:
- [ ] 编写Docker配置
- [ ] 设置CI/CD流程
- [ ] 配置监控告警
- [ ] 编写部署文档

**Docker配置**:
```dockerfile
# frontend/Dockerfile
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
# backend/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**CI/CD配置**:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          # 运行测试
          
  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker images
        run: |
          # 构建和推送镜像
      - name: Deploy to server
        run: |
          # 部署到服务器
```

**验收标准**:
- Docker镜像构建成功
- 自动化部署流程正常
- 监控告警配置完成
- 部署文档完整

## 3. 风险控制

### 3.1 技术风险
**风险**: 新技术栈学习成本高
**应对**: 提供技术培训，逐步迁移

**风险**: 数据迁移可能丢失
**应对**: 多次备份，分步验证

**风险**: 性能可能下降
**应对**: 性能测试，优化瓶颈

### 3.2 业务风险
**风险**: 功能回归问题
**应对**: 完整的测试覆盖

**风险**: 用户体验变差
**应对**: 用户反馈收集，快速迭代

### 3.3 项目风险
**风险**: 进度延期
**应对**: 合理排期，风险缓冲

**风险**: 人员变动
**应对**: 知识文档化，代码规范化

## 4. 质量保证

### 4.1 测试策略
- **单元测试**: 覆盖率 > 80%
- **集成测试**: 关键API接口
- **端到端测试**: 核心业务流程
- **性能测试**: 并发和大数据量

### 4.2 代码质量
- **代码规范**: ESLint + Prettier (前端), Black + isort (后端)
- **代码审查**: 所有代码必须经过审查
- **静态分析**: SonarQube代码质量检查
- **安全扫描**: 依赖漏洞扫描

### 4.3 文档要求
- **API文档**: Swagger自动生成
- **用户文档**: 操作手册和FAQ
- **开发文档**: 架构设计和开发指南
- **运维文档**: 部署和维护手册

## 5. 成功标准

### 5.1 技术指标
- [ ] 代码质量评分 > 8.0
- [ ] 测试覆盖率 > 80%
- [ ] API响应时间 < 1秒
- [ ] 页面加载时间 < 3秒
- [ ] 系统可用性 > 99.5%

### 5.2 功能指标
- [ ] 所有现有功能正常工作
- [ ] 新增功能按需求实现
- [ ] 用户体验显著提升
- [ ] 系统稳定性提高

### 5.3 维护指标
- [ ] 代码可读性提升
- [ ] 新功能开发效率提高
- [ ] 系统扩展性增强
- [ ] 运维成本降低

## 6. 总结

本重构计划提供了一个完整的系统现代化路径，通过分阶段实施，可以将现有系统升级为一个标准化的、高性能的、易维护的现代化应用。重构过程中需要严格按照计划执行，确保质量和进度的平衡。