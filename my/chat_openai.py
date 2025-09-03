import asyncio
import os
from mcp import Tool
from openai import AsyncOpenAI
from dataclasses import dataclass, field

from openai.types import FunctionDefinition
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
import dotenv
from pydantic import BaseModel
from rich import print as rprint

from utils import pretty

dotenv.load_dotenv()  # 读取.env里的API等信息


class ToolCallFunction(BaseModel):
    name: str = ""
    arguments: str = ""# 函数参数（JSON 字符串格式）
# 功能: 表示工具调用中的函数信息
# 作用: 封装工具调用时函数的具体信息，用于结构化存储函数名称和参数

class ToolCall(BaseModel):# 功能: 表示完整的工具调用信息
    id: str = ""
    function: ToolCallFunction = ToolCallFunction()
# 作用: 封装完整的工具调用数据，包括调用ID和具体的函数信息

class ChatOpenAIChatResponse(BaseModel): # 功能: 表示聊天API的响应结构
    content: str = ""
    tool_calls: list[ToolCall] = []
# 作用: 标准化聊天响应的数据结构，包含文本内容和可能的工具调用


@dataclass
class AsyncChatOpenAI: # 功能: 主要的异步OpenAI聊天客户端类
    model: str
    messages: list[ChatCompletionMessageParam] = field(default_factory=list) #消息历史列表
    tools: list[Tool] = field(default_factory=list) # MCP工具列表

    system_prompt: str = ""
    context: str = "" #上下文信息

    llm: AsyncOpenAI = field(init=False) #OpenAI客户端实例（自动初始化）

    def __post_init__(self): # 功能: 初始化后自动执行的方法
        self.llm = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL"),
        )
        if self.system_prompt:
            self.messages.insert(0, {"role": "system", "content": self.system_prompt})
        if self.context:
            self.messages.append({"role": "user", "content": self.context})
# 作用: 设置OpenAI客户端并处理系统提示词和上下文信息

    async def chat(self, prompt: str = "", print_llm_output: bool = True): # 功能: 主要的聊天方法
        pretty.log_title("CHAT")
        if prompt:
            self.messages.append({"role": "user", "content": prompt})
# 作用: 处理用户输入并与OpenAI API进行异步聊天交互，支持流式响应和工具调用

        # 只有在有工具的情况下才传递 tools 参数
        create_kwargs = {
            "model": self.model,
            "messages": self.messages,
            "stream": True
        }
        
        tools_definition = self.getToolsDefinition()
        if tools_definition:  # 只有在有工具的情况下才添加 tools 参数
            create_kwargs["tools"] = tools_definition
            
        streaming = await self.llm.chat.completions.create(**create_kwargs)
        pretty.log_title("RESPONSE")
        content = ""
        tool_calls: list[ToolCall] = []
        printed_llm_output = False
        async for chunk in streaming:
            delta = chunk.choices[0].delta
            # 处理 content
            if delta.content:
                content += delta.content or ""
                if print_llm_output:
                    print(delta.content, end="")
                    printed_llm_output = True
            # 处理 tool_calls
            if delta.tool_calls:
                for tool_call_chunk in delta.tool_calls:
                    # 第一次收到一个tool_call, 因为流式传输所以我们先设置一个占位值
                    if len(tool_call_chunk) <= tool_call_chunk.index:
                        tool_calls.append(ToolCall())
                    current_call = tool_calls[tool_call_chunk.index]
                    if tool_call_chunk.id:
                        current_call.id = tool_call_chunk.id or ""
                    if tool_call_chunk.function:
                        current_call.function.name = tool_call_chunk.function.name or ""
                        current_call.function.arguments = (
                            tool_call_chunk.function.arguments or ""
                        )
        if printed_llm_output:
            print()
        self.messages.append(
            {
                "role": "assistant",
                "content": content,
                "tool_calls": [
                    {
                        "type": "function",
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in tool_calls
                ],
            }
        )
        return ChatOpenAIChatResponse(
            content=content,
            tool_calls=tool_calls,
        )

    def getToolsDefinition(self) -> list[ChatCompletionToolParam]: # 功能: 获取工具定义
        return [
            ChatCompletionToolParam(
                type="function",
                function=FunctionDefinition(
                    name=t.name,
                    description=t.description,
                    parameters=t.inputSchema,
                ),
            )
            for t in self.tools
        ]
# 作用: 将MCP工具转换为OpenAI API所需的函数定义格式


async def example(): # 功能: 示例演示函数
    llm = AsyncChatOpenAI(
        model="deepseek-coder",
    )
    chat_resp = await llm.chat(prompt="Hello")
    rprint(chat_resp)
# 作用: 展示如何使用AsyncChatOpenAI类进行基本的聊天交互


if __name__ == "__main__": # 功能: 程序入口点
    asyncio.run(example())
# 作用: 当文件直接运行时执行示例函数
