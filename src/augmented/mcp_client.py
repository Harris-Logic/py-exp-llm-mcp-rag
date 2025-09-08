"""
modified from https://modelcontextprotocol.io/quickstart/client  in tab 'python'
"""
import asyncio
from contextlib import AsyncExitStack
import contextlib
import os
# typing模块中的类型注解说明：
# List: 来自typing模块的泛型类型，用于类型注解，支持指定元素类型，如List[str]
# list: Python内置的列表类型，实际的数据结构
# 区别：List用于类型提示，list用于创建实际对象
# 在Python 3.9+中，可以直接用 list[str] 替代 List[str]
from typing import Optional, List, Dict, Any, Tuple
import typing
from mcp import Tool, ClientSession, StdioServerParameters
# import mcp.cli
import mcp.client
import mcp.client.session
from mcp.client.stdio import stdio_client
import mcp
import mcp.client.stdio
from mcp.types import ListToolsResult
# from openai import AsyncOpenAI
from dataclasses import dataclass, field

from openai.types import FunctionDefinition
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print as rprint

import shlex
# from utils import pretty
import utils.info
from utils.pretty import log_title
import utils
import utils.pretty

import try_mcp_client

load_dotenv()  # 读取.env里的API等信息
# 直接从chat_openai.py里拿过来 from import

