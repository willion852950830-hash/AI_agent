# AI_agent
创建各种主流的ai_agent智能体

## 智能体列表 / Agent List

### 1. Weather Assistant (天气助手)
- 文件: `weather_assistant.py`
- 功能: 查询城市天气信息
- 使用: `python weather_assistant.py`

### 2. Bug Fixer Agent (Bug修复智能体)
- 文件: `bug_fixer_agent.py`
- 功能: 自动检测和修复Python代码中的bug
- 使用: `python bug_fixer_agent.py`

#### Bug修复智能体功能:
- ✅ **语法错误检测**: 自动识别Python语法错误
- ✅ **常见bug检测**: 
  - 条件语句中的赋值错误 (= vs ==)
  - 除零错误
  - 文件资源泄漏
  - 可变默认参数
- ✅ **代码结构分析**: 分析函数、类、导入等
- ✅ **自动修复**: 尝试自动修复常见错误
- ✅ **改进建议**: 提供代码质量改进建议

#### 使用示例:
```bash
# 启动智能体
python bug_fixer_agent.py

# 示例对话 (以下代码故意包含错误用于演示)
You: 帮我分析这段代码: 
def add(a, b):
    if a = 0:  # Bug示例: 这里应该用 == 而不是 =
        return b
    return a + b
