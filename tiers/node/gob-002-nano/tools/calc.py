import ast
import operator

# Safe math operations mapping
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expr_str: str) -> float:
    """Safely evaluate mathematical expressions without using eval()."""
    try:
        node = ast.parse(expr_str, mode='eval')
        return _eval_node(node.body)
    except (ValueError, TypeError, SyntaxError, ZeroDivisionError) as e:
        raise ValueError(f"Invalid expression: {e}")

def _eval_node(node):
    """Recursively evaluate AST nodes for mathematical expressions."""
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Only numbers are allowed")
    elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
        return node.n
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op = OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
        return op(left, right)
    
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op = OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary operation: {type(node.op).__name__}")
        return op(operand)
    
    else:
        raise ValueError(f"Unsupported node type: {type(node).__name__}")

def run(arg: str) -> str:
    """Safely evaluate mathematical expressions."""
    if not arg or len(arg) > 200:  # Limit input length
        return "Invalid input: expression too long or empty"
    
    try:
        result = safe_eval(arg.strip())
        return f"{arg} = {result}"
    except ValueError as e:
        return f"Error: {e}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Calculation error: {e}"
