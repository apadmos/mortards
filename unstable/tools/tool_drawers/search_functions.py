import os
import re


def search_in_files(pattern=None, content=None, path=None, directory=None):
    """Search for pattern across files (regex supported)."""
    results = []

    pattern = pattern or content
    regex = re.compile(pattern)
    extensions = [".py", ".css", ".txt"]
    directory = directory or path


    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                path = os.path.join(root, file)
                with open(path) as f:
                    for i, line in enumerate(f, 1):
                        if regex.search(line):
                            results.append({
                                'file': path,
                                'line': i,
                                'content': line.strip()
                            })
    return results

def find_file(name=None, filename=None, path:str=None, recursive:bool=True) -> str:
    name = name or filename
    if path is None:
        path = '.'
    path = os.path.abspath(path)
    hits = []
    for root, dirs, files in os.walk(path, topdown=recursive):
        if name in files or name in dirs:
            hits.append(os.path.join(root, name))
    if hits:
        if len(hits) > 1:
            return f"Multiple files found: {hits}"
        return hits[0]

    return f"FILE NOT FOUND {name}"


def find_usage(identifier, directory="."):
    """Find where a function/class/variable is used."""
    return search_in_files(rf'\b{identifier}\b', directory)


def find_definition(class_or_function_name):
    """Find where something is defined."""
    return search_in_files(rf'^(class|def)\s+{class_or_function_name}\b', ".")


def get_project_structure(path):
    """Get overview of project organization."""
    structure = {}
    for root, dirs, files in os.walk(path):
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
