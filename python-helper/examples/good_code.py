"""
good_code.py - 示例：符合规范的良好代码

这个文件展示了遵循 PEP 8 和最佳实践的代码。
"""

from typing import List, Optional


def calculate(x: int, y: int) -> int:
    """
    计算两个数的和。
    
    Args:
        x: 第一个数
        y: 第二个数
        
    Returns:
        两个数的和
    """
    result = x + y
    return result


class Calculator:
    """计算器类，提供基本的数学运算功能。"""
    
    def add(self, a: float, b: float) -> float:
        """
        加法运算。
        
        Args:
            a: 第一个数
            b: 第二个数
            
        Returns:
            两个数的和
        """
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """
        减法运算。
        
        Args:
            a: 被减数
            b: 减数
            
        Returns:
            差值
        """
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """
        乘法运算。
        
        Args:
            a: 第一个因子
            b: 第二个因子
            
        Returns:
            乘积
        """
        result = a * b
        return result
    
    def divide(self, a: float, b: float) -> Optional[float]:
        """
        除法运算。
        
        Args:
            a: 被除数
            b: 除数
            
        Returns:
            商，如果除数为零则返回 None
        """
        if b == 0:
            return None
        return a / b


def process_data(data: Optional[List[int]]) -> List[int]:
    """
    处理数据列表，将正数翻倍。
    
    Args:
        data: 输入数据列表
        
    Returns:
        处理后的数据列表
    """
    if data is None:
        return []
    
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result


def sum_positive(a: int, b: int, c: int, d: int, e: int) -> int:
    """
    计算所有正数的和。
    
    Args:
        a: 第一个数
        b: 第二个数
        c: 第三个数
        d: 第四个数
        e: 第五个数
        
    Returns:
        所有正数的和，如果没有正数则返回 0
    """
    numbers = [a, b, c, d, e]
    positive_numbers = [num for num in numbers if num > 0]
    
    if not positive_numbers:
        return 0
    
    return sum(positive_numbers)
