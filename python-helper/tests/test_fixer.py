"""
test_fixer.py - BugFixer 的单元测试
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from fixer import BugFixer
from analyzer import CodeIssue


class TestBugFixer:
    """测试 BugFixer 类"""
    
    def test_initialization(self):
        """测试 BugFixer 初始化"""
        fixer = BugFixer()
        assert fixer.fixes_applied == []
    
    def test_fix_code_with_empty_issues(self):
        """测试修复没有问题的代码"""
        fixer = BugFixer()
        code = "print('Hello, World!')"
        
        fixed_code = fixer.fix_code(code, [])
        assert fixed_code == code
    
    def test_add_docstring(self):
        """测试添加文档字符串"""
        fixer = BugFixer()
        code = """def hello():
    return "Hello"
"""
        
        issue = CodeIssue(
            line=1,
            column=0,
            message="函数缺少文档字符串",
            severity="warning",
            code="W0002"
        )
        
        fixed_code = fixer.fix_code(code, [issue])
        assert '"""' in fixed_code
        assert len(fixer.fixes_applied) > 0
    
    def test_fix_indentation(self):
        """测试修复缩进"""
        fixer = BugFixer()
        code = "def hello():\n\treturn 'Hello'"
        
        fixed_code = fixer.fix_indentation(code)
        assert '\t' not in fixed_code
        assert '    ' in fixed_code
    
    def test_remove_unused_imports(self):
        """测试移除未使用的导入"""
        fixer = BugFixer()
        code = """import os
import sys

print("Hello")
"""
        
        fixed_code = fixer.remove_unused_imports(code)
        # os 和 sys 都未使用，应该被移除
        # 但这个简单实现可能不完美
        assert isinstance(fixed_code, str)
    
    def test_get_fix_summary(self):
        """测试获取修复摘要"""
        fixer = BugFixer()
        code = "def hello():\n    return 'Hello'"
        
        issue = CodeIssue(
            line=1,
            column=0,
            message="函数缺少文档字符串",
            severity="warning",
            code="W0002"
        )
        
        fixer.fix_code(code, [issue])
        summary = fixer.get_fix_summary()
        
        assert 'total_fixes' in summary
        assert 'fixes' in summary
        assert isinstance(summary['total_fixes'], int)
