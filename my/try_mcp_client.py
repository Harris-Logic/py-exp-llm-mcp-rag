# from ast import arg
# from asyncio.windows_events import NULL
import contextlib
import utils
import typing
# from click import command
import mcp.client
import mcp.client.session
import mcp.client.stdio
import rich
import mcp

import utils.pretty

class MCPClient:
    def __init__(
            self,
            client_name: str,
            command: str,
            args: typing.List[str],
            version: str = "1.0.0",
    ) -> None:
        self.mcp_session: mcp.client.session.ClientSession | None
        self.exit_stack: contextlib.AsyncExitStack = contextlib.AsyncExitStack()

        self.client_name: str = client_name
        self.version: str = version
        self.command: str = command
        self.args: typing.List[str] = args

        self.tools: typing.List[mcp.types.Tool] = []

    async def close(self) -> None:
        await self.exit_stack.aclose()
        utils.pretty.log_title("🔌 MCP client connection closed")
        # 关闭异步上下文管理

    async def init(self) -> None:
        await self.connect_to_server()

    async def connect_to_server(self) -> None:
        try:
            server_param: mcp.client.stdio.StdioServerParameters = mcp.client.stdio.StdioServerParameters(
                # self,
                command=self.command,
                args=self.args,
                env=None,
            )

            stdio_transport: typing.Tuple[any, any] = await self.exit_stack.enter_async_context(
                mcp.client.stdio.stdio_client(server_param)
            )
            self.stdio, self.write = stdio_transport

            self.mcp_session = await self.exit_stack.enter_async_context(
                mcp.client.session.ClientSession(self.stdio, self.write)
            )

            # self.init
            await self.mcp_session.initialize()
            
            server_response: mcp.types.ListToolsResult = await self.mcp_session.list_tools()
            self.tools = server_response.tools

            utils.pretty.log_title(f"\n✅ Connected to MCP server with tool:", [tool.name for tool in self.tools]) #rich.print

        except Exception as error:
            rich.print(f"❌ Failed to connect to MCP server:{error}")
            raise ConnectionError(f"Failed to connect to MCP server:{error}") from error
        
    async def call_tools(
            self,
            tool_name: str,
            params: dict[str, typing.Any],
    ): #-> typing.Dict[str, any]:
        if self.mcp_session is None:
            raise ValueError("MCP session is not initialized")
        try:
            return await self.mcp_session.call_tool(tool_name, params)
            # tool_call_result: dict[str, typing.Any] = await self.mcp_session.call_tool(tool_name, params)
            # return tool_call_result
        except Exception as error:
            raise ValueError(f"Tool call failed for {tool_name}, {error}") from error
        
    def get_tools(self) -> typing.List[mcp.types.Tool]:
        return self.tools
