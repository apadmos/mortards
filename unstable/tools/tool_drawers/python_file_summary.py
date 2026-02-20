import ast

class PythonFileSummary:
    
    def __init__(self, path):
        self.path = path

    def get_function_signature(self, function_name):
        """Get the signature of a specific function without reading whole file."""
        with open(self.path) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                args = [arg.arg for arg in node.args.args]
                return f"def {function_name}({', '.join(args)})"
        return None
    
    def list_functions(self):
        """List all functions/methods in a file."""
        with open(self.path) as f:
            tree = ast.parse(f.read())
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                functions.append({
                    'name': node.name,
                    'args': args,
                    'line': node.lineno
                })
        return functions
    
    def list_classes(self):
        """List all classes and their methods."""
        with open(self.path) as f:
            tree = ast.parse(f.read())
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({
                    'name': node.name,
                    'methods': methods,
                    'line': node.lineno
                })
        return classes
    
    def get_imports(self):
        """List all imports in a file."""
        with open(self.path) as f:
            tree = ast.parse(f.read())
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                imports.append(f"from {node.module}")
        return imports
    
    def get_file_summary(self):
        """Get a summary of what's in a file without reading it all."""
        functions = self.list_functions()
        classes = self.list_classes()
        imports = self.get_imports()
    
        return {
            'self.path': self.path,
            'classes': [c['name'] for c in classes],
            'functions': [f['name'] for f in functions],
            'imports': imports
        }

    def __str__(self):
        functions = self.list_functions()
        classes = self.list_classes()

        signature_list = [
            f"{func['name']}({', '.join(func.get('args', []))})"
            for func in functions
        ]
        classes =[c['name'] for c in classes]
        imports = self.get_imports()
        if not signature_list and not classes and not imports:
            return "EMPTY PYTHON FILE"


        return f"FUNCTIONS: {signature_list}\nCLASSES: {classes} \nIMPORTS: {imports}"