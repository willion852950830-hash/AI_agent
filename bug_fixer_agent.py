import asyncio
import sys
import ast
import re
from typing import Dict, List, Optional, Any
from copilot import CopilotClient
from copilot.tools import define_tool
from copilot.generated.session_events import SessionEventType
from pydantic import BaseModel, Field


class AnalyzeCodeParams(BaseModel):
    code: str = Field(description="The Python code to analyze for bugs")


class FixCodeParams(BaseModel):
    code: str = Field(description="The buggy Python code to fix")
    error_message: Optional[str] = Field(default=None, description="Optional error message if available")


def detect_syntax_errors(code: str) -> List[Dict[str, str]]:
    """检测代码中的语法错误 / Detect syntax errors in code"""
    errors = []
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append({
            "type": "语法错误 / SyntaxError",
            "line": str(e.lineno) if e.lineno else "未知",
            "message": str(e.msg),
            "details": f"行 {e.lineno}: {e.text}" if e.text else ""
        })
    return errors


def detect_common_bugs(code: str) -> List[Dict[str, str]]:
    """检测常见的代码问题 / Detect common code issues"""
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        # 检测未使用的变量赋值 / Check for unused variable assignments
        if '=' in line and not line.strip().startswith('#'):
            # 检测可能的比较运算符错误 / Check for possible comparison operator errors
            if re.search(r'\bif\s+.*\s*=\s*[^=]', line):
                issues.append({
                    "type": "可能的赋值错误 / Possible Assignment Error",
                    "line": str(i),
                    "message": "在if语句中使用了赋值运算符(=)而不是比较运算符(==)",
                    "suggestion": "检查是否应该使用 == 进行比较"
                })
        
        # 检测除零错误 / Check for division by zero
        if re.search(r'/\s*0\b', line) and not line.strip().startswith('#'):
            issues.append({
                "type": "潜在除零错误 / Potential Division by Zero",
                "line": str(i),
                "message": "代码中存在除以0的操作",
                "suggestion": "添加检查以避免除零错误"
            })
        
        # 检测未关闭的文件 / Check for unclosed files
        if 'open(' in line and 'with' not in line and not line.strip().startswith('#'):
            issues.append({
                "type": "资源泄漏风险 / Resource Leak Risk",
                "line": str(i),
                "message": "文件打开但可能未正确关闭",
                "suggestion": "使用 'with' 语句确保文件正确关闭"
            })
        
        # 检测可变默认参数 / Check for mutable default arguments
        if re.search(r'def\s+\w+\([^)]*=\s*\[', line) or re.search(r'def\s+\w+\([^)]*=\s*\{', line):
            issues.append({
                "type": "可变默认参数 / Mutable Default Argument",
                "line": str(i),
                "message": "使用了可变对象作为默认参数",
                "suggestion": "使用 None 作为默认值，然后在函数内部初始化"
            })
    
    return issues


def analyze_code_structure(code: str) -> Dict[str, Any]:
    """分析代码结构 / Analyze code structure"""
    try:
        tree = ast.parse(code)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        
        return {
            "函数数量 / Functions": len(functions),
            "类数量 / Classes": len(classes),
            "导入数量 / Imports": len(imports),
            "函数列表 / Function List": functions[:5],  # 只显示前5个
            "类列表 / Class List": classes[:5]
        }
    except Exception:
        return {"error": "无法解析代码结构"}


@define_tool(description="分析Python代码并检测潜在的bug和问题 / Analyze Python code and detect potential bugs and issues")
async def analyze_code(params: AnalyzeCodeParams) -> dict:
    """分析代码并返回发现的问题"""
    code = params.code
    
    # 检测语法错误
    syntax_errors = detect_syntax_errors(code)
    
    # 检测常见问题
    common_bugs = detect_common_bugs(code)
    
    # 分析代码结构
    structure = analyze_code_structure(code)
    
    result = {
        "状态 / Status": "分析完成 / Analysis Complete",
        "语法错误 / Syntax Errors": syntax_errors if syntax_errors else "无 / None",
        "常见问题 / Common Issues": common_bugs if common_bugs else "无 / None",
        "代码结构 / Code Structure": structure
    }
    
    return result


