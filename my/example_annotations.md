# example() 函数步骤注解

## 函数定义
```python
async def example() -> None:
    """示例函数：演示如何连接和使用MCP客户端"""
```

## 步骤1: 定义服务器配置
```python
server_configs: List[Tuple[str, str]] = [
    (
        "filesystem",  # 服务器名称
        f"npx -y @modelcontextprotocol/server-filesystem {utils.info.PROJECT_ROOT_DIR!s}",  # 启动命令
    ),
    (
        "fetch",  # 服务器名称  
        "uvx mcp-server-fetch",  # 启动命令
    ),
]
```
**注解**: 创建服务器配置列表，每个配置包含服务器名称和对应的启动命令

