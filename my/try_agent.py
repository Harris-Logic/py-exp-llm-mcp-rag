

import typing
# from my import mcp_client
# from my.mcp_client import MCPClient
import utils.pretty


class Agent:
    mcp_clients: typing.List[mcp_client.MCPClient]

    async def init(self):
        utils.pretty.log_title("Tools")
        # 这里需要根据实际的MCP客户端初始化逻辑进行修改
        # 假设我们有一个MCP客户端实例需要初始化
        for mcp_client in self.mcp_clients:
            await mcp_client.init()
        


    async def cleanup(self):
        pass
        
    async def invoke(self):
        return await self._invoke()

    async def _invoke(self):
        pass
