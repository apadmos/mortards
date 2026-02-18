def syntax_check(path):
    """Check if Python file has syntax errors."""
    try:
        with open(path) as f:
            compile(f.read(), path, 'exec')
        return {"valid": True}
    except SyntaxError as e:
        return {
            "valid": False,
            "error": str(e),
            "line": e.lineno,
            "offset": e.offset
        }