"""
测试生成器模块

自动为 Python 代码生成单元测试。
"""

import ast
from typing import List, Dict, Any, Optional
from pathlib import Path


class TestGenerator:
    """测试生成器类"""
    
    def __init__(self, test_framework: str = 'pytest') -> None:
        """
        初始化测试生成器。
        
        Args:
            test_framework: 测试框架，支持 'pytest' 或 'unittest'
        """
        self.test_framework = test_framework.lower()
        if self.test_framework not in ['pytest', 'unittest']:
            raise ValueError("测试框架必须是 'pytest' 或 'unittest'")
    
    def generate_tests(self, filepath: str) -> str:
        """
        为文件生成测试代码。
        
        Args:
            filepath: 源代码文件路径
            
        Returns:
            生成的测试代码
            
        Raises:
            FileNotFoundError: 当文件不存在时
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.generate_tests_for_code(code, path.stem)
    
    def generate_tests_for_code(
        self,
        code: str,
        module_name: str
    ) -> str:
        """
        为代码生成测试。
        
        Args:
            code: 源代码
            module_name: 模块名
            
        Returns:
            生成的测试代码
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return ""
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Collect all functions, we'll filter later
                functions.append(node)
            elif isinstance(node, ast.ClassDef):
                classes.append(node)
        
        # Filter to only top-level functions (not inside classes)
        top_level_functions = []
        for func in functions:
            is_top_level = True
            for cls in classes:
                if func in cls.body:
                    is_top_level = False
                    break
            if is_top_level:
                top_level_functions.append(func)
        
        if self.test_framework == 'pytest':
            return self._generate_pytest_tests(
                module_name, top_level_functions, classes
            )
        else:
            return self._generate_unittest_tests(
                module_name, top_level_functions, classes
            )
    
    def _generate_pytest_tests(
        self,
        module_name: str,
        functions: List[ast.FunctionDef],
        classes: List[ast.ClassDef]
    ) -> str:
        """
        生成 pytest 测试代码。
        
        Args:
            module_name: 模块名
            functions: 函数列表
            classes: 类列表
            
        Returns:
            测试代码
        """
        lines = [
            '"""',
            f'{module_name} 模块的测试',
            '"""',
            '',
            'import pytest',
            f'from {module_name} import *',
            '',
            ''
        ]
        
        # 为函数生成测试
        for func in functions:
            if not func.name.startswith('_'):
                lines.extend(self._generate_function_test_pytest(func))
                lines.append('')
                lines.append('')
        
        # 为类生成测试
        for cls in classes:
            lines.extend(self._generate_class_test_pytest(cls))
            lines.append('')
            lines.append('')
        
        return '\n'.join(lines)
    
    def _generate_function_test_pytest(
        self,
        func: ast.FunctionDef
    ) -> List[str]:
        """
        为函数生成 pytest 测试。
        
        Args:
            func: 函数节点
            
        Returns:
            测试代码行列表
        """
        func_name = func.name
        test_name = f'test_{func_name}'
        
        lines = [
            f'def {test_name}():',
            f'    """{func_name} 函数的测试"""',
            '    # TODO: 实现测试逻辑',
            f'    # result = {func_name}()',
            '    # assert result is not None',
            '    pass'
        ]
        
        return lines
    
    def _generate_class_test_pytest(
        self,
        cls: ast.ClassDef
    ) -> List[str]:
        """
        为类生成 pytest 测试。
        
        Args:
            cls: 类节点
            
        Returns:
            测试代码行列表
        """
        cls_name = cls.name
        test_class_name = f'Test{cls_name}'
        
        lines = [
            f'class {test_class_name}:',
            f'    """{cls_name} 类的测试"""',
            '',
            '    def test_initialization(self):',
            '        """测试类初始化"""',
            '        # TODO: 实现测试逻辑',
            f'        # obj = {cls_name}()',
            '        # assert obj is not None',
            '        pass'
        ]
        
        # 为类方法生成测试
        for node in cls.body:
            if isinstance(node, ast.FunctionDef):
                # 跳过私有方法（除了__init__），但包括公共方法
                if node.name.startswith('_') and node.name != '__init__':
                    continue
                if node.name == '__init__':
                    continue
                lines.append('')
                lines.append(f'    def test_{node.name}(self):')
                lines.append(f'        """测试 {node.name} 方法"""')
                lines.append('        # TODO: 实现测试逻辑')
                lines.append('        pass')
        
        return lines
    
    def _generate_unittest_tests(
        self,
        module_name: str,
        functions: List[ast.FunctionDef],
        classes: List[ast.ClassDef]
    ) -> str:
        """
        生成 unittest 测试代码。
        
        Args:
            module_name: 模块名
            functions: 函数列表
            classes: 类列表
            
        Returns:
            测试代码
        """
        lines = [
            '"""',
            f'{module_name} 模块的测试',
            '"""',
            '',
            'import unittest',
            f'from {module_name} import *',
            '',
            ''
        ]
        
        # 为函数生成测试类
        if functions:
            lines.append('class TestFunctions(unittest.TestCase):')
            lines.append('    """测试模块函数"""')
            lines.append('')
            
            for func in functions:
                if not func.name.startswith('_'):
                    lines.extend(
                        self._generate_function_test_unittest(func)
                    )
                    lines.append('')
            
            lines.append('')
        
        # 为类生成测试类
        for cls in classes:
            lines.extend(self._generate_class_test_unittest(cls))
            lines.append('')
            lines.append('')
        
        lines.append('if __name__ == "__main__":')
        lines.append('    unittest.main()')
        
        return '\n'.join(lines)
    
    def _generate_function_test_unittest(
        self,
        func: ast.FunctionDef
    ) -> List[str]:
        """
        为函数生成 unittest 测试。
        
        Args:
            func: 函数节点
            
        Returns:
            测试代码行列表
        """
        func_name = func.name
        test_name = f'test_{func_name}'
        
        lines = [
            f'    def {test_name}(self):',
            f'        """{func_name} 函数的测试"""',
            '        # TODO: 实现测试逻辑',
            f'        # result = {func_name}()',
            '        # self.assertIsNotNone(result)',
            '        pass'
        ]
        
        return lines
    
    def _generate_class_test_unittest(
        self,
        cls: ast.ClassDef
    ) -> List[str]:
        """
        为类生成 unittest 测试。
        
        Args:
            cls: 类节点
            
        Returns:
            测试代码行列表
        """
        cls_name = cls.name
        test_class_name = f'Test{cls_name}'
        
        lines = [
            f'class {test_class_name}(unittest.TestCase):',
            f'    """{cls_name} 类的测试"""',
            '',
            '    def test_initialization(self):',
            '        """测试类初始化"""',
            '        # TODO: 实现测试逻辑',
            f'        # obj = {cls_name}()',
            '        # self.assertIsNotNone(obj)',
            '        pass'
        ]
        
        # 为类方法生成测试
        for node in cls.body:
            if isinstance(node, ast.FunctionDef):
                # 跳过私有方法（除了__init__），但包括公共方法
                if node.name.startswith('_') and node.name != '__init__':
                    continue
                if node.name == '__init__':
                    continue
                lines.append('')
                lines.append(f'    def test_{node.name}(self):')
                lines.append(f'        """测试 {node.name} 方法"""')
                lines.append('        # TODO: 实现测试逻辑')
                lines.append('        pass')
        
        return lines
    
    def save_tests(self, tests_code: str, output_path: str) -> None:
        """
        保存测试代码到文件。
        
        Args:
            tests_code: 测试代码
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(tests_code)
