# TbbID 后端

## 项目结构

本项目采用前后端分离架构，后端使用Django REST Framework提供API服务。

### 模块化设计

后端代码按功能模块进行组织，每个模块有独立的API和URL配置：

```
bidapp/
  ├── apis/                 # API视图函数按模块组织
  │    ├── project.py       # 项目相关API
  │    ├── bid.py           # 投标相关API
  │    ├── company.py       # 公司信息API
  │    ├── auth.py          # 用户认证API
  │    ├── list_simulator.py # 清单模拟器API
  │    ├── ...
  ├── urls/                 # URL路由配置按模块组织
  │    ├── project_urls.py
  │    ├── bid_urls.py
  │    ├── company_urls.py
  │    ├── ...
  ├── main_urls.py         # 主路由入口
  ├── utils.py             # 工具函数
  ├── models.py            # 数据模型
  ├── ...
```

### API模块说明

1. **项目模块** (`apis/project.py`):
   - 项目列表 - `GET /api/projects/`
   - 项目详情 - `GET /api/projects/<project_id>/`
   - 今日更新统计 - `GET /api/today_update_count/`

2. **投标模块** (`apis/bid.py`):
   - 标段列表 - `GET /api/bid_sections/`
   - 投标详情 - `GET /api/bids/<pk>/`
   - 投标结果 - `GET /api/bid_results/`
   - 投标结果详情 - `GET /api/bid_results/<pk>/`

3. **公司模块** (`apis/company.py`):
   - 公司搜索 - `GET /api/company-search/`
   - 公司投标记录 - `GET /api/company-bids/`

4. **用户认证模块** (`apis/auth.py`):
   - 发送验证码 - `POST /api/send_sms_code/`
   - 用户注册 - `POST /api/register/`
   - 用户登录 - `POST /api/login/`
   - 刷新令牌 - `POST /api/token/refresh/`
   - 用户信息 - `GET /api/user-info/`
   - 用户登出 - `POST /api/logout/`

5. **清单模拟器模块** (`apis/list_simulator.py`):
   - 清单模拟计算 - `POST /api/list-simulator/`

6. **Excel处理器模块** (`apis/excel_processor.py`):
   - Excel处理页面 - `GET /excel-processor/`
   - Excel处理提交 - `POST /excel-processor/`

7. **投标优化器模块** (`apis/bid_optimizer.py`):
   - 投标优化页面 - `GET /bid-optimizer/`
   - 投标优化计算 - `POST /bid-optimizer/`

## 运行项目

1. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

2. 运行开发服务器:
   ```
   python manage.py runserver
   ```

## 开发说明

- 添加新功能时，请遵循模块化结构，在相应的apis和urls目录下创建新文件
- 工具函数应放在utils.py中，便于复用
- 新增模块后，需在main_urls.py中引入对应的URL配置 