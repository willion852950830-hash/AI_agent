"""
代码分析器模块

提供代码质量分析和问题检测功能。
"""

import ast
from typing import List, Dict, Any, Optional
from pathlib import Path


class CodeIssue:
    """代码问题类"""
    
    def __init__(
        self,
        line: int,
        column: int,
        message: str,
        severity: str,
        code: str
    ) -> None:
        """
        初始化代码问题实例。
        
        Args:
            line: 问题所在行号
            column: 问题所在列号
            message: 问题描述
            severity: 问题严重性 (error, warning, info)
            code: 问题代码
        """
        self.line = line
        self.column = column
        self.message = message
        self.severity = severity
        self.code = code
    
    def __repr__(self) -> str:
        """返回问题的字符串表示"""
        return (
            f"CodeIssue(line={self.line}, column={self.column}, "
            f"severity={self.severity}, message={self.message})"
        )


class CodeAnalyzer:
    """代码分析器类"""
    
    def __init__(self) -> None:
        """初始化代码分析器"""
        self.issues: List[CodeIssue] = []
    
    def analyze_file(self, filepath: str) -> List[CodeIssue]:
        """
        分析 Python 文件。
        
        Args:
            filepath: 要分析的文件路径
            
        Returns:
            检测到的代码问题列表
            
        Raises:
            FileNotFoundError: 当文件不存在时
            SyntaxError: 当文件包含语法错误时
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.analyze_code(code)
    
    def analyze_code(self, code: str) -> List[CodeIssue]:
        """
        分析 Python 代码字符串。
        
        Args:
            code: 要分析的 Python 代码
            
        Returns:
            检测到的代码问题列表
        """
        self.issues = []
        
        try:
            tree = ast.parse(code)
            self._check_ast(tree)
        except SyntaxError as e:
            issue = CodeIssue(
                line=e.lineno or 0,
                column=e.offset or 0,
                message=f"语法错误: {e.msg}",
                severity="error",
                code="E0001"
            )
            self.issues.append(issue)
        
        return self.issues
    
    def _check_ast(self, tree: ast.AST) -> None:
        """
        检查 AST 树中的代码问题。
        
        Args:
            tree: Python AST 树
        """
        for node in ast.walk(tree):
            self._check_function_complexity(node)
            self._check_missing_docstrings(node)
            self._check_missing_type_hints(node)
    
    def _check_function_complexity(self, node: ast.AST) -> None:
        """检查函数复杂度"""
        if isinstance(node, ast.FunctionDef):
            # 简单的复杂度检查：统计嵌套层数
            complexity = self._calculate_complexity(node)
            if complexity > 10:
                issue = CodeIssue(
                    line=node.lineno,
                    column=node.col_offset,
                    message=f"函数 '{node.name}' 复杂度过高 ({complexity})",
                    severity="warning",
                    code="W0001"
                )
                self.issues.append(issue)
    
    def _check_missing_docstrings(self, node: ast.AST) -> None:
        """检查是否缺少文档字符串"""
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                issue = CodeIssue(
                    line=node.lineno,
                    column=node.col_offset,
                    message=f"{type(node).__name__} '{node.name}' 缺少文档字符串",
                    severity="warning",
                    code="W0002"
                )
                self.issues.append(issue)
    
    def _check_missing_type_hints(self, node: ast.AST) -> None:
        """检查是否缺少类型提示"""
        if isinstance(node, ast.FunctionDef):
            # 检查参数类型提示
            for arg in node.args.args:
                if arg.annotation is None and arg.arg != 'self':
                    issue = CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        message=f"参数 '{arg.arg}' 缺少类型提示",
                        severity="info",
                        code="I0001"
                    )
                    self.issues.append(issue)
            
            # 检查返回值类型提示
            if node.returns is None:
                issue = CodeIssue(
                    line=node.lineno,
                    column=node.col_offset,
                    message=f"函数 '{node.name}' 缺少返回值类型提示",
                    severity="info",
                    code="I0002"
                )
                self.issues.append(issue)
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """
        计算函数的圈复杂度。
        
        Args:
            node: 函数定义节点
            
        Returns:
            复杂度值
        """
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取分析统计信息。
        
        Returns:
            包含统计信息的字典
        """
        stats: Dict[str, Any] = {
            'total': len(self.issues),
            'errors': 0,
            'warnings': 0,
            'info': 0
        }
        
        for issue in self.issues:
            if issue.severity == 'error':
                stats['errors'] += 1
            elif issue.severity == 'warning':
                stats['warnings'] += 1
            elif issue.severity == 'info':
                stats['info'] += 1
        
        return stats
