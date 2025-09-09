# #!/usr/bin/env python3
# """
# MCP客户端测试脚本
# 用于测试MCPClient类的连接功能
# """

# import asyncio
# import sys
# from pathlib import Path

# # 添加当前目录到Python路径，以便导入my模块
# sys.path.insert(0, str(Path(__file__).parent))

# from my.mcp_client import MCPClient
# from utils import pretty

# async def test_mcp_client():
#     """测试MCP客户端连接功能"""
    
#     # 创建一个示例MCP客户端
#     # 注意：这里需要替换为实际的MCP服务器路径
#     client = MCPClient(
#         name="TestClient",
#         command="python",  # 或者 "node" 对于JavaScript服务器
#         args=["path/to/your/server.py"]  # 替换为实际的服务器脚本路径
#     )
    
#     try:
#         pretty.log_title("Testing MCP Client Connection", "TEST")
        
#         # 初始化并连接到服务器
#         print("🔄 Connecting to MCP server...")
#         await client.init()
        
#         # 获取工具列表
#         tools = client.get_tools()
#         print(f"📋 Available tools: {[tool.name for tool in tools]}")
        
#         # 显示工具详情
#         if tools:
#             print("\n🔧 Tool details:")
#             for tool in tools:
#                 print(f"  • {tool.name}: {tool.description}")
#                 if hasattr(tool, 'inputSchema'):
#                     print(f"    Input schema: {tool.inputSchema}")
        
#         print("\n✅ MCP client test completed successfully!")
        
#     except Exception as e:
#         print(f"❌ Test failed: {e}")
#         import traceback
#         traceback.print_exc()
    
#     finally:
#         # 清理资源
#         await client.close()

# if __name__ == "__main__":
#     # 运行测试
#     asyncio.run(test_mcp_client())
