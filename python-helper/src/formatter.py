"""
代码格式化模块

提供代码格式化功能，确保符合 PEP 8 标准。
"""

import re
from typing import List, Optional


class CodeFormatter:
    """代码格式化器类"""
    
    def __init__(self, line_length: int = 79, indent_size: int = 4) -> None:
        """
        初始化代码格式化器。
        
        Args:
            line_length: 最大行长度
            indent_size: 缩进大小（空格数）
        """
        self.line_length = line_length
        self.indent_size = indent_size
    
    def format_file(self, filepath: str) -> None:
        """
        格式化文件。
        
        Args:
            filepath: 要格式化的文件路径
            
        Raises:
            FileNotFoundError: 当文件不存在时
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        formatted_code = self.format_code(code)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_code)
    
    def format_code(self, code: str) -> str:
        """
        格式化代码。
        
        Args:
            code: 原始代码
            
        Returns:
            格式化后的代码
        """
        # 应用各种格式化规则
        code = self._fix_whitespace(code)
        code = self._fix_blank_lines(code)
        code = self._fix_imports(code)
        code = self._fix_trailing_whitespace(code)
        
        return code
    
    def _fix_whitespace(self, code: str) -> str:
        """
        修复空白字符。
        
        Args:
            code: 原始代码
            
        Returns:
            修复后的代码
        """
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 替换 tab 为空格
            line = line.replace('\t', ' ' * self.indent_size)
            
            # 修复操作符周围的空格
            line = self._fix_operator_spacing(line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_operator_spacing(self, line: str) -> str:
        """
        修复操作符周围的空格。
        
        Args:
            line: 代码行
            
        Returns:
            修复后的代码行
        """
        # 确保赋值操作符周围有空格
        line = re.sub(r'(\w)=(\w)', r'\1 = \2', line)
        
        # 确保比较操作符周围有空格
        line = re.sub(r'(\w)==(\w)', r'\1 == \2', line)
        line = re.sub(r'(\w)!=(\w)', r'\1 != \2', line)
        line = re.sub(r'(\w)<=(\w)', r'\1 <= \2', line)
        line = re.sub(r'(\w)>=(\w)', r'\1 >= \2', line)
        
        # 确保逗号后有空格
        line = re.sub(r',(\S)', r', \1', line)
        
        return line
    
    def _fix_blank_lines(self, code: str) -> str:
        """
        修复空行。
        
        Args:
            code: 原始代码
            
        Returns:
            修复后的代码
        """
        lines = code.split('\n')
        fixed_lines = []
        prev_blank = False
        
        for i, line in enumerate(lines):
            is_blank = not line.strip()
            
            # 类和函数定义前应有两个空行
            if i > 0 and (line.strip().startswith('class ') or 
                         line.strip().startswith('def ') and 
                         lines[i-1].strip() and 
                         not lines[i-1].strip().startswith('@')):
                if not prev_blank:
                    fixed_lines.append('')
                    fixed_lines.append('')
            
            # 避免连续多个空行
            if not (is_blank and prev_blank):
                fixed_lines.append(line)
            
            prev_blank = is_blank
        
        return '\n'.join(fixed_lines)
    
    def _fix_imports(self, code: str) -> str:
        """
        修复导入语句的格式。
        
        Args:
            code: 原始代码
            
        Returns:
            修复后的代码
        """
        lines = code.split('\n')
        fixed_lines = []
        import_section = []
        in_imports = False
        
        for line in lines:
            stripped = line.strip()
            
            # 检测导入语句
            if stripped.startswith('import ') or stripped.startswith('from '):
                in_imports = True
                import_section.append(line)
            elif in_imports and not stripped:
                # 导入部分结束
                if import_section:
                    # 排序导入语句
                    sorted_imports = self._sort_imports(import_section)
                    fixed_lines.extend(sorted_imports)
                    import_section = []
                in_imports = False
                fixed_lines.append(line)
            else:
                if in_imports:
                    # 非导入行，结束导入部分
                    if import_section:
                        sorted_imports = self._sort_imports(import_section)
                        fixed_lines.extend(sorted_imports)
                        import_section = []
                    in_imports = False
                fixed_lines.append(line)
        
        # 处理末尾的导入
        if import_section:
            sorted_imports = self._sort_imports(import_section)
            fixed_lines.extend(sorted_imports)
        
        return '\n'.join(fixed_lines)
    
    def _sort_imports(self, imports: List[str]) -> List[str]:
        """
        排序导入语句。
        
        Args:
            imports: 导入语句列表
            
        Returns:
            排序后的导入语句列表
        """
        # 按标准库、第三方库、本地库分组
        stdlib = []
        thirdparty = []
        local = []
        
        for imp in imports:
            stripped = imp.strip()
            if stripped.startswith('from .') or stripped.startswith('import .'):
                local.append(imp)
            elif any(lib in stripped for lib in ['os', 'sys', 're', 'ast', 'typing']):
                stdlib.append(imp)
            else:
                thirdparty.append(imp)
        
        # 每组内部排序
        stdlib.sort()
        thirdparty.sort()
        local.sort()
        
        # 组合，组间加空行
        result = []
        if stdlib:
            result.extend(stdlib)
        if thirdparty:
            if result:
                result.append('')
            result.extend(thirdparty)
        if local:
            if result:
                result.append('')
            result.extend(local)
        
        return result
    
    def _fix_trailing_whitespace(self, code: str) -> str:
        """
        移除行尾空白字符。
        
        Args:
            code: 原始代码
            
        Returns:
            修复后的代码
        """
        lines = code.split('\n')
        fixed_lines = [line.rstrip() for line in lines]
        return '\n'.join(fixed_lines)
    
    def check_line_length(self, code: str) -> List[int]:
        """
        检查超长的行。
        
        Args:
            code: 代码
            
        Returns:
            超长行的行号列表
        """
        lines = code.split('\n')
        long_lines = []
        
        for i, line in enumerate(lines, 1):
            if len(line) > self.line_length:
                long_lines.append(i)
        
        return long_lines
