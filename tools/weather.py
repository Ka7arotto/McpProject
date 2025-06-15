import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP


#OpenWeather API配置
OPENWEATHER_API="https://api.openweathermap.org/data/2.5/weather"
API_KEY="6444ff26b36d8fa88eaaf862445e138f"
USER_AGENT="weather-app/1.0"
#初始化MCP服务器
mcp=FastMCP()



async def get_weather(city:str)->dict[str,Any]|None:
    """
    获取指定城市的天气信息
    :param city: 城市名称(需要英文)
    :return: 天气信息字典或None
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 中文
    }
    headers={"User-Agent": USER_AGENT}

    async with httpx.AsyncClient() as client:
        try:
            response=await client.get(OPENWEATHER_API,params=params,
            headers=headers,timeout=30.0)
            response.raise_for_status()  # 检查请求是否成功
            # 解析JSON响应
            return response.json()
        except httpx.HTTPStatusError as e:
            
            return {"error":f"请求失败：{e.response.status_code} {e.response.reason_phrase}"}
        except Exception as e:
            return {"error":f"请求失败：{str(e)}"}

def format_weather(data:dict[str,Any]|str)->str:
    """
    格式化天气信息
    :param data: 天气信息字典或错误信息字符串
    :return: 格式化后的天气信息字符串
    """
    if isinstance(data, str):
        try:
            data=json.loads(data)
        except Exception as e:
            return f"数据解析错误：{str(e)}"
        
    if "error" in data:
        return f"错误：{data['error']}"

     # 提取数据时做容错处理
    city = data.get("name", "未知")
    country = data.get("sys", {}).get("country", "未知")
    temp = data.get("main", {}).get("temp", "N/A")
    humidity = data.get("main", {}).get("humidity", "N/A")
    wind_speed = data.get("wind", {}).get("speed", "N/A")
    # weather 可能为空列表，因此用 [0] 前先提供默认字典
    weather_list = data.get("weather", [{}])
    description = weather_list[0].get("description", "未知")
 
    return (
        f"🌍 {city}, {country}\n"
        f"🌡 温度: {temp}°C\n"
        f"💧 湿度: {humidity}%\n"
        f"🌬 风速: {wind_speed} m/s\n"
        f"🌤 天气: {description}\n"
    )
    

@mcp.tool()
async def query_weather(city:str)->str:
    """
    查询指定城市的天气信息
    :param city: 城市名称(英文)
    :return: 格式化后的天气信息字符串
    """
    data=await get_weather(city)
    return format_weather(data)

if __name__ == "__main__":
    # 启动I/O MCP服务器
    mcp.run(transport='stdio')

