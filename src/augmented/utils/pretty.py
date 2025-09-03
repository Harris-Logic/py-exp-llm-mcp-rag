# 导入所需的模块和类
from dataclasses import dataclass  # 导入dataclass装饰器，用于简化类的定义
import rich                         # 导入rich库主模块，用于富文本控制台输出
from rich.rule import Rule          # 导入Rule类，用于创建水平分隔线和标题规则
from rich.text import Text          # 导入Text类，用于创建富文本对象
from rich import print as rprint    # 导入rich的print函数并重命名，提供彩色输出

from rich.console import Console    # 导入Console类，用于更高级的控制台操作

# 步骤1: 创建全局的Rich控制台实例
# 这个实例可以在整个模块中重复使用，提供一致的输出格式
RICH_CONSOLE = Console()


@dataclass
class ALogger:
    """
    高级日志记录器类，支持带前缀的标题输出
    使用dataclass装饰器自动生成初始化方法和其他特殊方法
    """
    prefix: str = ""  # 日志前缀，默认为空字符串，用于标识日志来源

    def title(self, text: str | Text, rule_style="bright_black"):
        """
        输出带前缀的标题规则线
        
        Args:
            text: 标题文本，可以是字符串或Rich Text对象
            rule_style: 规则线的样式，默认为亮黑色
        """
        # 步骤1: 创建标题组件列表，用于组合前缀和标题文本
        lits = []
        
        # 步骤2: 如果设置了前缀，则添加到列表中
        # 使用rich.markup.escape()确保前缀中的特殊字符不会被解释为markup
        if self.prefix:
            lits.append(rich.markup.escape(self.prefix))
        
        # 步骤3: 如果提供了标题文本，则添加到列表中
        if text:
            lits.append(text)
        
        # 步骤4: 创建并输出Rule对象
        # 使用" ".join()将前缀和文本用空格连接，作为Rule的标题
        rprint(Rule(title=" ".join(lits), style=rule_style))


def log_title(text: str | Text, rule_style="bright_black"):
    """
    输出简单的标题规则线（无前缀版本）
    
    Args:
        text: 标题文本，可以是字符串或Rich Text对象
        rule_style: 规则线的样式，默认为亮黑色
    """
    # 步骤1: 创建输出对象列表
    objs = []
    
    # 步骤2: 如果提供了文本，创建Rule对象并添加到列表
    if text:
        objs.append(Rule(title=text, style=rule_style))
    
    # 步骤3: 使用解包操作符(*)输出所有对象
    # 这种方式可以同时输出多个Rule对象（虽然这里通常只有一个）
    rprint(*objs)


# 主程序入口 - 仅在直接运行此文件时执行
if __name__ == "__main__":
    # 步骤1: 创建ALogger实例，设置前缀为"[utils]"
    # 步骤2: 调用title方法输出示例标题
    # 这将显示一个带有前缀的水平分隔线，标题为"[utils] Hello World!"
    ALogger("[utils]").title("Hello World!")
