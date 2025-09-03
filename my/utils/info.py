# 导入pathlib模块中的Path类，用于跨平台的路径操作
from pathlib import Path

# 步骤1: 获取当前文件(__file__)的绝对路径
# 步骤2: 通过连续调用.parent四次来向上遍历目录层级，找到项目根目录
# 目录结构分析：
#   当前文件位置: PROJECT_ROOT/my/utils/info.py
#   .parent (第1次): PROJECT_ROOT/my/utils/     (info.py的父目录)
#   .parent (第2次): PROJECT_ROOT/my/           (utils目录的父目录)  
#   .parent (第3次): PROJECT_ROOT/              (my目录的父目录)
#   .parent (第4次): PROJECT_ROOT的父目录        (项目根目录的父目录)
# 注意: 根据当前的目录结构，应该只需要3个.parent来到达PROJECT_ROOT
PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent
