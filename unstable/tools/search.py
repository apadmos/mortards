def search_in_files(pattern, directory=".", extensions=[".py"]):
    """Search for pattern across files (regex supported)."""
    import re, os
    results = []
    regex = re.compile(pattern)

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


def find_usage(identifier, directory="."):
    """Find where a function/class/variable is used."""
    return search_in_files(rf'\b{identifier}\b', directory)


def find_definition(class_or_function_name):
    """Find where something is defined."""
    return search_in_files(rf'^(class|def)\s+{class_or_function_name}\b', ".")