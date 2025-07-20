import traceback

class CodeInterpreterTool:
    def evaluate_code(self, code: str) -> dict:
        try:
            # Try to compile the code to catch syntax errors
            compiled = compile(code, '<string>', 'exec')
            # Try to execute the code in a safe namespace
            exec_namespace = {}
            exec(compiled, exec_namespace)
            return {"success": True, "output": "Code executed successfully.", "errors": []}
        except Exception as e:
            tb = traceback.format_exc()
            return {"success": False, "output": "", "errors": [str(e), tb]} 