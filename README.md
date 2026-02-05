# AI_agent
创建各种主流的ai_agent智能体

## 已实现的智能体

### 1. Python Helper Agent

Python Bug修复专家，专注于修复各种代码错误。

**主要功能：**
- 遵循 PEP 8 编码规范
- 修复程序及代码错误，并直接修改源代码使其正确
- 处理程序运行中所报的错误，并修改源代码
- 编写清晰的文档字符串
- 创建全面的单元测试
- 优化代码性能和可读性
- 使用类型提示增强代码质量

**文档：** 详见 [python-helper/README.md](python-helper/README.md)

## 项目结构

```
AI_agent/
├── README.md
└── python-helper/          # Python 代码修复智能体
    ├── agent.yaml         # 智能体配置
    ├── README.md         # 详细文档
    ├── requirements.txt  # 依赖包
    ├── src/             # 源代码
    │   ├── analyzer.py
    │   ├── fixer.py
    │   ├── formatter.py
    │   ├── docstring_generator.py
    │   └── test_generator.py
    ├── tests/           # 单元测试
    └── examples/        # 使用示例
```

## 快速开始

### Python Helper Agent

```bash
# 安装依赖
cd python-helper
pip install -r requirements.txt

# 运行示例
python examples/usage_example.py

# 运行测试
pytest tests/
```

## 贡献

欢迎贡献新的智能体实现！

## 许可证

MIT License
