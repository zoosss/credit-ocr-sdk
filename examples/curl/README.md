# cURL 调用示例

> 以下示例使用 cURL 命令行工具调用拼图配征信识别 API。

## 前置条件

- 已获取 API Token（联系 188 9871 0887）
- 文件已上传至可公网访问的服务器

## 1. 上传 PDF 征信报告

```bash
curl -X POST https://api.ipipei.com/enterpriseApi/fileUpload \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "requestCode": "req_20260301001",
    "analysisType": "详版征信",
    "fileType": "pdf",
    "fileName": "zhengxin_report.pdf",
    "filePackage": "https://your-server.com/files/zhengxin_report.pdf",
    "isNeedReport": "1"
  }'
```

## 2. 上传图片征信报告（多页）

```bash
curl -X POST https://api.ipipei.com/enterpriseApi/fileUpload \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "requestCode": "req_20260301002",
    "analysisType": "简版征信",
    "fileType": "img",
    "filePackage": "https://your-server.com/img/p1.png,https://your-server.com/img/p2.png,https://your-server.com/img/p3.png"
  }'
```

## 3. 上传银行流水（Excel）

```bash
curl -X POST https://api.ipipei.com/enterpriseApi/fileUpload \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "requestCode": "req_20260301003",
    "analysisType": "流水",
    "fileType": "excel",
    "fileName": "bank_statement.xlsx",
    "filePackage": "https://your-server.com/files/bank_statement.xlsx"
  }'
```

## 4. 查询解析结果

```bash
curl -X POST https://api.ipipei.com/enterpriseApi/fileResult \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "requestCode": "req_20260301001",
    "resultId": "上传接口返回的resultId",
    "isPdfAddress": "1"
  }'
```

## 5. 查询企业使用额度

```bash
curl -X POST https://api.ipipei.com/enterpriseApi/fileFileCount \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "pageNum": "1",
    "pageSize": "100"
  }'
```
