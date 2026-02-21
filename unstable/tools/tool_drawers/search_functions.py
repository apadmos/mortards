import os
import re

from agent_parts.chat_parts.tool_request import ToolRequest


def truncate_context(content, max_len):
    if len(content) <= max_len:
        return content
    return content[:max_len] + '...'


def truncate_around_match(content, match_start, max_len):
    if len(content) <= max_len:
        return content
    half = max_len // 2
    start = max(0, match_start - half)
    end = min(len(content), start + max_len)
    if end - start < max_len:
        start = max(0, end - max_len)
    prefix = '...' if start > 0 else ''
    suffix = '...' if end < len(content) else ''
    return prefix + content[start:end] + suffix


def search_in_files(args: ToolRequest):
    path = args.get("path,name,content")
    pattern = args.get("pattern,regex")
    exclude = args.get("exclude") or []
    path = os.path.abspath(path)
    """Search for pattern across files (regex supported)."""
    results = []

    regex = re.compile(pattern)
    extensions = set([".py", ".css", ".txt"]) - set(exclude)

    MAX_LINE_LEN = 750
    CONTEXT_LINES = 3
    for root, dirs, files in os.walk(path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                path = os.path.join(root, file)
                with open(path) as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        line_stripped = line.rstrip('\n')
                        sr = regex.search(line_stripped)
                        if not sr:
                            continue

                        content = truncate_around_match(line_stripped, sr.start(), MAX_LINE_LEN)

                        context_before = [
                            truncate_context(lines[j].rstrip('\n'), MAX_LINE_LEN)
                            for j in range(max(0, i - CONTEXT_LINES), i)
                        ]
                        context_after = [
                            truncate_context(lines[j].rstrip('\n'), MAX_LINE_LEN)
                            for j in range(i + 1, min(len(lines), i + 1 + CONTEXT_LINES))
                        ]

                        results.append({
                            'file': path,
                            'line': i + 1,  # 1-indexed
                            'content': content,
                            'match_span': sr.span(),
                            'context_before': context_before,
                            'context_after': context_after,
                        })
    return results


def find_file(name=None, filename=None, path: str = None, recursive: bool = True) -> str:
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