class MCPClient:
    """
    MCP (Model Context Protocol) 客户端类
    用于连接和管理与 MCP 服务器的通信，获取和调用服务器提供的工具
    """
    
    def __init__(
            self, 
            name: str,
            command: str,
            args: List[str],
            version: str = "1.0.0"
    ) -> None:
        """
        初始化 MCP 客户端
        
        Args:
            name: 客户端名称，用于标识当前客户端实例
            command: 启动 MCP 服务器的命令路径（如: "node", "python", "npx" 等）
            args: 传递给服务器命令的参数列表（如: ["server.js", "--port", "3000"]）
            version: 客户端版本号，默认为 "1.0.0"
        
        Attributes:
            session: MCP 客户端会话对象，用于与服务器通信
            exit_stack: 异步上下文管理器，用于资源清理
            name: 存储客户端名称
            command: 存储服务器启动命令
            args: 存储命令参数
            version: 存储客户端版本
            tools: 从服务器获取的工具列表
        """
        # MCP 会话管理
        self.session: mcp.client.session.ClientSession | None
        # self.session: typing.Optional[mcp.client.session.ClientSession] = None # `Optional[X]` 等价于 `X | None`
        self.exit_stack: contextlib.AsyncExitStack = contextlib.AsyncExitStack()
        
        # 客户端基本信息
        self.name: str = name                    # 客户端标识名称
        self.command: str = command              # 服务器启动命令（如: "node", "python"）
        self.args: typing.List[str] = args              # 命令参数列表
        self.version: str = version              # 客户端版本号
        
        # 工具管理
        self.tools: typing.List[Tool] = []              # 存储从服务器获取的可用工具列表
    
    async def init(self) -> None:
        """初始化客户端，连接到服务器"""
        await self.connect_to_server()
        
    async def connect_to_server(self) -> None:
        """连接到MCP服务器
        
        创建与MCP服务器的连接，初始化会话，并获取服务器提供的工具列表
        
        Raises:
            ConnectionError: 如果连接服务器失败
            ValueError: 如果服务器响应无效
        """
        try:
            # 创建服务器参数配置
            server_params: mcp.client.stdio.StdioServerParameters = StdioServerParameters(
                command=self.command,
                args=self.args,
                env=None
            )
            
            # 创建标准输入输出传输通道
            stdio_transport: typing.Tuple[Any, Any] = await self.exit_stack.enter_async_context(
                mcp.client.stdio.stdio_client(server_params)
            )
            # 获取读写接口
            # self.stdio: Any
            # self.write: Any
            self.stdio, self.write = stdio_transport
            
            # 创建客户端会话
            self.session: mcp.client.session.ClientSession = await self.exit_stack.enter_async_context(
                ClientSession(self.stdio, self.write)
            )
            
            # 初始化会话
            await self.session.initialize()
            
            # 获取服务器提供的工具列表
            response: mcp.types.ListToolsResult = await self.session.list_tools()
            self.tools: List[Tool] = response.tools
            
            # 打印连接成功信息和可用工具
            rprint(f"\n✅ Connected to MCP server: ") #{self.name}
            # tool_names = []
            # for tool in self.tools:
            #     tool_names.append(tool.name)
            rprint("Available tools:", [tool.name for tool in self.tools])
            
        except Exception as error:
            rprint(f"❌ Failed to connect to MCP server: {error}")
            raise ConnectionError(f"Failed to connect to MCP server: {error}") from error
    
    async def close(self) -> None:
        """清理资源，关闭与服务器的连接"""
        await self.exit_stack.aclose()
        print("🔌 MCP client connection closed")
    
    async def call_tool(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用服务器上的特定工具
        
        Args:
            name: 工具名称
            params: 工具参数
            
        Returns:
            工具调用结果
            
        Raises:
            ValueError: 如果工具不存在或调用失败
        """
        if self.session is None:
            raise ValueError("Not connected to server")
        try:
            result: Dict[str, Any] = await self.session.call_tool(name, params)
            return result
        except Exception as error:
            raise ValueError(f"Tool call failed for {name}: {error}") from error
    
    def get_tools(self) -> List[Tool]:
        """返回从服务器获取的工具列表
        
        Returns:
            可用工具列表
        """
        return self.tools
    
async def example() -> None:
    """示例函数：演示如何连接和使用MCP客户端"""
    
    # 步骤1: 定义MCP服务器配置列表
    # 配置两个不同的MCP服务器：文件系统服务器和网络请求服务器
    # 
    # 类型注解解释：List[Tuple[str, str]]
    # - List: 来自typing模块的泛型类型，用于类型提示（Type Hinting）
    # - list: Python内置类型，用于创建实际的列表对象，如 list() 或 []
    # - List[Tuple[str, str]] 表示：这是一个列表，包含多个元组，每个元组包含两个字符串
    # - 等价写法（Python 3.9+）: list[tuple[str, str]]
    # - 实际创建对象使用的是 [] ，这是 list 类型的字面量语法
    server_configs: List[Tuple[str, str]] = [
        (
            "filesystem",  # 服务器名称：文件系统操作服务器
            f"npx -y @modelcontextprotocol/server-filesystem {utils.info.PROJECT_ROOT_DIR!s}",  # 启动命令：使用npx运行文件系统服务器，指定项目根目录
        ),
        (
            "fetch",  # 服务器名称：HTTP请求服务器
            "uvx mcp-server-fetch",  # 启动命令：使用uvx运行网络请求服务器
        ),
    ]
    
    # 步骤2: 遍历每个服务器配置，逐一连接和测试
    for mcp_name, cmd in server_configs:
        # 步骤2.1: 显示当前正在处理的服务器名称（用于日志分隔和识别）
        utils.pretty.log_title(mcp_name)
        
        # 步骤2.2: 解析命令字符串为命令和参数列表
        # 使用shlex.split()正确处理带空格和引号的命令行参数
        parts: List[str] = shlex.split(cmd)
        command: str = parts[0]      # 提取主命令（如：npx, uvx）
        args: List[str] = parts[1:]  # 提取命令参数列表（如：['-y', '@modelcontextprotocol/server-filesystem', '/path/to/project']）
        
        # 步骤2.3: 创建MCP客户端实例
        # 使用解析出的命令和参数初始化客户端对象
        mcp_client: try_mcp_client.MCPClient = try_mcp_client.MCPClient(
            mcp_name,
            command,
            args,
            # name=mcp_name,    # 设置客户端名称
            # command=command,  # 设置服务器启动命令
            # args=args,        # 设置命令参数
        )
        
        # 步骤2.4: 初始化客户端连接
        # 异步连接到MCP服务器，建立通信会话并获取可用工具列表
        await mcp_client.init()
        
        # 步骤2.5: 获取服务器提供的工具列表
        # 从已连接的服务器获取所有可用的工具（函数/方法）
        tools: List[Tool] = mcp_client.get_tools()
        
        # 步骤2.6: 显示获取到的工具信息
        # 打印工具列表以便查看服务器提供的功能
        rprint(tools)
        
        # 步骤2.7: 清理资源并关闭连接
        # 异步关闭与服务器的连接，释放相关资源
        await mcp_client.close()


if __name__ == "__main__":
    asyncio.run(example())
