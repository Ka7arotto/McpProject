from typing import Any
from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import os


#初始化MCP服务器
mcp=FastMCP()

@mcp.tool("get_content")
async def get_content(path:str)->dict[str,Any]|None:
    """
    获取指定路径的内容
    :param path: 文件路径
    :return: 文件内容字典或None
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        return {"content": content}
    except FileNotFoundError:
        return {"error": "文件未找到"}
    except Exception as e:
        return {"error": f"读取文件失败：{str(e)}"}

@mcp.tool("write_content")
async def write_content(path:str, content:str)->dict[str,Any]|None:
    """
    写入内容到指定路径的文件
    :param path: 文件路径
    :param content: 要写入的内容
    :return: 成功或错误信息字典
    """
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        return {"message": "内容写入成功"}
    except Exception as e:
        return {"error": f"写入文件失败：{str(e)}"}

@mcp.tool("list_files")
async def list_files(directory:str)->dict[str,Any]|None:
    """
    列出指定目录下的所有文件
    :param directory: 目录路径
    :return: 文件列表字典或错误信息字典
    """
    try:
        files = os.listdir(directory)
        return {"files": files}
    except FileNotFoundError:
        return {"error": "目录未找到"}
    except Exception as e:
        return {"error": f"列出文件失败：{str(e)}"}

if __name__ == "__main__":
    mcp.run(transport='stdio')