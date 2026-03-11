"""
拼图配征信识别 API - Python 调用示例

官网: https://www.ipipei.com
文档: https://github.com/ipipei/credit-ocr-sdk/docs/API.md
咨询: 188 9871 0887
"""

import requests
import time
import json


class IPIPEIClient:
    """拼图配征信识别 API 客户端"""

    def __init__(self, token, base_url="https://api.ipipei.com"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {token}"
        }

    def _gen_request_code(self):
        return f"req_{int(time.time() * 1000)}"

    def upload(self, file_url, analysis_type, file_type, file_name=None, password=None, need_report=False):
        """
        上传文件进行识别

        Args:
            file_url: 文件URL地址（多张图片用逗号分隔）
            analysis_type: 文件类型 - 详版征信/简版征信/企业征信/流水/其他
            file_type: 格式类型 - pdf/img/excel
            file_name: 文件名（PDF必填）
            password: PDF加密密码（可选）
            need_report: 是否需要AI分析报告

        Returns:
            result_id: 结果ID，用于查询解析结果
        """
        payload = {
            "requestCode": self._gen_request_code(),
            "analysisType": analysis_type,
            "fileType": file_type,
            "filePackage": file_url,
        }

        if file_name:
            payload["fileName"] = file_name
        if password:
            payload["passWord"] = password
        if need_report:
            payload["isNeedReport"] = "1"

        resp = requests.post(
            f"{self.base_url}/enterpriseApi/fileUpload",
            json=payload,
            headers=self.headers
        )
        result = resp.json()

        if result.get("code") == "200":
            return result["data"]
        else:
            raise Exception(f"上传失败: {result.get('msg', '未知错误')}")

    def get_result(self, result_id, need_pdf_address=True):
        """
        查询单次解析结果

        Args:
            result_id: 上传接口返回的结果ID
            need_pdf_address: 是否返回PDF报告地址

        Returns:
            解析结果字典
        """
        payload = {
            "requestCode": self._gen_request_code(),
            "resultId": result_id,
            "isPdfAddress": "1" if need_pdf_address else ""
        }

        resp = requests.post(
            f"{self.base_url}/enterpriseApi/fileResult",
            json=payload,
            headers=self.headers
        )
        return resp.json()

    def wait_for_result(self, result_id, max_retries=30, interval=5):
        """
        轮询等待解析完成

        Args:
            result_id: 结果ID
            max_retries: 最大重试次数
            interval: 轮询间隔（秒）

        Returns:
            解析结果数据
        """
        for i in range(max_retries):
            result = self.get_result(result_id)

            if result.get("code") != "200":
                raise Exception(f"查询失败: {result.get('msg')}")

            data = result["data"]
            status = data.get("isSuccess", "0")

            if status == "1":
                return data
            elif status == "2":
                raise Exception(f"解析失败: {data.get('errorMessage', '未知错误')}")

            print(f"[{i+1}/{max_retries}] 解析中，{interval}秒后重试...")
            time.sleep(interval)

        raise TimeoutError("解析超时，请稍后重试")

    def get_quota(self):
        """查询企业使用剩余额度"""
        payload = {
            "pageNum": "1",
            "pageSize": "500"
        }
        resp = requests.post(
            f"{self.base_url}/enterpriseApi/fileFileCount",
            json=payload,
            headers=self.headers
        )
        return resp.json()


# ============ 使用示例 ============

if __name__ == "__main__":
    # 初始化客户端
    client = IPIPEIClient(token="your_api_token_here")

    # --- 示例1: 上传PDF征信报告 ---
    print("=" * 50)
    print("示例1: 上传PDF征信报告")
    print("=" * 50)

    try:
        result_id = client.upload(
            file_url="https://your-server.com/files/credit_report.pdf",
            analysis_type="详版征信",
            file_type="pdf",
            file_name="credit_report.pdf",
            need_report=True
        )
        print(f"上传成功, resultId: {result_id}")

        data = client.wait_for_result(result_id)
        print(f"文件名: {data.get('fileName')}")
        print(f"页数: {data.get('pageCount')}")
        print(f"类型: {data.get('fileType')}")
        print(f"征信数据: {data.get('creditMessage_new', '')[:200]}...")

    except Exception as e:
        print(f"错误: {e}")

    # --- 示例2: 上传图片征信报告（多张） ---
    print("\n" + "=" * 50)
    print("示例2: 上传图片征信报告")
    print("=" * 50)

    try:
        result_id = client.upload(
            file_url="https://your-server.com/img/page1.png,https://your-server.com/img/page2.png",
            analysis_type="简版征信",
            file_type="img"
        )
        print(f"上传成功, resultId: {result_id}")

    except Exception as e:
        print(f"错误: {e}")

    # --- 示例3: 上传银行流水 ---
    print("\n" + "=" * 50)
    print("示例3: 上传银行流水")
    print("=" * 50)

    try:
        result_id = client.upload(
            file_url="https://your-server.com/files/bank_statement.xlsx",
            analysis_type="流水",
            file_type="excel",
            file_name="bank_statement.xlsx"
        )
        print(f"上传成功, resultId: {result_id}")

    except Exception as e:
        print(f"错误: {e}")

    # --- 示例4: 查询企业额度 ---
    print("\n" + "=" * 50)
    print("示例4: 查询企业使用额度")
    print("=" * 50)

    try:
        quota = client.get_quota()
        print(json.dumps(quota, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"错误: {e}")
