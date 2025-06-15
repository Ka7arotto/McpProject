import asyncio
from dotenv import load_dotenv
from typing import Optional
from contextlib import AsyncExitStack
import json
from openai import OpenAI

from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
import sys


class MCPClient:
    def __init__(self):
        '''Initialize the MCPClient'''

        self.openai_api_key="sk-blvnnivvsysypkenyyywxaxjtageyowdviqcdzgyzgrqxarx"
        self.base_url="https://api.siliconflow.cn/v1/" 
        self.model="Qwen/Qwen3-32B" 
        # self.openai_api_key="sk-blvnnivvsysypkenyyywxaxjtageyowdviqcdzgyzgrqxarx"
        # self.base_url="https://api.siliconflow.cn/v1/" 
        # self.model="Qwen/Qwen3-8B"
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is not set in the environment variables.")
        #创建 OpenAI 客户端实例
        self.client=OpenAI(api_key=self.openai_api_key, base_url=self.base_url) #OpenAI 类: 这是 OpenAI 官方 Python 客户端库的主要类，用于与 OpenAI 的 API 进行交互
        self.session: Optional[ClientSession]=None
        self.exit_stack=AsyncExitStack()

    
    async def connect_to_server(self,server_script_path:str):

        
        '''连接到MCP服务器并列出可用的工具'''
        is_python=server_script_path.endswith('.py')
        if_js=server_script_path.endswith('.js')
        if not (is_python or if_js):
            raise ValueError("Server script must be a Python (.py) or JavaScript (.js) file.")
        
        #确定执行命令python or node
        command="python" if is_python else "node"
        server_params=StdioServerParameters(
            command=command, 
            args=[server_script_path],
            env=None
        )

        #启动MCP服务器并建立通信
        stdio_transport=await self.exit_stack.enter_async_context(
            stdio_client(server_params)#用于创建一个标准输入/输出（stdio）的客户端传输层
        )
        self.stdio,self.write=stdio_transport
        self.session=await self.exit_stack.enter_async_context(
            ClientSession(
                self.stdio,
                self.write,
            )
        )

        await self.session.initialize()

        # 获取可用工具列表
        response=await self.session.list_tools()
        tools=response.tools
        print("\n已连接到服务器，支持以下工具：",[tool.name for tool in tools])

    async def process_query(self,query:str)->str:
        '''
        使用大模型处理查询并调用可用的MCP工具（Function）
        '''
        messages=[{"role":"user","content":query}]
        response=await self.session.list_tools()

        available_tools=[{
            "type":"function",
            "function":{
                "name":tool.name,
                "description":tool.description,
                "input_schema":tool.inputSchema
            }
        }for tool in response.tools]

        response=self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=available_tools
        )

        #处理返回内容
        content=response.choices[0]
        if content.finish_reason=="tool_calls":
            #如果是需要使用工具，就解析工具
            tool_call=content.message.tool_calls[0]
            tool_name=tool_call.function.name
            tool_args=json.loads(tool_call.function.arguments)
        
            #执行工具
            result=await self.session.call_tool(tool_name,tool_args)
            print(f"\n\n🌟Calling tool {tool_name} with args {tool_args} ....\n\n")

            #将模型返回的调用的tool和tool执行后的数据存入
            messages.append(content.message.model_dump())
            messages.append({
                "role":"tool",
                "content":result.content[0].text,
                "tool_call_id":tool_call.id
            })

            #将上面结果返回给大模型用于生产最终的结果
            response=self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        return content.message.content

    async def chat_loop(self):
        ''''运行交互式聊天循环'''
        print("\n🤖 MCP客户端已启动！输入 'quit' 退出")

        while True:
            try:
                query= input("\n请输入您的查询（或输入 'quit' 退出）：")
                if query.lower() == 'quit':
                    print("退出聊天...")
                    break
                response=await self.process_query(query)
                print(f"\n🤖 OpenAI：{response}")
           
            except Exception as e:
                print(f"发生错误：{str(e)}")

    async def close(self):
        '''关闭MCP客户端'''
        await self.exit_stack.aclose()
        print("MCP客户端已关闭。")
    
async def main():
    if len(sys.argv) < 2:
        print("🌟 Usage: python client.py <path_to_server_srcipt>")
        sys.exit(1)
    client=MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.close()
if __name__ == "__main__":
    import sys
    asyncio.run(main())