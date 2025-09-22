"""
modified from https://modelcontextprotocol.io/quickstart/client  in tab 'python'
MCP客户端实现，基于Model Context Protocol官方示例修改
"""

import asyncio
from typing import Any, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client

from rich import print as rprint

from dotenv import load_dotenv

# from utils 
from augmented.mcp_tools import PresetMcpTools
from .utils.info import PROJECT_ROOT_DIR
from augmented.utils.pretty import RICH_CONSOLE

# 加载环境变量
load_dotenv()


# MCP客户端类，用于连接和管理MCP服务器
class MCPClient:
    """MCP客户端，负责与MCP服务器建立连接、管理工具调用和资源清理"""
    
    def __init__(
        self,
        name: str,
        command: str,
        args: list[str],
        version: str = "0.0.1",
    ) -> None:
        """初始化MCP客户端
        
        Args:
            name: 客户端名称标识
            command: MCP服务器启动命令
            args: 命令参数列表
            version: 客户端版本号
        """
        self.session: Optional[ClientSession] = None  # MCP会话对象
        self.exit_stack = AsyncExitStack()  # 异步上下文管理器栈，用于资源清理
        self.name = name  # 客户端名称
        self.version = version  # 客户端版本
        self.command = command  # 服务器启动命令
        self.args = args  # 命令参数列表
        self.tools: list[Tool] = []  # 从服务器获取的工具列表

    # 初始化客户端连接
    async def init(self) -> None:
        """初始化客户端，连接到MCP服务器"""
        await self._connect_to_server()

    # 清理客户端资源
    async def cleanup(self) -> None:
        """清理客户端资源，关闭与服务器的连接"""
        try:
            await self.exit_stack.aclose()  # 关闭所有异步上下文
        except Exception:
            rprint("Error during MCP client cleanup, traceback and continue!")
            RICH_CONSOLE.print_exception()  # 打印异常信息但继续执行

    # 获取工具列表
    def get_tools(self) -> list[Tool]:
        """返回从服务器获取的可用工具列表"""
        return self.tools

    # 连接到MCP服务器
    async def _connect_to_server(
        self,
    ) -> None:
        """连接到MCP服务器，建立会话并获取可用工具"""
        # 配置服务器参数
        server_params = StdioServerParameters(
            command=self.command,  # 服务器启动命令
            args=self.args,  # 命令参数
        )

        # 创建标准输入输出传输通道
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params),  # 创建stdio客户端
        )
        self.stdio, self.write = stdio_transport  # 获取读写接口
        
        # 创建客户端会话
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)  # 创建会话对象
        )

        # 初始化会话
        await self.session.initialize()

        # 获取服务器提供的工具列表
        response = await self.session.list_tools()
        self.tools = response.tools  # 存储工具列表
        # 打印连接成功信息和可用工具
        rprint("\nConnected to server with tools:", [tool.name for tool in self.tools])

    # 调用工具方法
    async def call_tool(
            self, 
            name: str,
            params: dict[str, Any]
    ):
        """调用MCP服务器上的特定工具
        
        Args:
            name: 工具名称
            params: 工具参数字典
            
        Returns:
            工具调用结果
        """
        return await self.session.call_tool(name, params)  # 调用服务器工具


# 示例函数，演示MCP客户端的使用
async def example() -> None:
    """MCP客户端使用示例，演示如何连接和使用不同的MCP工具"""
    # 遍历预设的MCP工具配置
    for mcp_tool in [
        PresetMcpTools.filesystem.append_mcp_params(f" {PROJECT_ROOT_DIR!s}"),  # 文件系统工具，配置项目根目录
        PresetMcpTools.fetch,  # 网络抓取工具
    ]:
        rprint(mcp_tool.shell_cmd)  # 打印工具的命令行（用于调试）
        # 创建MCP客户端实例
        mcp_client = MCPClient(**mcp_tool.to_common_params())
        await mcp_client.init()  # 初始化客户端连接
        tools = mcp_client.get_tools()  # 获取可用工具列表
        rprint(tools)  # 打印工具信息
        await mcp_client.cleanup()  # 清理客户端资源


# 程序主入口
if __name__ == "__main__":
    """程序主入口点，运行MCP客户端示例"""
    asyncio.run(example())  # 运行异步示例函数
