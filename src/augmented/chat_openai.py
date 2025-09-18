import asyncio
import os
from mcp import Tool
import mcp
from openai import NOT_GIVEN, AsyncOpenAI
from dataclasses import dataclass, field

from openai.types import FunctionDefinition
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
import dotenv
from pydantic import BaseModel
from rich import print as rprint

from augmented.utils import pretty
from augmented.utils.info import DEFAULT_MODEL_NAME

# 日志记录器，用于格式化输出聊天相关的日志信息
PRETTY_LOGGER = pretty.ALogger("[ChatOpenAI]")

# 加载环境变量文件
dotenv.load_dotenv()


# 工具调用函数的模型定义，包含函数名称和参数字符串
class ToolCallFunction(BaseModel):
    """表示工具调用中的函数信息"""
    name: str = ""  # 函数名称
    arguments: str = ""  # 函数参数字符串（JSON格式）


# 工具调用的模型定义，包含调用ID和函数信息
class ToolCall(BaseModel):
    """表示一个完整的工具调用请求"""
    id: str = ""  # 工具调用的唯一标识符
    function: ToolCallFunction = ToolCallFunction()  # 函数调用信息


# OpenAI聊天响应的模型定义，包含内容文本和工具调用列表
class ChatOpenAIChatResponse(BaseModel):
    """表示OpenAI聊天API的响应结果"""
    content: str = ""  # AI生成的文本内容
    tool_calls: list[ToolCall] = []  # 需要调用的工具列表


# 异步OpenAI聊天客户端类，用于与OpenAI API进行交互
@dataclass
class AsyncChatOpenAI:
    """异步OpenAI聊天客户端，支持工具调用和流式响应"""
    
    model: str  # 使用的AI模型名称
    messages: list[ChatCompletionMessageParam] = field(default_factory=list)  # 聊天消息历史
    tools: list[mcp.Tool] = field(default_factory=list)  # 可用的工具列表

    system_prompt: str = ""  # 系统提示词
    context: str = ""  # 上下文信息

    llm: AsyncOpenAI = field(init=False)  # OpenAI客户端实例

    # 初始化后处理，设置OpenAI客户端并添加系统提示和上下文
    def __post_init__(self) -> None:
        """初始化OpenAI客户端并设置初始消息"""
        # 创建OpenAI异步客户端实例
        self.llm = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # 从环境变量获取API密钥
            base_url=os.environ.get("OPENAI_BASE_URL"),  # 从环境变量获取API基础URL
        )
        # 如果有系统提示，插入到消息列表开头
        if self.system_prompt:
            self.messages.insert(0, {"role": "system", "content": self.system_prompt})
        # 如果有上下文信息，添加到消息列表
        if self.context:
            self.messages.append({"role": "user", "content": self.context})

    # 主要的聊天方法，处理用户提示并返回响应
    async def chat(
        self, prompt: str = "", print_llm_output: bool = True
    ) -> ChatOpenAIChatResponse:
        """主聊天方法，处理用户输入并返回AI响应"""
        try:
            # 调用内部聊天实现
            return await self._chat(prompt, print_llm_output)
        except Exception as e:
            # 打印错误信息并重新抛出异常
            rprint(f"Error during chat: {e!s}")
            raise

    # 内部聊天实现，处理与OpenAI API的实际交互
    async def _chat(
        self, prompt: str = "", print_llm_output: bool = True
    ) -> ChatOpenAIChatResponse:
        """内部聊天实现，处理流式响应和工具调用"""
        # 记录聊天开始
        PRETTY_LOGGER.title("CHAT")
        
        # 如果有用户提示，添加到消息历史
        if prompt:
            self.messages.append({"role": "user", "content": prompt})

        content = ""  # 存储AI生成的文本内容
        tool_calls: list[ToolCall] = []  # 存储工具调用信息
        printed_llm_output = False  # 标记是否已经打印了输出
        
        # 获取工具定义，如果没有工具则使用NOT_GIVEN
        param_tools = self.get_tools_definition() or NOT_GIVEN
        
        # 创建流式聊天完成请求
        async with await self.llm.chat.completions.create(
            model=self.model,  # 指定模型
            messages=self.messages,  # 消息历史
            tools=param_tools,  # 可用工具
            stream=True,  # 启用流式响应
        ) as stream:
            # 记录响应开始
            PRETTY_LOGGER.title("RESPONSE")
            
            # 处理流式响应块
            async for chunk in stream:
                delta = chunk.choices[0].delta
                
                # 处理文本内容
                if delta.content:
                    content += delta.content or ""
                    # 如果需要打印输出，实时显示内容
                    if print_llm_output:
                        print(delta.content, end="")
                        printed_llm_output = True
                
                # 处理工具调用
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        # 确保工具调用列表足够长
                        if len(tool_calls) <= tool_call.index:
                            tool_calls.append(ToolCall())
                        
                        this_tool_call = tool_calls[tool_call.index]
                        
                        # 处理工具调用ID
                        if tool_call.id:
                            this_tool_call.id += tool_call.id or ""
                        
                        # 处理函数信息
                        if tool_call.function:
                            # 处理函数名称
                            if tool_call.function.name:
                                this_tool_call.function.name += (
                                    tool_call.function.name or ""
                                )
                            # 处理函数参数
                            if tool_call.function.arguments:
                                this_tool_call.function.arguments += (
                                    tool_call.function.arguments or ""
                                )
        
        # 如果打印了输出，添加换行符
        if printed_llm_output:
            print()
        
        # 将AI响应添加到消息历史中
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
        
        # 返回聊天响应对象
        return ChatOpenAIChatResponse(
            content=content,
            tool_calls=tool_calls,
        )

    # 获取工具定义，将MCP工具转换为OpenAI API所需的格式
    def get_tools_definition(self) -> list[ChatCompletionToolParam]:
        """将MCP工具转换为OpenAI API兼容的工具定义格式"""
        return [
            ChatCompletionToolParam(
                type="function",  # 工具类型为函数
                function=FunctionDefinition(
                    name=t.name,  # 工具名称
                    description=t.description,  # 工具描述
                    parameters=t.inputSchema,  # 工具输入参数模式
                ),
            )
            for t in self.tools  # 遍历所有可用工具
        ]

    # 添加工具执行结果到消息历史中
    def append_tool_result(self, tool_call_id: str, tool_output: str) -> None:
        """将工具执行结果添加到聊天历史中"""
        self.messages.append(
            {
                "role": "tool",  # 消息角色为工具
                "tool_call_id": tool_call_id,  # 对应的工具调用ID
                "content": tool_output,  # 工具执行结果
            }
        )


# 示例函数，展示如何使用AsyncChatOpenAI类
async def example() -> None:
    """示例函数，演示AsyncChatOpenAI的基本用法"""
    # 创建聊天客户端实例
    llm = AsyncChatOpenAI(
        model=DEFAULT_MODEL_NAME,  # 使用默认模型
    )
    # 发送聊天请求
    chat_resp = await llm.chat(prompt="Hello")
    # 打印响应结果
    rprint(chat_resp)


if __name__ == "__main__":
    # 运行示例函数
    asyncio.run(example())
