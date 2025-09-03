# MCP客户端实现

基于Model Context Protocol (MCP) 的Python客户端实现，参考了官方文档和TypeScript版本。

## 功能特性

- ✅ MCP服务器连接管理
- ✅ 工具发现和调用
- ✅ 异步操作支持
- ✅ 资源清理和错误处理
- ✅ 与OpenAI聊天集成

## 文件结构

```
my/
├── mcp_client.py          # 主MCP客户端实现
├── chat_openai.py         # OpenAI聊天客户端
├── test_mcp_client.py     # 客户端测试脚本
├── example_integration.py # MCP与OpenAI集成示例
└── README_MCP_CLIENT.md   # 本文档
```

## 快速开始

### 1. 安装依赖

确保已安装所需的Python包：

```bash
pip install mcp openai python-dotenv pydantic rich
```

### 2. 创建MCP客户端

```python
from my.mcp_client import MCPClient

# 创建客户端实例
client = MCPClient(
    name="MyClient",
    command="python",  # 或 "node" 对于JavaScript服务器
    args=["path/to/your/server.py"]  # 服务器脚本路径
)

# 连接到服务器
await client.init()

# 获取可用工具
tools = client.get_tools()
print("Available tools:", [tool.name for tool in tools])

# 调用工具
result = await client.call_tool("tool_name", {"param": "value"})

# 清理资源
await client.close()
```

### 3. 与OpenAI集成

```python
from my.mcp_client import MCPClient
from my.chat_openai import AsyncChatOpenAI

# 创建MCP客户端并连接
mcp_client = MCPClient(...)
await mcp_client.init()

# 创建OpenAI聊天客户端，使用MCP工具
chat_client = AsyncChatOpenAI(
    model="gpt-3.5-turbo",
    tools=mcp_client.get_tools()
)

# 进行聊天，自动处理工具调用
response = await chat_client.chat("请使用工具查询信息")
```

## API参考

### MCPClient类

#### 初始化
```python
MCPClient(name: str, command: str, args: list[str], version: str = "1.0.0")
```

#### 方法
- `async init()`: 初始化并连接到服务器
- `async connect_to_server()`: 连接到MCP服务器
- `async call_tool(name: str, params: dict)`: 调用指定工具
- `async close()`: 关闭连接并清理资源
- `get_tools()`: 获取可用工具列表

### 错误处理

客户端包含完善的错误处理机制：
- 连接失败时抛出 `ConnectionError`
- 工具调用失败时抛出 `ValueError`
- 所有操作都有适当的异常捕获和日志记录

## 示例用法

### 基本测试
```bash
python my/test_mcp_client.py
```

### 集成演示
```bash
python my/example_integration.py
```

## 注意事项

1. **服务器路径**: 需要替换示例中的服务器路径为实际的MCP服务器脚本
2. **环境变量**: 确保设置了正确的OpenAI API密钥和环境变量
3. **异步操作**: 所有方法都是异步的，需要在异步环境中运行
4. **资源管理**: 使用 `AsyncExitStack` 确保资源正确清理

## 基于的参考

- [MCP官方Python快速开始](https://modelcontextprotocol.io/quickstart/client)
- TypeScript MCP客户端实现 (`my/MCPClient.ts`)
- OpenAI聊天客户端实现 (`my/chat_openai.py`)

## 扩展建议

1. 添加更多工具调用示例
2. 实现工具调用结果的自动处理
3. 添加对话历史管理
4. 支持多种LLM提供商
5. 添加GUI界面

## 故障排除

如果遇到连接问题：
1. 检查服务器路径是否正确
2. 确认服务器脚本有执行权限
3. 检查网络连接和防火墙设置
4. 查看详细的错误日志
