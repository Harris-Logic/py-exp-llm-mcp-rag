"""
modified from https://modelcontextprotocol.io/quickstart/client  in tab 'python'
"""
import asyncio
import os
from mcp import Tool
from openai import AsyncOpenAI
from dataclasses import dataclass, field

from openai.types import FunctionDefinition
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
import dotenv
from pydantic import BaseModel
from rich import print as rprint

from utils import pretty

dotenv.load_dotenv()  # 读取.env里的API等信息
# 直接从chat_openai.py里拿过来 from import

