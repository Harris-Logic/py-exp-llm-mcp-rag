#!/usr/bin/env python3
"""
测试包含工具的 tool_calls 功能
"""

import asyncio
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from mcp import Tool
from try_chat_openai import AsyncChatOpenAI

async def test_with_tools():
    """测试包含工具的情况"""
    
    # 创建一个简单的工具
    weather_tool = Tool(
        name="get_weather",
        description="获取指定城市的天气信息",
        inputSchema={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    )
    
    # 创建一个包含工具的聊天实例
    chat = AsyncChatOpenAI(
        model="deepseek-chat",
        system_prompt="你是一个有帮助的助手，可以使用工具来获取信息",
        tools=[weather_tool]
    )
    
    try:
        # 发送一个可能触发工具调用的消息
        print("发送测试消息（可能触发工具调用）...")
        response = await chat.chat(prompt="请问北京的天气怎么样？")
        print(f"响应内容: {response.content}")
        print(f"工具调用数量: {len(response.toolCalls)}")
        
        for i, tool_call in enumerate(response.toolCalls):
            print(f"工具调用 {i+1}:")
            print(f"  ID: {tool_call.id}")
            print(f"  名称: {tool_call.function.name}")
            print(f"  参数: {tool_call.function.arguments}")
        
    except Exception as e:
        print(f"错误发生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_tools())
