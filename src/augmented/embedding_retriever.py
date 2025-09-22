from dataclasses import dataclass, field
import os

import httpx
from rich import print as rprint

from augmented.vector_store import VectorStore, VectorStoreItem


# 嵌入检索器类，负责处理文本嵌入和向量检索
@dataclass
class EembeddingRetriever:
    """嵌入检索器，处理文本嵌入生成和向量相似性检索"""
    
    embedding_model: str  # 使用的嵌入模型名称
    vector_store: VectorStore = field(default_factory=VectorStore)  # 向量存储实例

    # 内部嵌入方法，调用嵌入API生成文本向量
    async def _embed(self, text: str) -> list[float] | None:
        """内部方法：调用嵌入API将文本转换为向量表示"""
        # 获取嵌入API的基础URL，优先使用EMBEDDING_BASE_URL，其次使用OPENAI_BASE_URL
        base_url = os.environ.get("EMBEDDING_BASE_URL") or os.environ.get(
            "OPENAI_BASE_URL"
        )
        # 获取API密钥，优先使用EMBEDDING_KEY，其次使用OPENAI_API_KEY
        api_key = os.environ.get("EMBEDDING_KEY") or os.environ.get("OPENAI_API_KEY")
        url = f"{base_url}/embeddings"  # 构建完整的API端点URL
        headers = {
            "Authorization": f"Bearer {api_key}",  # 认证头
            "Content-Type": "application/json",  # 内容类型头
        }
        data = {
            "model": self.embedding_model,  # 指定嵌入模型
            "input": text,  # 输入文本
            "encoding_format": "float",  # 编码格式为浮点数
        }
        # 使用异步HTTP客户端发送请求
        async with httpx.AsyncClient() as client:
            try:
                # 发送POST请求到嵌入API
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()  # 检查HTTP状态码，出错时抛出异常
                rprint(response)  # 打印响应信息（用于调试）
                resp_data = response.json()  # 解析JSON响应
                result: list[float] = resp_data["data"][0]["embedding"]  # 提取嵌入向量
                rprint(result)  # 打印嵌入向量（用于调试）
                return result  # 返回嵌入向量
            except httpx.HTTPStatusError as http_err:
                # 处理HTTP状态错误
                print(f"HTTP error occurred: {http_err}")
            except Exception as err:
                # 处理其他异常
                print(f"An error occurred: {err}")

    # 查询嵌入方法，将查询文本转换为向量
    async def embed_query(self, query: str) -> list[float] | None:
        """将查询文本转换为嵌入向量"""
        result = await self._embed(query)  # 调用内部嵌入方法
        return result  # 返回嵌入向量

    # 文档嵌入方法，将文档文本转换为向量并存储
    async def embed_documents(self, document: str) -> list[float] | None:
        """将文档文本转换为嵌入向量并添加到向量存储"""
        result = await self._embed(document)  # 调用内部嵌入方法生成向量
        # 将文档和对应的嵌入向量添加到向量存储
        self.vector_store.add(VectorStoreItem(embedding=result, document=document))
        return result  # 返回嵌入向量

    # 检索方法，根据查询文本查找最相关的文档
    async def retrieve(self, query: str, top_k: int = 5) -> list[VectorStoreItem]:
        """根据查询文本检索最相关的文档"""
        query_embedding = await self.embed_query(query)  # 将查询文本转换为向量
        # 在向量存储中搜索最相似的文档
        return self.vector_store.search(query_embedding, top_k)
