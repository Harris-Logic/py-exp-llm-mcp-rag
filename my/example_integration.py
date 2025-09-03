#!/usr/bin/env python3
"""
MCP客户端与OpenAI集成示例
展示如何将MCP工具与OpenAI聊天功能结合使用
"""

import asyncio
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from mcp_client import MCPClient
from chat_openai import AsyncChatOpenAI, ChatOpenAIChatResponse
from utils import pretty

class MCPOpenAIIntegration:
    """MCP客户端与OpenAI的集成类"""
    
    def __init__(self, mcp_client: MCPClient, model: str = "gpt-3.5-turbo"):
        """
        初始化集成类
        
        Args:
            mcp_client: 已连接的MCP客户端实例
            model: OpenAI模型名称
        """
        self.mcp_client = mcp_client
        self.model = model
        
        # 创建OpenAI聊天客户端
        self.chat_client = AsyncChatOpenAI(
            model=model,
            tools=mcp_client.get_tools()  # 使用MCP工具
        )
    
    async def process_query(self, query: str) -> str:
        """处理查询，使用MCP工具和OpenAI"""
        
        pretty.log_title("Processing Query", "QUERY")
        print(f"💬 User: {query}")
        
        # 使用OpenAI处理查询
        response = await self.chat_client.chat(prompt=query)
        
        # 处理工具调用
        if response.tool_calls:
            pretty.log_title("Tool Calls Detected", "TOOLS")
            
            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                tool_args = eval(tool_call.function.arguments)  # 将字符串参数转换为字典
                
                print(f"🛠️  Calling tool: {tool_name}")
                print(f"   Arguments: {tool_args}")
                
                try:
                    # 调用MCP工具
                    tool_result = await self.mcp_client.call_tool(tool_name, tool_args)
                    print(f"✅ Tool result: {tool_result}")
                    
                    # 将工具结果添加到对话上下文
                    # 这里可以进一步处理工具结果并继续对话
                    
                except Exception as e:
                    print(f"❌ Tool call failed: {e}")
        
        return response.content

async def main():
    """主函数：演示MCP与OpenAI的集成"""
    
    # 创建MCP客户端（需要替换为实际的服务器路径）
    mcp_client = MCPClient(
        name="ExampleMCPClient",
        command="python",  # 或 "node"
        args=["path/to/your/mcp/server.py"]  # 替换为实际路径
    )
    
    try:
        # 连接到MCP服务器
        print("🔗 Connecting to MCP server...")
        await mcp_client.init()
        
        # 创建集成实例
        integration = MCPOpenAIIntegration(mcp_client)
        
        # 示例查询
        queries = [
            "你好，请介绍一下你自己",
            "你能使用哪些工具？",
            # 添加更多测试查询
        ]
        
        for query in queries:
            result = await integration.process_query(query)
            print(f"\n🤖 Assistant: {result}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 清理资源
        await mcp_client.close()
        print("👋 Integration demo completed")

if __name__ == "__main__":
    asyncio.run(main())
