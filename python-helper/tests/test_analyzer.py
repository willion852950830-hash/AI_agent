"""
test_analyzer.py - CodeAnalyzer 的单元测试
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analyzer import CodeAnalyzer, CodeIssue


class TestCodeIssue:
    """测试 CodeIssue 类"""
    
    def test_initialization(self):
        """测试 CodeIssue 初始化"""
        issue = CodeIssue(
            line=10,
            column=5,
            message="测试问题",
            severity="error",
            code="E0001"
        )
        
        assert issue.line == 10
        assert issue.column == 5
        assert issue.message == "测试问题"
        assert issue.severity == "error"
        assert issue.code == "E0001"
    
    def test_repr(self):
        """测试 CodeIssue 字符串表示"""
        issue = CodeIssue(
            line=10,
            column=5,
            message="测试问题",
            severity="error",
            code="E0001"
        )
        
        repr_str = repr(issue)
        assert "line=10" in repr_str
        assert "column=5" in repr_str
        assert "severity=error" in repr_str


class TestCodeAnalyzer:
    """测试 CodeAnalyzer 类"""
    
    def test_initialization(self):
        """测试 CodeAnalyzer 初始化"""
        analyzer = CodeAnalyzer()
        assert analyzer.issues == []
    
    def test_analyze_valid_code(self):
        """测试分析有效代码"""
        analyzer = CodeAnalyzer()
        code = """
def hello():
    '''Hello function'''
    return "Hello"
"""
        issues = analyzer.analyze_code(code)
        # 可能有类型提示缺失的警告，但不应有语法错误
        assert all(issue.severity != "error" for issue in issues)
    
    def test_analyze_code_with_syntax_error(self):
        """测试分析有语法错误的代码"""
        analyzer = CodeAnalyzer()
        code = "def hello(\n    pass"
        
        issues = analyzer.analyze_code(code)
        assert len(issues) > 0
        assert any(issue.severity == "error" for issue in issues)
    
    def test_check_missing_docstrings(self):
        """测试检查缺失的文档字符串"""
        analyzer = CodeAnalyzer()
        code = """
def function_without_docstring():
    return 42
"""
        issues = analyzer.analyze_code(code)
        docstring_issues = [
            i for i in issues 
            if "文档字符串" in i.message
        ]
        assert len(docstring_issues) > 0
    
    def test_check_missing_type_hints(self):
        """测试检查缺失的类型提示"""
        analyzer = CodeAnalyzer()
        code = """
def add(a, b):
    '''Add two numbers'''
    return a + b
"""
        issues = analyzer.analyze_code(code)
        type_hint_issues = [
            i for i in issues 
            if "类型提示" in i.message
        ]
        assert len(type_hint_issues) > 0
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        analyzer = CodeAnalyzer()
        code = """
def func():
    pass
"""
        analyzer.analyze_code(code)
        stats = analyzer.get_statistics()
        
        assert 'total' in stats
        assert 'errors' in stats
        assert 'warnings' in stats
        assert 'info' in stats
        assert stats['total'] >= 0
