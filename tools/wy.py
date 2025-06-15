import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP


#信息检索系统api
API="http://127.0.0.1:8000/retrieve"


#初始化MCP服务器
mcp=FastMCP()

import requests
from typing import Dict, Any

API = "http://127.0.0.1:8000/retrieve"

@mcp.tool()
def get_answer(query: str) -> Dict[str, Any] | None:
    """
    获取指定问题的答案（同步 requests 版本）
    :param query: 医疗问题字符串
    :return: 答案信息字典或None
    """
    params = {"query": query}

    try:
        response = requests.post(API, data=params,  timeout=30.0)
        response.raise_for_status()  # 检查请求是否成功
        with open("tools/wy.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        

        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"请求失败：{e.response.status_code} {e.response.reason_phrase}"}
    except Exception as e:
        return {"error": f"请求失败：{str(e)}"}
        

if __name__ == "__main__":
    # 启动I/O MCP服务器
    mcp.run(transport='stdio')