# REST API 分页功能实现文档

## 概述

本文档描述了如何在后端API中实现分页功能，以支持前端组件的"查看更多"功能和分页展示。

## 分页实现

### 分页类

在 `pagination.py` 中，我们定义了一个标准的分页器 `StandardResultsSetPagination`，它支持以下功能：

- 默认每页显示10条记录
- 通过 `page_size` 参数自定义每页记录数量（最大100）
- 通过 `page` 参数指定页码
- 返回分页后的数据，包括：
  - 总记录数 (`count`)
  - 总页数 (`total_pages`)
  - 当前页码 (`current`)
  - 下一页链接 (`next`)
  - 上一页链接 (`previous`)
  - 当前页的数据 (`results`)

### API端点

以下API端点已经实现了分页功能：

1. `/api/projects/` - 项目列表
2. `/api/bid_sections/` - 标段列表
3. `/api/bid_results/` - 中标结果列表

### 请求参数

支持的URL参数：

- `page`: 页码，默认为1
- `page_size`: 每页条数，默认为10，最大100
- `search`: 搜索关键词（根据不同的API有不同的搜索字段）

### 响应格式

```json
{
  "count": 100,               // 总记录数
  "total_pages": 10,          // 总页数
  "current": 1,               // 当前页码
  "next": "http://example.com/api/items/?page=2",  // 下一页链接
  "previous": null,           // 上一页链接
  "results": [                // 当前页的数据
    {
      "id": 1,
      "name": "Item 1"
      // ...
    },
    {
      "id": 2,
      "name": "Item 2"
      // ...
    }
    // ...
  ]
}
```

## 搜索功能

每个API端点都支持搜索功能，以下是搜索字段：

1. 项目列表 (`/api/projects/`)
   - 项目名称 (`title`)
   - 项目区域 (`district_show`)

2. 标段列表 (`/api/bid_sections/`)
   - 标段名称 (`section_name`)

3. 中标结果列表 (`/api/bid_results/`)
   - 标段名称 (`section_name`)
   - 中标单位 (`bidder_name`)

## 错误处理

分页器实现了错误处理机制，当发生以下情况时会优雅地处理：

- 无效的页码参数
- 无效的每页条数参数
- 分页过程中发生的其他错误

在出现错误时，API会尝试返回未分页的数据（默认10条记录）。

## 测试

在 `tests/test_pagination.py` 中包含了完整的测试用例，用于验证分页功能、搜索功能和错误处理机制的正确性。

## 前端集成

前端可以通过以下方式与分页API交互：

```javascript
// 示例：获取项目列表的第2页，每页5条记录
axios.get('/api/projects/?page=2&page_size=5')
  .then(res => {
    // 处理分页数据
    const { count, total_pages, current, results } = res.data;
    // 更新UI
  });

// 示例：搜索项目
axios.get('/api/projects/?search=关键词&page=1&page_size=10')
  .then(res => {
    // 处理搜索结果
  });
``` 