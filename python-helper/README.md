# Python Helper Agent

## 概述

Python Helper 是一个专业的 Python 代码修复和优化智能体，专注于：

- 遵循 PEP 8 编码规范
- 修复程序及代码错误，并直接修改源代码使其正确
- 处理程序运行中所报的错误，并修改源代码
- 编写清晰的文档字符串
- 创建全面的单元测试
- 优化代码性能和可读性
- 使用类型提示增强代码质量

## 功能特性

### 1. PEP 8 代码规范检查
自动检查并修复代码以符合 PEP 8 标准。

### 2. 类型提示支持
为 Python 代码添加类型提示，提高代码质量和可维护性。

### 3. 文档字符串生成
自动生成符合 Google/NumPy 风格的文档字符串。

### 4. 单元测试生成
为代码创建全面的单元测试用例。

### 5. 代码优化
优化代码性能和可读性。

## 使用方法

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用示例

```python
from python_helper import CodeAnalyzer, BugFixer, TestGenerator

# 分析代码
analyzer = CodeAnalyzer()
issues = analyzer.analyze_file("example.py")

# 修复代码
fixer = BugFixer()
fixer.fix_file("example.py", issues)

# 生成测试
test_gen = TestGenerator()
test_gen.generate_tests("example.py")
```

## 项目结构

```
python-helper/
├── agent.yaml          # 智能体配置
├── README.md          # 文档
├── requirements.txt   # 依赖
├── src/              # 源代码
│   ├── __init__.py
│   ├── analyzer.py   # 代码分析器
│   ├── fixer.py      # Bug 修复器
│   ├── formatter.py  # 代码格式化
│   ├── docstring_generator.py  # 文档字符串生成
│   └── test_generator.py       # 测试生成器
├── tests/            # 测试文件
└── examples/         # 示例文件
```

## 最佳实践

1. **遵循 PEP 8**: 所有代码都应符合 PEP 8 标准
2. **类型提示**: 为函数参数和返回值添加类型提示
3. **文档字符串**: 为所有公共函数和类添加详细的文档字符串
4. **单元测试**: 保持高测试覆盖率
5. **代码审查**: 定期审查和优化代码

## 许可证

MIT License
