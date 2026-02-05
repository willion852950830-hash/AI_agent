"""
文档字符串生成器模块

自动生成符合规范的文档字符串。
"""

import ast
import re
from typing import List, Dict, Any, Optional


class DocstringGenerator:
    """文档字符串生成器类"""
    
    def __init__(self, style: str = 'google') -> None:
        """
        初始化文档字符串生成器。
        
        Args:
            style: 文档字符串风格，支持 'google' 或 'numpy'
        """
        self.style = style.lower()
        if self.style not in ['google', 'numpy']:
            raise ValueError("风格必须是 'google' 或 'numpy'")
    
    def generate_for_function(
        self,
        func_name: str,
        args: List[str],
        return_type: Optional[str] = None,
        description: Optional[str] = None
    ) -> str:
        """
        为函数生成文档字符串。
        
        Args:
            func_name: 函数名
            args: 参数列表
            return_type: 返回值类型
            description: 函数描述
            
        Returns:
            生成的文档字符串
        """
        if description is None:
            description = f"{func_name} 函数的文档字符串。"
        
        if self.style == 'google':
            return self._generate_google_style(
                description, args, return_type
            )
        else:
            return self._generate_numpy_style(
                description, args, return_type
            )
    
    def _generate_google_style(
        self,
        description: str,
        args: List[str],
        return_type: Optional[str]
    ) -> str:
        """
        生成 Google 风格的文档字符串。
        
        Args:
            description: 描述
            args: 参数列表
            return_type: 返回值类型
            
        Returns:
            文档字符串
        """
        lines = [f'"""{description}']
        
        if args:
            lines.append('')
            lines.append('Args:')
            for arg in args:
                if arg != 'self' and arg != 'cls':
                    lines.append(f'    {arg}: {arg} 参数的描述')
        
        if return_type:
            lines.append('')
            lines.append('Returns:')
            lines.append(f'    {return_type}: 返回值的描述')
        
        lines.append('"""')
        return '\n'.join(lines)
    
    def _generate_numpy_style(
        self,
        description: str,
        args: List[str],
        return_type: Optional[str]
    ) -> str:
        """
        生成 NumPy 风格的文档字符串。
        
        Parameters
        ----------
        description : str
            描述
        args : List[str]
            参数列表
        return_type : Optional[str]
            返回值类型
            
        Returns
        -------
        str
            文档字符串
        """
        lines = [f'"""{description}']
        
        if args:
            lines.append('')
            lines.append('Parameters')
            lines.append('----------')
            for arg in args:
                if arg != 'self' and arg != 'cls':
                    lines.append(f'{arg} : type')
                    lines.append(f'    {arg} 参数的描述')
        
        if return_type:
            lines.append('')
            lines.append('Returns')
            lines.append('-------')
            lines.append(f'{return_type}')
            lines.append('    返回值的描述')
        
        lines.append('"""')
        return '\n'.join(lines)
    
    def generate_for_class(
        self,
        class_name: str,
        description: Optional[str] = None
    ) -> str:
        """
        为类生成文档字符串。
        
        Args:
            class_name: 类名
            description: 类描述
            
        Returns:
            生成的文档字符串
        """
        if description is None:
            description = f"{class_name} 类的文档字符串。"
        
        return f'"""{description}"""'
    
    def generate_for_module(
        self,
        module_name: str,
        description: Optional[str] = None
    ) -> str:
        """
        为模块生成文档字符串。
        
        Args:
            module_name: 模块名
            description: 模块描述
            
        Returns:
            生成的文档字符串
        """
        if description is None:
            description = f"{module_name} 模块的文档字符串。"
        
        lines = [
            f'"""',
            f'{description}',
            f'"""'
        ]
        return '\n'.join(lines)
    
    def parse_function_signature(self, code: str) -> Dict[str, Any]:
        """
        解析函数签名。
        
        Args:
            code: 包含函数定义的代码
            
        Returns:
            包含函数信息的字典
            
        Raises:
            SyntaxError: 当代码包含语法错误时
        """
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                return_type = None
                
                if node.returns:
                    if isinstance(node.returns, ast.Name):
                        return_type = node.returns.id
                    elif isinstance(node.returns, ast.Constant):
                        return_type = str(node.returns.value)
                
                return {
                    'name': node.name,
                    'args': args,
                    'return_type': return_type
                }
        
        return {}
    
    def add_docstring_to_code(self, code: str) -> str:
        """
        为代码中的函数和类添加文档字符串。
        
        Args:
            code: 原始代码
            
        Returns:
            添加了文档字符串的代码
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code
        
        lines = code.split('\n')
        
        # 收集需要添加文档字符串的位置
        positions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    args = [arg.arg for arg in node.args.args]
                    docstring = self.generate_for_function(
                        node.name,
                        args
                    )
                    positions.append((node.lineno, docstring, 'function'))
            elif isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    docstring = self.generate_for_class(node.name)
                    positions.append((node.lineno, docstring, 'class'))
        
        # 从后往前插入，避免行号变化
        positions.sort(reverse=True)
        
        for lineno, docstring, obj_type in positions:
            # 找到定义行
            def_line = lines[lineno - 1]
            indent = len(def_line) - len(def_line.lstrip())
            
            # 插入文档字符串
            docstring_lines = docstring.split('\n')
            indented_docstring = [
                ' ' * (indent + 4) + line if line.strip() else line
                for line in docstring_lines
            ]
            
            # 在定义行之后插入
            for i, line in enumerate(indented_docstring):
                lines.insert(lineno + i, line)
        
        return '\n'.join(lines)
