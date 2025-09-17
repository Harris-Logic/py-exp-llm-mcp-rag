# UV Python 版本管理指南

## 当前配置状态

✅ **已成功配置**：
- UV 版本：0.8.17
- Python 版本：3.12.3（与项目要求一致）
- 虚拟环境：`.venv/`（已创建并激活）
- 所有依赖：已通过 `uv sync` 安装完成

## 常用命令

### 1. 激活虚拟环境
```bash
source .venv/bin/activate
```

### 2. 安装/更新依赖
```bash
# 同步所有依赖（推荐）
uv sync

# 安装单个包
uv add <package-name>

# 安装开发依赖
uv add --group dev <package-name>
```

### 3. Python 版本管理
```bash
# 使用特定Python版本创建虚拟环境
uv venv .venv --python 3.12

# 查看可用的Python版本
uv python list

# 安装特定Python版本
uv python install 3.12
```

### 4. 依赖管理
```bash
# 查看已安装的包
uv pip list

# 更新所有包
uv pip install --upgrade --upgrade-strategy eager -r <(uv pip freeze)

# 生成requirements.txt
uv pip freeze > requirements.txt
```

## 项目结构说明

- `.python-version`: 指定项目使用的Python版本（3.12）
- `pyproject.toml`: 项目配置和依赖声明
- `uv.lock`: 依赖锁文件，确保环境一致性
- `.venv/`: 虚拟环境目录（已配置在VSCode中显示）

## VSCode 配置

已在 `.vscode/settings.json` 中配置显示 `.venv` 文件夹：
```json
{
    "files.exclude": {
        "**/.venv": false
    },
    "search.exclude": {
        "**/.venv": false
    }
}
```

## 开发工作流

1. **启动开发**：
   ```bash
   source .venv/bin/activate
   ```

2. **运行项目**：
   ```bash
   python rag_example.py
   ```

3. **添加新依赖**：
   ```bash
   uv add <new-package>
   uv sync
   ```

4. **更新依赖**：
   ```bash
   uv sync
   ```

## 优势

- ⚡ **极速安装**: uv 比 pip 快 10-100 倍
- 🔒 **确定性构建**: 通过 lock 文件确保环境一致性  
- 🐍 **多版本支持**: 轻松管理多个 Python 版本
- 📦 **一体化工具**: 替代 pip、virtualenv、pip-tools 等多个工具

## 故障排除

如果遇到权限问题，可以设置链接模式为 copy：
```bash
export UV_LINK_MODE=copy
uv sync
```

或者直接使用参数：
```bash
uv sync --link-mode=copy
```

## 更多信息

- [UV 官方文档](https://github.com/astral-sh/uv)
- [Python 版本管理指南](https://docs.astral.sh/uv/guides/python/)
