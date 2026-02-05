"""
Bug 修复器模块

提供自动修复代码问题的功能。
"""

import ast
import re
from typing import List, Optional, Dict, Any
from pathlib import Path

from .analyzer import CodeIssue, CodeAnalyzer


class BugFixer:
    """Bug 修复器类"""
    
    def __init__(self) -> None:
        """初始化 Bug 修复器"""
        self.analyzer = CodeAnalyzer()
        self.fixes_applied: List[Dict[str, Any]] = []
    
    def fix_file(self, filepath: str, issues: Optional[List[CodeIssue]] = None) -> bool:
        """
        修复文件中的问题。
        
        Args:
            filepath: 要修复的文件路径
            issues: 要修复的问题列表，如果为 None 则自动分析
            
        Returns:
            是否成功修复
            
        Raises:
            FileNotFoundError: 当文件不存在时
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        # 如果没有提供问题列表，先分析文件
        if issues is None:
            issues = self.analyzer.analyze_file(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 修复代码
        fixed_code = self.fix_code(code, issues)
        
        # 写回文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_code)
        
        return True
    
    def fix_code(self, code: str, issues: List[CodeIssue]) -> str:
        """
        修复代码中的问题。
        
        Args:
            code: 原始代码
            issues: 要修复的问题列表
            
        Returns:
            修复后的代码
        """
        self.fixes_applied = []
        lines = code.split('\n')
        
        # 按行号排序问题（从后往前修复，避免行号变化）
        sorted_issues = sorted(issues, key=lambda x: x.line, reverse=True)
        
        for issue in sorted_issues:
            if issue.code == "W0002":  # 缺少文档字符串
                lines = self._add_docstring(lines, issue)
            elif issue.code.startswith("I000"):  # 类型提示相关
                # 类型提示需要更复杂的处理，这里先跳过
                pass
        
        return '\n'.join(lines)
    
    def _add_docstring(self, lines: List[str], issue: CodeIssue) -> List[str]:
        """
        添加文档字符串。
        
        Args:
            lines: 代码行列表
            issue: 代码问题
            
        Returns:
            修复后的代码行列表
        """
        line_idx = issue.line - 1
        if line_idx >= len(lines):
            return lines
        
        # 找到函数或类定义
        def_line = lines[line_idx]
        indent = len(def_line) - len(def_line.lstrip())
        inner_indent = indent + 4
        
        # 提取函数或类名
        match = re.search(r'(def|class)\s+(\w+)', def_line)
        if not match:
            return lines
        
        obj_type, obj_name = match.groups()
        
        # 生成简单的文档字符串
        if obj_type == 'def':
            docstring = f'{" " * inner_indent}"""{obj_name} 函数的文档字符串。"""'
        else:
            docstring = f'{" " * inner_indent}"""{obj_name} 类的文档字符串。"""'
        
        # 插入文档字符串
        lines.insert(line_idx + 1, docstring)
        
        self.fixes_applied.append({
            'line': issue.line,
            'type': 'docstring',
            'message': f'为 {obj_name} 添加了文档字符串'
        })
        
        return lines
    
    def fix_indentation(self, code: str, tab_size: int = 4) -> str:
        """
        修复代码缩进。
        
        Args:
            code: 原始代码
            tab_size: Tab 的空格数
            
        Returns:
            修复后的代码
        """
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 替换 tab 为空格
            fixed_line = line.replace('\t', ' ' * tab_size)
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines)
    
    def fix_line_length(self, code: str, max_length: int = 79) -> str:
        """
        修复过长的代码行。
        
        Args:
            code: 原始代码
            max_length: 最大行长度
            
        Returns:
            修复后的代码
        """
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            if len(line) <= max_length:
                fixed_lines.append(line)
            else:
                # 简单处理：在合适的位置换行
                # 实际应用中需要更复杂的逻辑
                fixed_lines.append(line[:max_length])
                fixed_lines.append(' ' * 4 + line[max_length:])
        
        return '\n'.join(fixed_lines)
    
    def remove_unused_imports(self, code: str) -> str:
        """
        移除未使用的导入。
        
        Args:
            code: 原始代码
            
        Returns:
            修复后的代码
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code
        
        # 收集所有导入
        imports: Dict[str, int] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node.lineno
        
        # 检查导入是否被使用
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
        
        # 移除未使用的导入行
        lines = code.split('\n')
        unused_lines = set()
        
        for name, lineno in imports.items():
            if name not in used_names:
                unused_lines.add(lineno - 1)
        
        fixed_lines = [
            line for idx, line in enumerate(lines)
            if idx not in unused_lines
        ]
        
        return '\n'.join(fixed_lines)
    
    def get_fix_summary(self) -> Dict[str, Any]:
        """
        获取修复摘要。
        
        Returns:
            包含修复统计的字典
        """
        return {
            'total_fixes': len(self.fixes_applied),
            'fixes': self.fixes_applied
        }
