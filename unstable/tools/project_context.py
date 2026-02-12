import ast
import os

def get_function_signature(path, function_name):
    """Get the signature of a specific function without reading whole file."""
    with open(path) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            args = [arg.arg for arg in node.args.args]
            return f"def {function_name}({', '.join(args)})"
    return None

def list_functions(path):
    """List all functions/methods in a file."""
    with open(path) as f:
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

def list_classes(path):
    """List all classes and their methods."""
    with open(path) as f:
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

def get_imports(path):
    """List all imports in a file."""
    with open(path) as f:
        tree = ast.parse(f.read())
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend([alias.name for alias in node.names])
        elif isinstance(node, ast.ImportFrom):
            imports.append(f"from {node.module}")
    return imports

def get_project_structure():
    """Get overview of project organization."""
    structure = {}
    for root, dirs, files in os.walk("."):
        # Skip hidden and virtual env
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']

        rel_root = root.replace("./", "")
        py_files = [f for f in files if f.endswith('.py')]
        if py_files:
            structure[rel_root] = py_files
    return structure


def get_related_files(path):
    """Find files likely related to this one."""
    # Same directory
    dirname = os.path.dirname(path)
    basename = os.path.basename(path).replace('_controller.py', '')

    related = []

    # Look for matching data access
    da_path = f"data_access/{basename}_data_access.py"
    if os.path.exists(da_path):
        related.append(da_path)

    # Look for matching templates
    template_path = f"templates/{basename}_*.html"
    import glob
    related.extend(glob.glob(template_path))

    return related


def get_file_summary(path):
    """Get a summary of what's in a file without reading it all."""
    functions = list_functions(path)
    classes = list_classes(path)
    imports = get_imports(path)

    return {
        'path': path,
        'classes': [c['name'] for c in classes],
        'functions': [f['name'] for f in functions],
        'imports': imports[:5]  # First 5 imports
    }