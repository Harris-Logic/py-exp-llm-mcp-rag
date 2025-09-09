import asyncio
from typing import List
from try_mcp_client import MCPClient
from try_agent import Agent

URL = 'https://github.com/unjs/consola'
TASK = f"""
Please help me summarize the content of this website.
URL: {URL}
"""

async def main():
    # 创建MCP客户端实例
    fetch_mcp = MCPClient("mcp-server-fetch", "uvx", ['mcp-server-fetch'])
    
    # 创建Agent实例
    agent = Agent([fetch_mcp], 'deepseek-chat', 'You are a helpful assistant.')
    
    # 初始化Agent
    await agent.init()
    
    # 执行任务
    await agent.invoke(TASK)
    
    # 关闭Agent
    await agent.close()

if __name__ == "__main__":
    asyncio.run(main())
