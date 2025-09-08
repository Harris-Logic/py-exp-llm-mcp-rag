

from ast import arguments
from mcp import Tool
import mcp
from openai import AsyncOpenAI, OpenAI
# import openai.types

import openai.types.chat.completions
from pydantic import BaseModel
# from my.chat_openai import ToolCall
# from augmented.chat_openai import ToolCallFunction
# from augmented.chat_openai import ToolCallFunction
import utils
import utils.pretty
import rich
import dataclasses

class ToolCallFunction(BaseModel):
    name: str
    arguments: str
class ToolCall(BaseModel):
    id: str
    function: ToolCallFunction=ToolCallFunction()

class ChatOpenAIChatResponse(BaseModel):
    content: str = ""
    toolCalls: list[ToolCall] = []

import openai.types.chat
@dataclasses.dataclass
class AsyncChatOpenAI:
    model: str
    messages: list[openai.types.chat.ChatCompletionMessageParam]=dataclasses.field(default_factory=list)
    tools: list[mcp.Tool]=dataclasses.field(default_factory=list)

    llm: AsyncOpenAI=dataclasses.field(init=False)

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
        utils.pretty.log_title("CHAT")
        if prompt:
            self.messages.append({"role":"user", "content":prompt})

        content = ""
        tool_calls: list[ToolCall] = []
        print_llm_output = False
        param_tools = self.get_tool_definition()

    def get_tool_definition():
        pass

    def append_tool_result(self, tool_call_id: str, tool_output: str):
        self.messages.append(
            {
                "role": "Tool",
                "content": tool_output,
                tool_call_id: tool_call_id, 
            }
        )




# class ChatOpenAI:
#     messages: openai.types.chat.ChatCompletionMessage

    
