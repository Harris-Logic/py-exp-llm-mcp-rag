
from ast import arguments
from ctypes import util
from json import tool

import logging
import os
import sys
from turtle import mode
from dotenv import load_dotenv
from mcp import Tool
import mcp
from openai import AsyncOpenAI, OpenAI, NOT_GIVEN
# import openai.types

import openai.types.chat.completions
# from openai.types.chat import ChatCompletion

# from my.chat_openai import ToolCall
# from augmented.chat_openai import ToolCallFunction
# from augmented.chat_openai import ToolCallFunction
import utils
from utils.pretty import log_title
import rich
from typing import Dict, Any
import dataclasses
from openai.types.shared_params.function_definition import FunctionDefinition

from openai.types.chat import (
        ChatCompletionMessageParam,
        ChatCompletionToolParam,
    )

from pydantic import BaseModel
from typing import Optional

class ToolCallFunction(BaseModel):
    name: str = ""
    arguments: str = ""
class ToolCall(BaseModel):
    id: str = ""
    function: ToolCallFunction=ToolCallFunction()

class ChatOpenAIChatResponse(BaseModel):
    content: str = ""
    toolCalls: list[ToolCall] = []

# class FunctionDefinition (BaseModel):
    # name: str
    # description: str
    # parameters: Dict[str, Any]
    
class ChatCompletionTool(BaseModel):
    type: str = "function"
    function: FunctionDefinition


from typing import Any,Dict, Optional, Union, List
import openai.types.chat
@dataclasses.dataclass
class AsyncChatOpenAI:
    model: str
    messages: list[ChatCompletionMessageParam]=dataclasses.field(default_factory=list)
    tools: list[mcp.Tool]=dataclasses.field(default_factory=list)
    
    async_llm: AsyncOpenAI=dataclasses.field(init=False)
    
    def __init__(self, model: str, system_prompt: str = '', tools: list[mcp.Tool] = [], context: str = '') :
        load_dotenv()

        self.async_llm = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL"),
            # api_key=os.getenv("OPENAI_API_KEY"),
            # base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.model = model
        # self.messages : List[Dict[str,Any]] = []
        # self.tools = tools or []
        self.messages: list[ChatCompletionMessageParam] = []
        self.tools: list[mcp.Tool] = tools or []

        if system_prompt:
            self.messages.append({ 'role':'system', 'content': system_prompt})
        
        if context:
            self.messages.append({ 'role':'user','content':context })

    async def chat(
            self, 
            prompt: str = "",
            print_llm_output: bool = True,
    ) -> ChatOpenAIChatResponse:
        try:
            return await self._chat(prompt, print_llm_output)
        except Exception as e:
            rich.print(f"Error during chat: {e!s}")
            raise
    
    async def _chat(
            self,
            prompt: str = "",
            print_llm_output: bool = True,
    ) -> ChatOpenAIChatResponse:
        log_title("CHAT")
        if prompt is not None:
            self.messages.append({"role":"user", "content":prompt})

        stream = await self.async_llm.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.get_tool_definition() or NOT_GIVEN,
            stream=True,
        )

        content = ""
        tool_calls: list[ToolCall] = []
        print_llm_output = False
        # param_tools = self.get_tool_definition()
        log_title("RESPONSE")

        async for chunk in stream:
            delta = chunk.choices[0].delta

            if delta.content:
                content_chunk = delta.content or ""
                content += content_chunk
                logging.info(f"", content_chunk)

            if delta.tool_calls:
                for tool_call_chunk in delta.tool_calls:
                    if len(tool_calls) <= tool_call_chunk.index:
                        tool_calls.append(ToolCall())
                        # tool_calls.append({
                        #     "id": str(tool_call_chunk.index),
                        #     "function": {"name":"","arguments": ""},
                        # })
                    
                    current_call = tool_calls[tool_call_chunk.index]
                    if tool_call_chunk.id:
                        current_call.id += tool_call_chunk.id
                    if tool_call_chunk.function and tool_call_chunk.function.name:
                        current_call.function.name += tool_call_chunk.function.name
                    if tool_call_chunk.function and tool_call_chunk.function.arguments:
                        current_call.function.arguments += tool_call_chunk.function.arguments
        # 构建助手消息，只有当有工具调用时才包含tool_calls字段
        assistant_message: Dict[str, Any] = {
            "role": "assistant",
            "content": content,
        }
        
        # 只有当有有效的工具调用时才添加tool_calls字段
        valid_tool_calls = [
            {
                "type": "function",
                "id": tc.id,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in tool_calls
            if tc.function.name  # 只包含有名称的tool calls
        ]
        
        if valid_tool_calls:
            assistant_message["tool_calls"] = valid_tool_calls
            
        self.messages.append(assistant_message)  # type: ignore

        # self.messages.append({
        #     "role": "assistant",
        #     "content": content,
        #     "tool_calls": [
        #         {
        #             "type": "function",
        #             "id": tc.id,
        #             "function": {
        #                 "name": tc.function.name,
        #                 "arguments": tc.function.arguments,
        #             },
        #         }
        #         for tc in tool_calls
        #     ],
        # })

        return ChatOpenAIChatResponse(
            content=content,
            toolCalls=tool_calls,
        )
    
    def get_tool_definition(self) -> List [ChatCompletionToolParam]:
        """
        获取工具定义 - 将工具列表转换为OpenAI API所需的格式
        
        Returns:
            格式化后的工具定义数组
        """
        return [
            ChatCompletionToolParam(
                type="function",
                function=FunctionDefinition(
                    name=tool.name,
                    description=tool.description or "",
                    parameters=tool.inputSchema,
                ),
            )
            for tool in self.tools
        ]

    def append_tool_result(self, tool_call_id: str, tool_output: str):
        self.messages.append(
            {
                "role": "tool",
                "content": tool_output,
                "tool_call_id": tool_call_id, 
            }
        )




# class ChatOpenAI:
#     messages: openai.types.chat.ChatCompletionMessage
