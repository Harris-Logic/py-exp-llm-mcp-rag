#!/usr/bin/env python3
"""
测试 tool_calls 问题的脚本
"""

import asyncio
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from try_chat_openai import AsyncChatOpenAI

async def test_tool_calls():
    """测试 tool_calls 功能"""
    
    # 创建一个简单的聊天实例
    chat = AsyncChatOpenAI(
        model="deepseek-chat",
        system_prompt="你是一个有帮助的助手"
    )
    
    try:
        # 发送一个简单的消息
        print("发送测试消息...")
        response = await chat.chat(prompt="你好")
        print(f"响应内容: {response.content}")
        print(f"工具调用: {response.toolCalls}")
        
    except Exception as e:
        print(f"错误发生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tool_calls())