@define_tool(description="自动修复Python代码中的常见bug / Automatically fix common bugs in Python code")
async def fix_code(params: FixCodeParams) -> dict:
    """尝试自动修复代码中的问题"""
    code = params.code
    error_msg = params.error_message
    fixed_code = code
    fixes_applied = []
    
    # 修复常见的缩进问题 / Fix common indentation issues
    if "IndentationError" in str(error_msg):
        lines = code.split('\n')
        # 简单的缩进修复
        fixed_lines = []
        for line in lines:
            # 移除行首的多余空格
            stripped = line.lstrip()
            if stripped:
                # 保持基本的缩进结构
                indent_level = (len(line) - len(stripped)) // 4
                fixed_lines.append('    ' * indent_level + stripped)
            else:
                fixed_lines.append(line)
        fixed_code = '\n'.join(fixed_lines)
        fixes_applied.append("修复了缩进错误 / Fixed indentation errors")
    
    # 修复if语句中的赋值错误 / Fix assignment in if statements
    if re.search(r'\bif\s+.*\s*=\s*[^=]', code):
        fixed_code = re.sub(r'(\bif\s+[^=]*?)=([^=])', r'\1==\2', fixed_code)
        fixes_applied.append("将if语句中的'='修改为'==' / Changed '=' to '==' in if statement")
    
    # 添加with语句包装文件操作 / Add with statement for file operations
    if 'open(' in code and 'with' not in code:
        fixes_applied.append("建议：使用with语句包装文件操作 / Suggestion: Wrap file operations with 'with' statement")
    
    result = {
        "状态 / Status": "修复完成 / Fix Complete",
        "应用的修复 / Fixes Applied": fixes_applied if fixes_applied else ["无需修复 / No fixes needed"],
        "修复后的代码 / Fixed Code": fixed_code if fixes_applied else "代码看起来正常 / Code looks fine"
    }
    
    return result


@define_tool(description="提供Python代码bug修复的建议和最佳实践 / Provide suggestions and best practices for Python bug fixing")
async def suggest_fixes(params: AnalyzeCodeParams) -> dict:
    """提供代码改进建议"""
    suggestions = []
    code = params.code
    
    # 检查是否有异常处理 / Check for exception handling
    if 'try' not in code:
        suggestions.append({
            "类型 / Type": "异常处理 / Exception Handling",
            "建议 / Suggestion": "考虑添加try-except块来处理潜在的错误"
        })
    
    # 检查是否有文档字符串 / Check for docstrings
    if '"""' not in code and "'''" not in code:
        suggestions.append({
            "类型 / Type": "文档 / Documentation",
            "建议 / Suggestion": "添加文档字符串以提高代码可读性"
        })
    
    # 检查类型提示 / Check for type hints
    if 'def ' in code and '->' not in code:
        suggestions.append({
            "类型 / Type": "类型提示 / Type Hints",
            "建议 / Suggestion": "考虑添加类型提示以提高代码安全性"
        })
    
    return {
        "建议数量 / Number of Suggestions": len(suggestions),
        "建议列表 / Suggestions": suggestions if suggestions else ["代码质量良好 / Code quality looks good"]
    }


async def main():
    """主函数 / Main function"""
    client = CopilotClient({
        "cli_url": "171.80.9.194:4321"
    })
    await client.start()

    session = await client.create_session({
        "model": "gpt-4.1",
        "streaming": True,
        "tools": [analyze_code, fix_code, suggest_fixes],
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()

    session.on(handle_event)

    print("🐛 Python Bug修复智能体 / Python Bug Fixer Agent")
    print("=" * 60)
    print("功能 / Features:")
    print("  • 分析代码并检测bug / Analyze code and detect bugs")
    print("  • 自动修复常见错误 / Automatically fix common errors")
    print("  • 提供代码改进建议 / Provide code improvement suggestions")
    print("\n示例问题 / Example Questions:")
    print("  • 帮我分析这段代码: [粘贴代码]")
    print("  • 这段代码有什么问题: [粘贴代码]")
    print("  • 如何修复这个错误: [描述错误]")
    print("\n输入 'exit' 退出 / Type 'exit' to quit\n")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break

        if user_input.lower() == "exit":
            break

        sys.stdout.write("Assistant: ")
        await session.send_and_wait({"prompt": user_input})
        print("\n")

    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
