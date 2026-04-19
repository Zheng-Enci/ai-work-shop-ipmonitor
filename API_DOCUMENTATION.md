# AiWorkShop IP 监控系统 API 接口文档

**版本**: v1.0.0  
**最后更新**: 2026-04-19  
**协议**: HTTP/HTTPS  
**编码**: UTF-8  
**内容类型**: application/json

---

## 目录

1. [文档说明](#文档说明)
2. [基础信息](#基础信息)
3. [通用规范](#通用规范)
4. [接口列表](#接口列表)
5. [错误码说明](#错误码说明)
6. [附录](#附录)

---

## 文档说明

### 适用范围

本文档适用于 AiWorkShop IP 监控系统的 RESTful API 接口，提供 IP 扫描数据统计、IP 范围查询等功能。

### 阅读对象

- 前端开发人员
- 后端开发人员
- 测试工程师
- 运维工程师

### 版本历史

| 版本号 | 更新日期 | 更新内容 | 作者 |
|--------|----------|----------|------|
| v1.0.0 | 2026-04-19 | 初始版本，包含基础接口 | 郑恩赐 |

---

## 基础信息

### 服务地址

| 环境 | 协议 | 地址 | 端口 |
|------|------|------|------|
| 本地开发 | HTTP | 127.0.0.1 | 5000 |
| 局域网 | HTTP | 10.0.48.241 | 5000 |

### 请求基础信息

| 项目 | 说明 |
|------|------|
| 协议 | HTTP/1.1 或 HTTPS |
| 请求方式 | GET、POST、OPTIONS |
| 字符编码 | UTF-8 |
| 请求格式 | application/json |
| 响应格式 | application/json |

### 公共请求头

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| Content-Type | String | 是 | 内容类型 | application/json |
| Accept | String | 是 | 接受类型 | application/json |
| Origin | String | 否 | 来源域名 | http://localhost:3000 |

---

## 通用规范

### 接口路径规范

- **路径格式**: `/api/{资源名}`
- **命名规范**: 小写字母，短横线分隔（kebab-case）
- **版本控制**: 路径中包含版本号，如 `/api/v1/resource`

### HTTP 方法规范

| 方法 | 用途 | 幂等性 |
|------|------|--------|
| GET | 获取资源 | 是 |
| POST | 创建资源 | 否 |
| PUT | 全量更新 | 是 |
| PATCH | 局部更新 | 否 |
| DELETE | 删除资源 | 是 |

### 通用响应结构

所有接口返回统一格式的 JSON 数据：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {}
}
```

**字段说明**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | Integer | 是 | 业务状态码，200 表示成功，非 200 表示失败 |
| message | String | 是 | 操作结果描述，可直接展示给用户 |
| data | Object/Array/Null | 是 | 响应数据，根据接口不同返回不同类型 |

### 时间戳格式

- **格式**: Unix 时间戳（秒）
- **类型**: Float
- **示例**: `1776589846.8984776`
- **说明**: 表示从 1970-01-01 00:00:00 UTC 到当前时间的秒数，包含小数部分

---

## 接口列表

### 1. 获取 IP 出现次数统计

#### 基本信息

| 项目 | 内容 |
|------|------|
| 接口名称 | get-ip-counts |
| 请求路径 | /api/ip-counts |
| 请求方法 | GET |
| 接口描述 | 获取指定时间范围内每个 IP 出现的次数统计 |

#### 请求参数

**Query 参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| start_time | Float | 是 | 开始时间戳（Unix 时间戳，秒） | 0 |
| end_time | Float | 是 | 结束时间戳（Unix 时间戳，秒） | 9999999999 |

#### 请求示例

```http
GET /api/ip-counts?start_time=0&end_time=9999999999 HTTP/1.1
Host: 10.0.48.241:5000
Content-Type: application/json
Accept: application/json
```

#### 响应参数

**成功响应 (HTTP 200)**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer | 业务状态码，固定为 200 |
| message | String | 操作结果描述 |
| data | Object | 响应数据对象 |
| data.total_scans | Integer | 该时间范围内的扫描次数 |
| data.ip_counts | Object | IP 出现次数统计，键为 IP 地址，值为出现次数 |

**响应示例**:

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "total_scans": 15,
        "ip_counts": {
            "10.0.48.241": 15,
            "10.0.48.153": 12,
            "10.0.48.154": 10,
            "10.0.48.155": 8,
            "10.0.48.156": 8
        }
    }
}
```

#### 错误响应

**参数缺失 (HTTP 400)**:

```json
{
    "code": 400,
    "message": "缺少必要参数：start_time 和 end_time",
    "data": null
}
```

**参数格式错误 (HTTP 400)**:

```json
{
    "code": 400,
    "message": "时间戳格式错误，必须是数字",
    "data": null
}
```

---

### 2. 获取扫描次数

#### 基本信息

| 项目 | 内容 |
|------|------|
| 接口名称 | get-scan-count |
| 请求路径 | /api/scan-count |
| 请求方法 | GET |
| 接口描述 | 获取指定时间范围内的扫描次数 |

#### 请求参数

**Query 参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| start_time | Float | 是 | 开始时间戳（Unix 时间戳，秒） | 0 |
| end_time | Float | 是 | 结束时间戳（Unix 时间戳，秒） | 9999999999 |

#### 请求示例

```http
GET /api/scan-count?start_time=0&end_time=9999999999 HTTP/1.1
Host: 10.0.48.241:5000
Content-Type: application/json
Accept: application/json
```

#### 响应参数

**成功响应 (HTTP 200)**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer | 业务状态码，固定为 200 |
| message | String | 操作结果描述 |
| data | Object | 响应数据对象 |
| data.scan_count | Integer | 该时间范围内的扫描次数 |

**响应示例**:

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "scan_count": 15
    }
}
```

#### 错误响应

**参数缺失 (HTTP 400)**:

```json
{
    "code": 400,
    "message": "缺少必要参数：start_time 和 end_time",
    "data": null
}
```

**参数格式错误 (HTTP 400)**:

```json
{
    "code": 400,
    "message": "时间戳格式错误，必须是数字",
    "data": null
}
```

---

### 3. 获取坊内 IP 列表

#### 基本信息

| 项目 | 内容 |
|------|------|
| 接口名称 | get-fang-ips |
| 请求路径 | /api/fang-ips |
| 请求方法 | GET |
| 接口描述 | 获取配置中定义的坊内 IP 地址列表 |

#### 请求参数

无

#### 请求示例

```http
GET /api/fang-ips HTTP/1.1
Host: 10.0.48.241:5000
Content-Type: application/json
Accept: application/json
```

#### 响应参数

**成功响应 (HTTP 200)**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer | 业务状态码，固定为 200 |
| message | String | 操作结果描述 |
| data | Object | 响应数据对象 |
| data.fang_ips | Array[String] | 坊内 IP 地址列表 |
| data.count | Integer | 坊内 IP 数量 |

**响应示例**:

```json
{
    "code": 200,
    "message": "获取坊内 IP 列表成功",
    "data": {
        "fang_ips": [
            "10.0.48.153",
            "10.0.48.154",
            "10.0.48.155",
            "10.0.48.156",
            "10.0.48.157"
        ],
        "count": 47
    }
}
```

---

### 4. 获取 IP 范围

#### 基本信息

| 项目 | 内容 |
|------|------|
| 接口名称 | get-ip-range |
| 请求路径 | /api/ip-range |
| 请求方法 | GET |
| 接口描述 | 获取配置中定义的扫描 IP 范围 |

#### 请求参数

无

#### 请求示例

```http
GET /api/ip-range HTTP/1.1
Host: 10.0.48.241:5000
Content-Type: application/json
Accept: application/json
```

#### 响应参数

**成功响应 (HTTP 200)**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer | 业务状态码，固定为 200 |
| message | String | 操作结果描述 |
| data | Object | 响应数据对象 |
| data.ip_range | Array[String] | IP 地址范围列表 |
| data.count | Integer | IP 地址总数 |
| data.start_ip | String | 起始 IP 地址 |
| data.end_ip | String | 结束 IP 地址 |

**响应示例**:

```json
{
    "code": 200,
    "message": "获取 IP 范围成功",
    "data": {
        "ip_range": [
            "10.0.48.151",
            "10.0.48.152",
            "10.0.48.153"
        ],
        "count": 100,
        "start_ip": "10.0.48.151",
        "end_ip": "10.0.48.250"
    }
}
```

---

## 错误码说明

### 业务错误码

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 操作成功 | 正常处理 |
| 400 | 请求参数错误 | 检查请求参数是否符合要求 |
| 404 | 资源不存在 | 检查请求路径是否正确 |
| 500 | 服务器内部错误 | 联系管理员或稍后重试 |

### HTTP 状态码

| 状态码 | 说明 | 场景 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 400 | Bad Request | 请求参数错误 |
| 404 | Not Found | 接口路径不存在 |
| 405 | Method Not Allowed | 请求方法不支持 |
| 500 | Internal Server Error | 服务器内部错误 |

---

## 附录

### A. 时间戳获取示例

#### Python

```python
from datetime import datetime

# 获取当前时间戳
now = datetime.now().timestamp()
print(now)  # 1776589846.8984776

# 获取指定时间的时间戳
dt = datetime(2026, 4, 19, 10, 30, 0)
timestamp = dt.timestamp()
print(timestamp)
```

#### JavaScript

```javascript
// 获取当前时间戳（秒）
const now = Math.floor(Date.now() / 1000);
console.log(now);

// 获取指定时间的时间戳
const dt = new Date('2026-04-19T10:30:00');
const timestamp = Math.floor(dt.getTime() / 1000);
console.log(timestamp);
```

### B. 常用时间范围

| 描述 | 时间范围计算 |
|------|--------------|
| 最近 1 小时 | end_time - 3600 |
| 最近 1 天 | end_time - 86400 |
| 最近 7 天 | end_time - 604800 |
| 最近 30 天 | end_time - 2592000 |

### C. 测试 URL 列表

| 接口 | 测试 URL |
|------|----------|
| IP 出现次数统计 | `http://10.0.48.241:5000/api/ip-counts?start_time=0&end_time=9999999999` |
| 扫描次数 | `http://10.0.48.241:5000/api/scan-count?start_time=0&end_time=9999999999` |
| 坊内 IP 列表 | `http://10.0.48.241:5000/api/fang-ips` |
| IP 范围 | `http://10.0.48.241:5000/api/ip-range` |

### D. 配置说明

#### 坊内 IP 范围

```python
# 坊内 IP 地址段
FANG_IPS = [
    153-174,    # 10.0.48.153 - 10.0.48.174
    176-180,    # 10.0.48.176 - 10.0.48.180
    185-190,    # 10.0.48.185 - 10.0.48.190
    226-249     # 10.0.48.226 - 10.0.48.249
]
```

#### 扫描 IP 范围

```python
# 扫描 IP 地址段
IP_RANGE = 151-250  # 10.0.48.151 - 10.0.48.250
```

### E. 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-19 | 初始版本，包含 4 个基础接口 |

---

**文档维护**: AiWorkShop 开发团队  
**联系方式**: 如有问题请联系开发团队
