from dataclasses import dataclass
import os
import shlex
from typing import Self, Any

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# MCP工具信息类，用于配置和管理MCP工具
@dataclass
class McpToolInfo:
    """MCP工具配置信息类，包含工具名称、shell命令模式和参数配置"""
    
    name: str  # 工具名称
    shell_cmd_pattern: str  # shell命令模式字符串，支持格式化参数
    main_cmd_options: str = ""  # 主命令选项
    mcp_params: str = ""  # MCP特定参数

    # 获取完整的shell命令
    @property
    def shell_cmd(self) -> str:
        """生成完整的shell命令字符串"""
        return self.shell_cmd_pattern.format(
            main_cmd_options=self.main_cmd_options,  # 格式化主命令选项
            mcp_params=self.mcp_params,  # 格式化MCP参数
        )

    # 添加MCP参数
    def append_mcp_params(self, params: str) -> Self:
        """向MCP参数追加内容"""
        if params:
            self.mcp_params += params  # 追加参数内容
        return self  # 返回自身以支持链式调用

    # 添加主命令选项
    def append_main_cmd_options(self, options: str) -> Self:
        """向主命令选项追加内容"""
        if options:
            self.main_cmd_options += options  # 追加选项内容
        return self  # 返回自身以支持链式调用

    # 转换为通用参数字典
    def to_common_params(self) -> dict[str, Any]:
        """将工具配置转换为通用的参数字典"""
        command, *args = shlex.split(self.shell_cmd)  # 解析shell命令为命令和参数列表
        return dict(
            name=self.name,  # 工具名称
            command=command,  # 主命令
            args=args,  # 命令参数列表
        )


# MCP命令选项配置类
class McpCmdOptions:
    """MCP命令选项配置，包含各种环境相关的选项设置"""
    
    # UVX使用国内镜像的选项
    uvx_use_cn_mirror = (
        ("--extra-index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple")  # 清华PyPI镜像
        if os.environ.get("USE_CN_MIRROR")  # 检查是否启用国内镜像
        else ""  # 不启用时返回空字符串
    )
    
    # NPX使用国内镜像的选项
    npx_use_cn_mirror = (
        ("--registry https://registry.npmmirror.com")  # npm国内镜像
        if os.environ.get("USE_CN_MIRROR")  # 检查是否启用国内镜像
        else ""  # 不启用时返回空字符串
    )
    
    # Fetch服务器使用代理的选项
    fetch_server_mcp_use_proxy = (
        f"--proxy-url {os.environ.get('PROXY_URL')}"  # 代理URL配置
        if os.environ.get("PROXY_URL")  # 检查是否配置了代理
        else ""  # 未配置代理时返回空字符串
    )


# 预设MCP工具类
class PresetMcpTools:
    """预设的MCP工具配置，包含常用的MCP服务器工具"""
    
    # 文件系统工具配置
    filesystem = McpToolInfo(
        name="filesystem",  # 工具名称：文件系统
        shell_cmd_pattern="npx {main_cmd_options} -y @modelcontextprotocol/server-filesystem {mcp_params}",  # npx命令模式
    ).append_main_cmd_options(
        McpCmdOptions.npx_use_cn_mirror,  # 添加npm国内镜像选项
    )
    
    # 网络抓取工具配置
    fetch = (
        McpToolInfo(
            name="fetch",  # 工具名称：网络抓取
            shell_cmd_pattern="uvx {main_cmd_options} mcp-server-fetch {mcp_params}",  # uvx命令模式
        )
        .append_main_cmd_options(
            McpCmdOptions.uvx_use_cn_mirror,  # 添加PyPI国内镜像选项
        )
        .append_mcp_params(
            McpCmdOptions.fetch_server_mcp_use_proxy,  # 添加代理配置选项
        )
    )
