import ast
import operator


class BrainiacTools:
    """Tools Brainiac can use to perform everyday tasks."""

    def calculate(self, expression):
        """Safely calculate basic mathematical expressions."""

        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        def evaluate(node):
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 10:
                    raise ValueError("Exponent is too large.")

                return allowed_operators[type(node.op)](left, right)

            if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](evaluate(node.operand))

            raise ValueError("I can only calculate basic mathematical expressions.")

        try:
            tree = ast.parse(expression, mode="eval")
            result = evaluate(tree.body)
            return f"The answer is {result}."

        except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
            return "Sorry, I couldn't calculate that expression."
