<h1 align="center">Welcome to mcp_server 👋</h1>
<p>
</p>

# MCP 开发应用

## 项目结构

```
mcp_server/
├── __init__.py
├── .env
├── .python-version
├── client.py
├── fscan.py
├── get-pip.py
├── mcp_server.code-workspace
├── pyproject.toml
├── README.md
├── test.py
├── test.txt
├── uv.lock
├── __pycache__/
│   ├── config.cpython-313.pyc
│   └── main.cpython-313.pyc
└── tools/
    ├── __init__.py
    ├── file.py
    ├── fscan.py
    ├── tempCodeRunnerFile.py
    ├── test.py
    ├── weather.py
    └── wy.py
```

## 文件说明

-   `client.py`: MCP 客户端，用于连接到 MCP 服务器。
-   `tools/file.py`: MCP 工具文件，包含多个工具函数。
-   `tools/weather.py`: 示例工具文件，用于天气相关功能。
-   `.env`: 环境变量配置文件。
-   `pyproject.toml`: 项目配置文件，包含依赖和元信息。
-   `README.md`: 项目说明文件。
-   `test.py`: 测试脚本。
-   `tools/tempCodeRunnerFile.py`: 临时代码运行文件。

## Usage

```sh
python client.py tools/weather.py
```

## Author

👤 **goku**

-   Github: [@goku](https://github.com/Ka7arotto)

## Show your support

Give a ⭐️ if this project helped you!
