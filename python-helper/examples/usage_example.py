"""
示例：使用 Python Helper Agent 分析和修复代码

这个示例展示了如何使用 Python Helper 的各种功能。
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analyzer import CodeAnalyzer
from fixer import BugFixer
from formatter import CodeFormatter
from docstring_generator import DocstringGenerator
from test_generator import TestGenerator


def example_analyze_code():
    """演示代码分析功能"""
    print("=== 代码分析示例 ===\n")
    
    code = """
def calculate(x,y):
    return x+y

class MyClass:
    def method(self,a,b):
        return a*b
"""
    
    analyzer = CodeAnalyzer()
    issues = analyzer.analyze_code(code)
    
    print(f"发现 {len(issues)} 个问题：")
    for issue in issues:
        print(f"  - 第 {issue.line} 行：{issue.message}")
    
    stats = analyzer.get_statistics()
    print(f"\n统计：{stats}")


def example_fix_code():
    """演示代码修复功能"""
    print("\n=== 代码修复示例 ===\n")
    
    code = """
def calculate(x, y):
    return x + y

class MyClass:
    def method(self, a, b):
        return a * b
"""
    
    fixer = BugFixer()
    issues = fixer.analyzer.analyze_code(code)
    fixed_code = fixer.fix_code(code, issues)
    
    print("修复后的代码：")
    print(fixed_code)
    
    summary = fixer.get_fix_summary()
    print(f"\n修复统计：{summary}")


def example_format_code():
    """演示代码格式化功能"""
    print("\n=== 代码格式化示例 ===\n")
    
    code = """
import os
import sys
from typing import List

def my_function(x,y,z):
    result=x+y+z
    return result
"""
    
    formatter = CodeFormatter()
    formatted_code = formatter.format_code(code)
    
    print("格式化后的代码：")
    print(formatted_code)


def example_generate_docstring():
    """演示文档字符串生成功能"""
    print("\n=== 文档字符串生成示例 ===\n")
    
    # Google 风格
    gen_google = DocstringGenerator(style='google')
    docstring = gen_google.generate_for_function(
        'calculate',
        ['x', 'y'],
        'int'
    )
    print("Google 风格文档字符串：")
    print(docstring)
    
    # NumPy 风格
    gen_numpy = DocstringGenerator(style='numpy')
    docstring = gen_numpy.generate_for_function(
        'calculate',
        ['x', 'y'],
        'int'
    )
    print("\n\nNumPy 风格文档字符串：")
    print(docstring)


def example_generate_tests():
    """演示测试生成功能"""
    print("\n=== 测试生成示例 ===\n")
    
    code = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class Calculator:
    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
"""
    
    # pytest 风格
    gen_pytest = TestGenerator(test_framework='pytest')
    tests = gen_pytest.generate_tests_for_code(code, 'calculator')
    
    print("生成的 pytest 测试：")
    print(tests)


def main():
    """主函数"""
    print("Python Helper Agent - 使用示例\n")
    print("=" * 50)
    
    example_analyze_code()
    example_fix_code()
    example_format_code()
    example_generate_docstring()
    example_generate_tests()
    
    print("\n" + "=" * 50)
    print("示例运行完成！")


if __name__ == "__main__":
    main()
