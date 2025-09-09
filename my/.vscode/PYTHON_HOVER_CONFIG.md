# Python悬停详细程度配置指南

## 配置说明

此配置文件 (`settings.json`) 允许您像TypeScript一样调整Python的悬停详细程度。

## 主要配置项

### 1. 类型检查模式
```json
"python.analysis.typeCheckingMode": "basic"
```
- `"off"`: 关闭类型检查
- `"basic"`: 基本类型检查（推荐）
- `"strict"`: 严格类型检查

### 2. 诊断严重性级别
每个诊断项可以设置为以下级别：
- `"error"`: 错误（红色）
- `"warning"`: 警告（黄色）
- `"information"`: 信息（蓝色）
- `"none"`: 不显示

### 3. 常用配置示例

**减少干扰的配置**：
```json
"python.analysis.diagnosticSeverityOverrides": {
  "reportUnusedImport": "none",
  "reportUnusedVariable": "none",
  "reportShadowedImports": "none"
}
```

**严格检查配置**：
```json
"python.analysis.diagnosticSeverityOverrides": {
  "reportMissingImports": "error",
  "reportUndefinedVariable": "error",
  "reportGeneralTypeIssues": "error"
}
```

## 如何调整

1. 打开VSCode设置 (Ctrl+, 或 Cmd+,)
2. 搜索 "python.analysis.diagnosticSeverityOverrides"
3. 根据需要调整各个诊断项的严重性级别

## 生效方式

- 保存配置文件后，VSCode会自动重新加载
- 可能需要重启VSCode使某些设置完全生效
- 打开Python文件查看悬停提示的变化

## 常用诊断项

| 诊断项 | 描述 | 默认级别 |
|--------|------|----------|
| reportMissingImports | 缺失导入 | error |
| reportUndefinedVariable | 未定义变量 | error |
| reportUnusedImport | 未使用导入 | warning |
| reportGeneralTypeIssues | 一般类型问题 | error |
| reportUnusedVariable | 未使用变量 | warning |
