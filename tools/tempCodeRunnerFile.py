import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP


#信息检索系统api
API="http://127.0.0.1:8000/retrieve"

params = {"query": "膀胱癌的治疗方案是什么？"}
headers = {"Content-Type": "text/plain"}
with httpx.Client() as client:

    response =  client.post(API, data=params, headers=headers,timeout=30.0)
    response.raise_for_status()  # 检查请求是否成功
        # 解析JSON响应
    print("\n获取到的答案：", response.json())
        