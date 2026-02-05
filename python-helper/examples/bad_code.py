"""
bad_code.py - 示例：包含各种代码问题的文件

这个文件故意包含一些代码问题，用于演示 Python Helper 的修复能力。
"""

# 注意：这些导入故意未使用，用于测试未使用导入的检测和移除功能
import os
import sys

def calculate(x,y):
    result=x+y
    return result

class Calculator:
    def add(self,a,b):
        return a+b
    
    def subtract(self,a,b):
        return a-b
    
    def multiply(self,a,b):
        result=a*b
        return result
    
    def divide(self,a,b):
        if b==0:
            return None
        return a/b

def process_data(data):
    if data is None:
        return []
    
    result=[]
    for item in data:
        if item>0:
            result.append(item*2)
    return result

def complex_function(a,b,c,d,e):
    if a>0:
        if b>0:
            if c>0:
                if d>0:
                    if e>0:
                        return a+b+c+d+e
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    else:
        return 0
