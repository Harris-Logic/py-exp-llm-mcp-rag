from dataclasses import dataclass, field
from typing import Self


# 向量存储项类，包含嵌入向量和对应的文档内容
@dataclass
class VectorStoreItem:
    """向量存储中的单个项目，包含文本的嵌入向量和原始文档内容"""
    
    embedding: list[float]  # 文本的嵌入向量表示
    document: str  # 原始文档文本内容


# 向量存储类，用于存储和检索向量化的文档
@dataclass
class VectorStore:
    """向量存储实现，支持添加文档和基于余弦相似度的检索"""
    
    items: list[VectorStoreItem] = field(default_factory=list)  # 存储所有向量项目的列表

    # 添加向量项目到存储中
    def add(self, item: VectorStoreItem) -> Self:
        """向向量存储中添加一个新的向量项目"""
        self.items.append(item)  # 将项目添加到列表中
        return self  # 返回自身以支持链式调用

    # 搜索与查询向量最相似的项目
    def search(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list[VectorStoreItem]:
        """根据查询向量搜索最相似的前k个文档"""
        # 对所有项目按与查询向量的余弦相似度进行排序，取前top_k个
        result = sorted(
            self.items,  # 要排序的项目列表
            key=lambda item: self._cosine_similarity(query_embedding, item.embedding),  # 按相似度排序
            reverse=True,  # 降序排列（相似度从高到低）
        )[:top_k]  # 取前top_k个结果
        return result  # 返回搜索结果

    # 计算两个向量之间的余弦相似度
    def _cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        """计算两个向量之间的余弦相似度"""
        # 计算向量点积
        dot_product = sum(a * b for a, b in zip(v1, v2))
        # 计算第一个向量的模长
        magnitude_v1 = sum(a**2 for a in v1) ** 0.5
        # 计算第二个向量的模长
        magnitude_v2 = sum(b**2 for b in v2) ** 0.5
        # 返回余弦相似度（点积除以模长的乘积）
        return dot_product / (magnitude_v1 * magnitude_v2)
