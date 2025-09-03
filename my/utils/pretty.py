# 导入Rich库的相关模块，用于创建美观的控制台输出
from rich.panel import Panel            # 导入Panel类，用于创建带边框的面板显示
from rich.console import RenderableType  # 导入RenderableType类型，用于类型注解
from rich import print as rprint         # 导入rich的print函数并重命名为rprint，提供彩色和格式化输出


def log_title(renderable: RenderableType = "", title: str = "-"):
    """
    创建并显示一个带标题的面板，用于美化日志输出
    
    Args:
        renderable: 面板内容，可以是字符串、富文本或其他可渲染对象，默认为空字符串
        title: 面板标题，显示在面板顶部边框上，默认为"-"
    
    功能说明:
        此函数用于在控制台输出格式化的标题面板，常用于：
        1. 分隔不同的日志区域
        2. 突出显示重要信息
        3. 提高日志的可读性和美观度
    """
    # 步骤1: 使用rich库的Panel创建一个带边框和标题的面板
    # Panel会自动添加边框，并将title显示在顶部边框中央
    # 步骤2: 使用rprint输出格式化的面板到控制台
    # rprint支持Rich的所有渲染特性，包括颜色、样式和布局
    rprint(
        Panel(
            renderable,  # 面板主体内容 - 可以是文本、表格、进度条等任何可渲染对象
            title=title, # 面板标题 - 显示在面板顶部边框上，用于标识内容类型或用途
        )
    )
