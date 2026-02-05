"""
test_formatter.py - CodeFormatter 的单元测试
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from formatter import CodeFormatter


class TestCodeFormatter:
    """测试 CodeFormatter 类"""
    
    def test_initialization(self):
        """测试 CodeFormatter 初始化"""
        formatter = CodeFormatter()
        assert formatter.line_length == 79
        assert formatter.indent_size == 4
    
    def test_initialization_custom_params(self):
        """测试自定义参数初始化"""
        formatter = CodeFormatter(line_length=100, indent_size=2)
        assert formatter.line_length == 100
        assert formatter.indent_size == 2
    
    def test_fix_whitespace(self):
        """测试修复空白字符"""
        formatter = CodeFormatter()
        code = "def hello():\n\treturn 'Hello'"
        
        formatted = formatter.format_code(code)
        assert '\t' not in formatted
    
    def test_fix_operator_spacing(self):
        """测试修复操作符间距"""
        formatter = CodeFormatter()
        code = "x=1+2"
        
        formatted = formatter._fix_operator_spacing(code)
        assert ' = ' in formatted
    
    def test_fix_trailing_whitespace(self):
        """测试移除行尾空白"""
        formatter = CodeFormatter()
        code = "x = 1   \ny = 2  "
        
        formatted = formatter._fix_trailing_whitespace(code)
        lines = formatted.split('\n')
        assert not lines[0].endswith(' ')
        assert not lines[1].endswith(' ')
    
    def test_check_line_length(self):
        """测试检查行长度"""
        formatter = CodeFormatter(line_length=10)
        code = "x = 1\ny = 2 + 3 + 4 + 5 + 6"
        
        long_lines = formatter.check_line_length(code)
        assert len(long_lines) > 0
        assert 2 in long_lines
    
    def test_format_code(self):
        """测试完整的代码格式化"""
        formatter = CodeFormatter()
        code = "x=1\ny=2"
        
        formatted = formatter.format_code(code)
        assert isinstance(formatted, str)
        assert len(formatted) > 0
