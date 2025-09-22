"""
augmented 包初始化文件

这个包提供了增强的AI代理功能，包括：
- 与OpenAI API的异步聊天接口
- MCP（Model Context Protocol）客户端支持
- 向量存储和检索功能
- 工具调用和管理

主要模块：
- chat_openai: OpenAI聊天客户端实现
- agent: AI代理协调器
- mcp_client: MCP客户端实现
- mcp_tools: MCP工具配置
- embedding_retriever: 嵌入检索器
- vector_store: 向量存储实现
- _client: 内部客户端实现
"""

# 导出主要的类和函数
from .chat_openai import AsyncChatOpenAI, ChatOpenAIChatResponse
from .agent import Agent
from ._client import MCPClient
from .mcp_tools import PresetMcpTools, McpToolInfo
from .embedding_retriever import EembeddingRetriever
from .vector_store import VectorStore, VectorStoreItem

# 包版本信息
__version__ = "0.1.0"
__author__ = "augmented package authors"
__description__ = "Enhanced AI agent with MCP and RAG capabilities"

# 定义包的公开接口
__all__ = [
    "AsyncChatOpenAI",
    "ChatOpenAIChatResponse",
    "Agent",
    "MCPClient",
    "PresetMcpTools",
    "McpToolInfo",
    "EembeddingRetriever",
    "VectorStore",
    "VectorStoreItem",
]
