from http import client, server
import json
from os import error
from urllib import response

from attr import dataclass
from mcp import ServerResult
from networkx import rescale_layout
import rich
from augmented import mcp_client
import try_mcp_client
from try_mcp_client import MCPClient
import typing
# from my import mcp_client
# from my.mcp_client import MCPClient
import try_chat_openai
import utils.pretty

@dataclass
class Agent:
    mcp_clients: list[try_mcp_client.MCPClient]
    llm:try_chat_openai.AsyncChatOpenAI | None = None
    model_name: str
    system_prompt: str

    async def init(self):
        utils.pretty.log_title("Tools")
        
        for mcp_client in self.mcp_clients:
            await mcp_client.init()

        # tools.extend(mcp_client.get_tools())
        tools = [tool for mcp_client in self.mcp_clients for tool in mcp_client.get_tools()]

        self.llm = try_chat_openai.ChatOpenAI(
            self.model_name, 
            self.system_prompt, 
            tools
        )

    async def cleanup(self):
        utils.pretty.log_title("CLEANUP LLM&TOOLS")
        for mcp_client in self.mcp_clients:
            await mcp_client.close()
        
    async def invoke(self, prompt: str):
        return await self._invoke(prompt)

    async def _invoke(self, prompt: str):
        if self.llm is None:
            raise ValueError("llm not call .init()")
        
        server_response = await self.llm.chat(prompt)
        
        while True:
            if server_response.toolCalls is not None:
                for tool_call in server_response.toolCalls:
                    # mcp = self.mcp_clients.
                    mcp = next(
                        (mcp_client for mcp_client in self.mcp_clients
                         if any(tool.name == tool_call.function.name for tool in mcp_client.get_tools())),
                        None,
                    )
                    target_mcp = mcp
                    # for mcp_client in self.mcp_clients:
                    #     if tool_call.function.name in [ # 工具的名
                    #         tool.name for tool in mcp_client.get_tools()
                    #     ]:
                    #         target_mcp = mcp_client
                    #         break
                    
                    if target_mcp is not None:
                        utils.pretty.log_title(f"TOOL USE `{tool_call.function.name}`")
                        rich.print("with args:", tool_call.function.arguments)

                        mcp_result = await target_mcp.call_tools(
                            tool_call.function.name,
                            json.load(tool_call.function.arguments),
                        )
                        # utils.pretty.log_title(f"result: `{json.}`")
                        rich.print("result: ", mcp_result)

                        self.llm.append_tool_result(
                            tool_call_id=tool_call.id, 
                            tool_output=mcp_result.model_dump_json(),
                        )
                    else:
                        self.llm.append_tool_result(
                            tool_call.id,
                            "Tool not found",
                        )
                server_response = await self.llm.chat()
                continue
            await self.cleanup()
            return server_response.cont


