# 导入必要的库和模块
import asyncio  # 异步编程支持
from dataclasses import dataclass  # 用于创建数据类
import json  # JSON数据处理

from rich import print as rprint  # 美化输出打印

# 导入自定义模块
from augmented.chat_openai import AsyncChatOpenAI  # 异步OpenAI聊天客户端
from augmented.mcp_client import MCPClient  # MCP客户端
from augmented.mcp_tools import PresetMcpTools  # 预设MCP工具
from augmented.utils import pretty  # 美化工具
from augmented.utils.info import DEFAULT_MODEL_NAME, PROJECT_ROOT_DIR  # 默认配置

# 创建日志记录器，用于Agent相关的日志输出
PRETTY_LOGGER = pretty.ALogger("[Agent]")


# Agent类，负责协调LLM和MCP工具的执行
@dataclass
class Agent:
    """AI代理类，协调语言模型和工具调用的执行"""
    
    mcp_clients: list[MCPClient]  # MCP客户端列表，提供各种工具功能
    model: str  # 使用的AI模型名称
    llm: AsyncChatOpenAI | None = None  # 语言模型实例，初始为None
    system_prompt: str = ""  # 系统提示词
    context: str = ""  # 上下文信息

    # 初始化Agent，设置LLM和工具
    async def init(self) -> None:
        """初始化Agent，设置语言模型和可用工具"""
        PRETTY_LOGGER.title("INIT LLM&TOOLS")  # 记录初始化开始
        tools = []  # 初始化工具列表
        
        # 遍历所有MCP客户端并初始化
        for mcp_client in self.mcp_clients:
            await mcp_client.init()  # 异步初始化MCP客户端
            tools.extend(mcp_client.get_tools())  # 获取客户端提供的工具并添加到列表
        
        # 创建异步聊天LLM实例，配置模型、工具、系统提示和上下文
        self.llm = AsyncChatOpenAI(
            self.model,  # 模型名称
            tools=tools,  # 可用工具列表
            system_prompt=self.system_prompt,  # 系统提示词
            context=self.context,  # 上下文信息
        )

    # 清理Agent资源，关闭MCP客户端连接
    async def cleanup(self) -> None:
        """清理Agent资源，关闭所有MCP客户端连接"""
        PRETTY_LOGGER.title("CLEANUP LLM&TOOLS")  # 记录清理开始

        # 循环处理所有MCP客户端，确保正确清理
        while self.mcp_clients:
            # NOTE: 需要先处理其他依赖于mcp_client的资源, 不然会有一堆错误, 如
            # RuntimeError: Attempted to exit cancel scope in a different task than it was entered in
            # RuntimeError: Attempted to exit a cancel scope that isn't the current tasks's current cancel scope an error occurred during closing of asynchronous generator <async_generator object stdio_client at 0x76c3e08ee0c0>
            mcp_client = self.mcp_clients.pop()  # 从列表中移除并获取最后一个客户端
            await mcp_client.cleanup()  # 异步清理MCP客户端资源

    # 公开的调用方法，转发到内部实现
    async def invoke(self, prompt: str) -> str | None:
        """公开调用方法，处理用户输入并返回响应"""
        return await self._invoke(prompt)

    # 核心调用逻辑：处理用户输入，执行工具调用循环
    async def _invoke(self, prompt: str) -> str | None:
        """核心调用逻辑：处理用户输入，执行工具调用循环"""
        if self.llm is None:
            raise ValueError("llm not call .init()")  # 检查LLM是否已初始化
        
        # 发送初始消息给LLM
        chat_resp = await self.llm.chat(prompt)
        i = 0  # 循环计数器
        
        # 工具调用循环：处理LLM可能返回的工具调用请求
        while True:
            PRETTY_LOGGER.title(f"INVOKE CYCLE {i}")  # 记录当前循环次数
            i += 1
            # 处理工具调用
            rprint(chat_resp)  # 打印LLM响应
            
            # 检查是否有工具调用请求
            if chat_resp.tool_calls:
                # 遍历所有工具调用请求
                for tool_call in chat_resp.tool_calls:
                    target_mcp_client: MCPClient | None = None
                    
                    # 查找对应的MCP客户端来处理这个工具调用
                    for mcp_client in self.mcp_clients:
                        if tool_call.function.name in [
                            t.name for t in mcp_client.get_tools()
                        ]:
                            target_mcp_client = mcp_client
                            break
                    
                    # 如果找到对应的客户端，执行工具调用
                    if target_mcp_client:
                        PRETTY_LOGGER.title(f"TOOL USE `{tool_call.function.name}`")
                        rprint("with args:", tool_call.function.arguments)
                        
                        # 调用工具并获取结果
                        mcp_result = await target_mcp_client.call_tool(
                            tool_call.function.name,
                            json.loads(tool_call.function.arguments),  # 解析JSON参数
                        )
                        rprint("call result:", mcp_result)
                        
                        # 将工具调用结果添加到LLM上下文中
                        self.llm.append_tool_result(
                            tool_call.id, mcp_result.model_dump_json()
                        )
                    else:
                        # 工具未找到，返回错误信息
                        self.llm.append_tool_result(tool_call.id, "tool not found")
                
                # 继续对话，让LLM处理工具调用结果
                chat_resp = await self.llm.chat()
            else:
                # 没有工具调用，返回最终响应内容
                return chat_resp.content


# Agent使用示例：演示如何配置和使用Agent进行网页爬取和内容保存
async def example() -> None:
    """示例函数，演示Agent的基本用法和配置"""
    enabled_mcp_clients = []  # 启用的MCP客户端列表
    agent = None  # Agent实例
    
    try:
        # 配置要使用的MCP工具
        for mcp_tool in [
            PresetMcpTools.filesystem.append_mcp_params(f" {PROJECT_ROOT_DIR!s}"),  # 文件系统工具，配置项目根目录
            PresetMcpTools.fetch,  # 网络抓取工具
        ]:
            rprint(mcp_tool.shell_cmd)  # 打印MCP工具的shell命令（用于调试）
            mcp_client = MCPClient(**mcp_tool.to_common_params())  # 创建MCP客户端实例
            enabled_mcp_clients.append(mcp_client)  # 添加到启用列表

        # 创建Agent实例
        agent = Agent(
            model=DEFAULT_MODEL_NAME,  # 使用默认模型
            mcp_clients=enabled_mcp_clients,  # 配置MCP客户端
        )
        await agent.init()  # 初始化Agent

        # 调用Agent执行任务：爬取Hacker News内容并保存到文件
        resp = await agent.invoke(
            f"爬取 https://news.ycombinator.com 的内容, 并且总结后保存在 {PROJECT_ROOT_DIR / 'output' / 'step3-agent-with-mcp'!s} 目录下的news.md文件中"
        )
        rprint(resp)  # 打印最终响应
    
    except Exception as e:
        # 异常处理：打印错误信息并重新抛出
        rprint(f"Error during agent execution: {e!s}")
        raise
    
    finally:
        # 确保资源清理：无论是否发生异常都执行清理
        if agent:
            await agent.cleanup()


# 程序主入口：运行示例函数
if __name__ == "__main__":
    """程序主入口点，运行Agent示例"""
    asyncio.run(example())  # 运行异步示例函数
