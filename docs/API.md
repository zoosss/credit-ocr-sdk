# 拼图配征信识别 API 接口文档

> 版本：v2.3 | 更新日期：2026-03-01
>
> 基础地址：`https://api.ipipei.com`

---

## 目录

- [鉴权说明](#鉴权说明)
- [接口列表](#接口列表)
  - [2.3.1.1 文件上传接口](#2311-文件上传接口)
  - [2.3.1.2 文件解析结果](#2312-文件解析结果)
  - [2.3.1.3 企业使用剩余额度](#2313-企业使用剩余额度)
- [错误码说明](#错误码说明)
- [文件限制说明](#文件限制说明)

---

## 鉴权说明

所有接口均需在请求头中携带 `Authorization` 字段进行身份验证。

| Header | 必选 | 类型 | 说明 |
|--------|:---:|------|------|
| Content-Type | 是 | String | `application/json; charset=UTF-8` |
| Authorization | 是 | String | `Bearer {your_token}` |

> 如需获取 API Token，请联系商务团队：**188 9871 0887**

---

## 接口列表

### 2.3.1.1 文件上传接口

上传征信报告、银行流水等信贷文件进行识别与解析。

- **接口地址**：`/enterpriseApi/fileUpload`
- **请求方式**：`POST`
- **Content-Type**：`application/json`

#### 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|--------|:---:|------|------|
| requestCode | 是 | String | 本次请求标识（建议使用UUID） |
| fileName | 否 | String | 文件名称。**PDF文件必填**，以传入的文件名为准；图片不需要传入 |
| analysisType | 是 | String | 文件证件类型。可选值：`详版征信` / `简版征信` / `企业征信` / `流水` / `其他` |
| fileType | 是 | String | 文件格式类型。可选值：`pdf` / `img` / `excel` |
| passWord | 否 | String | PDF文件如果是加密的情况下，必须传入密码 |
| filePackage | 是 | String | 文件包（文件URL地址）。PDF一次只能识别一份，不能传多份；图片可多张（但是一份），多张用逗号隔开 |
| isNeedReport | 否 | String | AI分析内容，传入 `"1"` 即可开启（目前只支持简版征信） |

#### 文件上传类型要求

| 文件类型 | 大小限制 | 格式要求 |
|---------|---------|---------|
| 详版征信 PDF | ≤ 100M | PDF格式 |
| 简版征信 PDF | ≤ 15M | PDF格式 |
| 企业征信 | ≤ 1M | PDF格式 |
| 流水 | ≤ 10M | PDF 或 Excel（xls/xlsx/csv），**不支持** png、jpg等图片格式 |

> **注意**：
> - `fileType` 为 `img` 时，`filePackage` 传入图片类型URL，可传入多份，用逗号隔开
> - `fileType` 为 `pdf` 时，`filePackage` 传入PDF文件URL
> - `fileType` 为 `excel` 时，只能传入 xls/xlsx/csv 文件格式类型

#### 请求示例

**PDF文件请求：**

```json
{
  "requestCode": "21xzc41zxv4d4vvf6rvfd321vbdf654bdf65b1",
  "analysisType": "简版征信",
  "fileName": "xxxxxxx111.pdf",
  "fileType": "pdf",
  "filePackage": "https://www.xxxxxx.com/profile/fileAndImg/xxxxxxx111.pdf"
}
```

**图片请求（多张）：**

```json
{
  "requestCode": "21xzc41zxv4d4vvf6rvfd321vbdf654bdf65b1",
  "analysisType": "简版征信",
  "fileType": "img",
  "filePackage": "https://www.xxxxxx.com/profile/fileAndImg/1.png,https://www.xxxxxx.com/profile/fileAndImg/2.png"
}
```

**通用请求示例：**

```json
{
  "requestCode": "4xc89z74x89c4xz98c489zx",
  "analysisType": "详版征信/简版征信/企业征信/流水",
  "fileType": "pdf/img",
  "filePackage": "https://189.494.591.100/4155456456.png,https://189.494.591.100/4155456456.png"
}
```

#### 成功响应

```json
{
  "msg": "操作成功",
  "code": "200",
  "data": "1545156416516548"
}
```

> `data` 字段返回 32 位标识，即 `resultId`，用于调用 [文件解析结果接口](#2312-文件解析结果) 查询结果。

#### 失败响应

```json
{
  "msg": "操作失败，文件传入类型不匹配。",
  "code": "500",
  "data": ""
}
```

---

### 2.3.1.2 文件解析结果

通过文件上传接口获取到的 `resultId` 调用此接口，获取文件解析结果。

> 如果接口返回的 `isSuccess` 为 `0`，说明文件仍在解析中，请稍后重试。

- **接口地址**：`/enterpriseApi/fileResult`
- **请求方式**：`POST`
- **Content-Type**：`application/json`

#### 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|--------|:---:|------|------|
| requestCode | 是 | String | 本次请求标识 |
| resultId | 是 | String | 传入上传接口返回的结果ID |
| isPdfAddress | 否 | String | 是否需要返回报告PDF文件地址，传入 `"1"` 即可 |

#### 请求示例

```json
{
  "requestCode": "4xc89z74x89c4xz98c489zx",
  "resultId": "789xz7c89xz4c89xz4c9x8z4c",
  "isPdfAddress": ""
}
```

#### 成功响应

```json
{
  "msg": "操作成功",
  "code": "200",
  "data": {
    "fileName": "杨测试",
    "pageCount": 20,
    "creationTime": "具体调用时间",
    "errorMessage": "错误信息",
    "fileAliasName": "流水解析成功",
    "fileType": "流水/简版征信/企业征信/详版征信/其他",
    "imgType": "文字版",
    "isSuccess": "0",
    "actualFileType": "流水/简版征信/详版征信/其他",
    "reportAddress": "",
    "pdfAddressUrl": "",
    "creditMessage": "",
    "creditMessage_new": "",
    "analysisReport": ""
  }
}
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| fileName | String | 文件名称 |
| pageCount | Integer | 本次传入的文件页数 |
| creationTime | String | 具体调用时间 |
| errorMessage | String | 错误信息 |
| fileAliasName | String | 文件别名/解析状态描述 |
| fileType | String | 证件类型：`流水` / `简版征信` / `企业征信` / `详版征信` / `其他` |
| imgType | String | `文字版` / `图片版` |
| isSuccess | String | `0` = 解析中，`1` = 解析完成，`2` = 解析失败 |
| actualFileType | String | 实际文件类型。如果不为空，则说明客户上传的类型和选择的类型不符合 |
| reportAddress | String | 报告URL地址（目前提供所有报告） |
| pdfAddressUrl | String | PDF报告URL地址（目前提供所有报告） |
| creditMessage | String | 流水和企业征信数据（取这个值） |
| creditMessage_new | String | 简版征信和详版征信数据（取这个值） |
| analysisReport | String | AI分析内容（目前只支持简版征信） |

#### isSuccess 状态说明

| 值 | 状态 | errorMessage |
|---|------|-------------|
| 0 | 解析中 | 一定为空 |
| 1 | 解析成功 | 一定为空 |
| 2 | 解析失败 | 一定不为空，包含详细的错误提示 |

#### 失败响应

```json
{
  "msg": "操作失败，具体的错误类型",
  "code": "500",
  "data": ""
}
```

---

### 2.3.1.3 企业使用剩余额度

该接口主要服务与对接的企业，针对文件上传的使用次数进行统计和剩余额度查询。无需传参即可查询。

- **接口地址**：`/enterpriseApi/fileFileCount`
- **请求方式**：`POST`
- **Content-Type**：`application/json`

#### 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|--------|:---:|------|------|
| pageNum | 否 | String | 当前页码 |
| pageSize | 否 | String | 总条数 |
| requestCode | 否 | String | 本次请求标识 |
| resultId | 否 | String | 查看具体的文件 resultId 标识 |

#### 请求示例

```json
{
  "pageNum": "1",
  "pageNum": "500",
  "requestCode": "UUID 32 位或时间戳",
  "resultId": "文件的结果Id UUID 32"
}
```

> **注意**：最多可查询 500 份文件，超过按 500 份文件返回。

---

## 错误码说明

| 错误码 | 说明 |
|-------|------|
| 200 | 操作成功 |
| 500 | 操作失败（具体原因见 msg 字段） |

---

## 文件限制说明

| 文件类型 | 最大大小 | 支持格式 |
|---------|---------|---------|
| 详版征信 PDF | 100M | PDF |
| 简版征信 PDF | 15M | PDF |
| 企业征信 | 1M | PDF |
| 流水文件 | 10M | PDF / Excel（xls/xlsx/csv） |
| 图片文件 | - | PNG / JPG / TIFF 等 |

---

## 接入支持

如需获取 API Token 或技术支持，请联系我们：

- 📞 **产品咨询**：188 9871 0887
- 🌐 **官网**：[www.ipipei.com](https://www.ipipei.com)
- 📧 **邮箱**：hrd@IPIPEI.com

---

<div align="center">

**© 2023-2026 湖南拼图配人工智能应用软件有限公司**

</div>
