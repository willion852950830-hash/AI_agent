"""
测试用例 - 包含各种常见bug的Python代码示例
Test Cases - Python code examples with various common bugs
"""

# 示例1: 条件语句中使用赋值运算符而不是比较运算符
# Example 1: Using assignment operator instead of comparison in if statement
def example_1_wrong():
    x = 5
    if x = 5:  # Bug: 应该使用 == 而不是 =
        print("x is 5")

# 修复后的版本
def example_1_fixed():
    x = 5
    if x == 5:  # Fixed: 使用 == 进行比较
        print("x is 5")


# 示例2: 除零错误
# Example 2: Division by zero
def example_2_wrong(a, b):
    return a / 0  # Bug: 除以0

# 修复后的版本
def example_2_fixed(a, b):
    if b == 0:
        return None  # 或者抛出异常
    return a / b


# 示例3: 文件未正确关闭
# Example 3: File not properly closed
def example_3_wrong():
    f = open('test.txt', 'r')  # Bug: 文件可能不会被正确关闭
    content = f.read()
    return content

# 修复后的版本
def example_3_fixed():
    with open('test.txt', 'r') as f:  # Fixed: 使用with语句
        content = f.read()
    return content


# 示例4: 可变默认参数
# Example 4: Mutable default argument
def example_4_wrong(item, lst=[]):  # Bug: 可变默认参数
    lst.append(item)
    return lst

# 修复后的版本
def example_4_fixed(item, lst=None):  # Fixed: 使用None作为默认值
    if lst is None:
        lst = []
    lst.append(item)
    return lst


# 示例5: 缩进错误
# Example 5: Indentation error
def example_5_wrong():
    x = 1
    y = 2
   z = 3  # Bug: 缩进不正确
    return x + y + z

# 修复后的版本
def example_5_fixed():
    x = 1
    y = 2
    z = 3  # Fixed: 正确的缩进
    return x + y + z


# 示例6: 缺少异常处理
# Example 6: Missing exception handling
def example_6_wrong(filename):
    f = open(filename, 'r')  # Bug: 没有异常处理
    content = f.read()
    f.close()
    return content

# 修复后的版本
def example_6_fixed(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None


if __name__ == "__main__":
    print("这个文件包含了多个常见bug的示例")
    print("使用bug_fixer_agent.py来分析和修复这些问题")
    print("\nThis file contains examples of common bugs")
    print("Use bug_fixer_agent.py to analyze and fix these issues")
