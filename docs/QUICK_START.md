# 快速接入指南

> 本文档帮助您在最短时间内完成拼图配征信识别 API 的接入。

---

## 接入流程

```
联系商务获取Token ──→ 阅读API文档 ──→ 调用上传接口 ──→ 轮询获取结果
```

### 第一步：获取 API Token

联系拼图配商务团队获取企业专属 API Token：

- 📞 **188 9871 0887**
- 🌐 [www.ipipei.com](https://www.ipipei.com)

### 第二步：上传文件

将征信报告或银行流水文件上传至您的文件服务器，获取可公网访问的 URL 地址。

### 第三步：调用上传接口

调用 `enterpriseApi/fileUpload` 接口提交文件进行识别。

### 第四步：查询解析结果

使用上传接口返回的 `resultId`，调用 `enterpriseApi/fileResult` 接口获取解析结果。

> 文件解析为异步操作，`isSuccess` 为 `0` 时表示仍在解析中，建议间隔 3-5 秒轮询。

---

## 代码示例

### Python

```python
import requests
import time

BASE_URL = "https://api.ipipei.com"
TOKEN = "your_api_token"

HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "Authorization": f"Bearer {TOKEN}"
}


def upload_credit_file(file_url, analysis_type="详版征信", file_type="pdf", file_name=None):
    """上传征信文件进行识别"""
    payload = {
        "requestCode": f"req_{int(time.time() * 1000)}",
        "analysisType": analysis_type,
        "fileType": file_type,
        "filePackage": file_url,
        "isNeedReport": "1"
    }
    if file_name and file_type == "pdf":
        payload["fileName"] = file_name

    resp = requests.post(f"{BASE_URL}/enterpriseApi/fileUpload", json=payload, headers=HEADERS)
    result = resp.json()

    if result["code"] == "200":
        print(f"上传成功，resultId: {result['data']}")
        return result["data"]
    else:
        print(f"上传失败: {result['msg']}")
        return None


def get_parse_result(result_id, max_retries=20, interval=5):
    """轮询获取解析结果"""
    request_code = f"req_{int(time.time() * 1000)}"

    for i in range(max_retries):
        payload = {
            "requestCode": request_code,
            "resultId": result_id,
            "isPdfAddress": "1"
        }
        resp = requests.post(f"{BASE_URL}/enterpriseApi/fileResult", json=payload, headers=HEADERS)
        result = resp.json()

        if result["code"] != "200":
            print(f"查询失败: {result['msg']}")
            return None

        data = result["data"]
        status = data.get("isSuccess", "0")

        if status == "1":
            print("解析完成！")
            return data
        elif status == "2":
            print(f"解析失败: {data.get('errorMessage', '未知错误')}")
            return None
        else:
            print(f"解析中... ({i + 1}/{max_retries})")
            time.sleep(interval)

    print("超时：文件解析未完成")
    return None


if __name__ == "__main__":
    # 上传PDF征信报告
    result_id = upload_credit_file(
        file_url="https://your-server.com/files/credit_report.pdf",
        analysis_type="详版征信",
        file_type="pdf",
        file_name="credit_report.pdf"
    )

    if result_id:
        # 轮询获取结果
        data = get_parse_result(result_id)
        if data:
            print(f"文件名: {data.get('fileName')}")
            print(f"页数: {data.get('pageCount')}")
            print(f"文件类型: {data.get('fileType')}")
            # 征信数据在 creditMessage_new 字段中
            credit_data = data.get("creditMessage_new", "")
            if credit_data:
                print("征信数据获取成功")
```

### Java

```java
import java.net.http.*;
import java.net.URI;

public class CreditOcrClient {

    private static final String BASE_URL = "https://api.ipipei.com";
    private static final String TOKEN = "your_api_token";

    public static String uploadFile(String fileUrl, String analysisType, String fileType) throws Exception {
        String json = String.format("""
            {
                "requestCode": "req_%d",
                "analysisType": "%s",
                "fileType": "%s",
                "filePackage": "%s",
                "isNeedReport": "1"
            }
            """, System.currentTimeMillis(), analysisType, fileType, fileUrl);

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/enterpriseApi/fileUpload"))
                .header("Content-Type", "application/json; charset=UTF-8")
                .header("Authorization", "Bearer " + TOKEN)
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Response: " + response.body());
        return response.body();
    }

    public static String getResult(String resultId) throws Exception {
        String json = String.format("""
            {
                "requestCode": "req_%d",
                "resultId": "%s",
                "isPdfAddress": "1"
            }
            """, System.currentTimeMillis(), resultId);

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/enterpriseApi/fileResult"))
                .header("Content-Type", "application/json; charset=UTF-8")
                .header("Authorization", "Bearer " + TOKEN)
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
}
```

### cURL

```bash
# 1. 上传PDF征信文件
curl -X POST https://api.ipipei.com/enterpriseApi/fileUpload \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "requestCode": "unique-request-id-001",
    "analysisType": "详版征信",
    "fileType": "pdf",
    "fileName": "credit_report.pdf",
    "filePackage": "https://your-server.com/files/credit_report.pdf",
    "isNeedReport": "1"
  }'

# 2. 上传图片征信文件（多张）
curl -X POST https://api.ipipei.com/enterpriseApi/fileUpload \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "requestCode": "unique-request-id-002",
    "analysisType": "简版征信",
    "fileType": "img",
    "filePackage": "https://your-server.com/img/page1.png,https://your-server.com/img/page2.png"
  }'

# 3. 查询解析结果
curl -X POST https://api.ipipei.com/enterpriseApi/fileResult \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "requestCode": "unique-request-id-001",
    "resultId": "上传接口返回的resultId",
    "isPdfAddress": "1"
  }'

# 4. 查询企业使用额度
curl -X POST https://api.ipipei.com/enterpriseApi/fileFileCount \
  -H "Content-Type: application/json; charset=UTF-8" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "pageNum": "1",
    "pageSize": "500"
  }'
```

---

## 注意事项

1. **异步解析**：文件上传后为异步处理，需轮询 `fileResult` 接口获取结果
2. **轮询间隔**：建议 3-5 秒轮询一次，避免频繁请求
3. **文件大小**：注意不同类型文件的大小限制（详版征信 ≤100M，简版 ≤15M，企业征信 ≤1M，流水 ≤10M）
4. **文件URL**：`filePackage` 需传入可公网访问的文件URL地址
5. **数据安全**：建议使用 HTTPS 协议传输，文件URL建议设置有效期

---

## 获取帮助

- 📖 [完整API文档](API.md)
- 🌐 [官网](https://www.ipipei.com)
- 📞 技术支持：**188 9871 0887**
