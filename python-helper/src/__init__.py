"""
Python Helper - 代码分析和修复工具包

这个包提供了一套工具来分析、修复和优化 Python 代码。
"""

from typing import List

__version__ = "1.0.0"
__author__ = "AI Agent Team"

__all__: List[str] = [
    "CodeAnalyzer",
    "BugFixer",
    "CodeFormatter",
    "DocstringGenerator",
    "TestGenerator",
]

# 延迟导入以避免循环依赖
def __getattr__(name: str):
    """延迟导入模块组件"""
    if name == "CodeAnalyzer":
        from .analyzer import CodeAnalyzer
        return CodeAnalyzer
    elif name == "BugFixer":
        from .fixer import BugFixer
        return BugFixer
    elif name == "CodeFormatter":
        from .formatter import CodeFormatter
        return CodeFormatter
    elif name == "DocstringGenerator":
        from .docstring_generator import DocstringGenerator
        return DocstringGenerator
    elif name == "TestGenerator":
        from .test_generator import TestGenerator
        return TestGenerator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
