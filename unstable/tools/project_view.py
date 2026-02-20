import os

from tools.tool_drawers.python_file_summary import PythonFileSummary


class ProjectView:

    def __init__(self, root_dir:str, project_dir:str, modules_di:str):
        self.root_dir = root_dir
        self.project_dir = project_dir
        self.modules_dir = modules_di

    def walk_files(self, start_path, with_details:bool, prefix=''):
        output = ''
        entries = sorted(os.listdir(start_path))
        for entry in entries:
            path = os.path.join(start_path, entry)
            if with_details:
                output += f"{self.summarize_file(path)}\n"
            else:
                output += f"{prefix}{entry}\n"
            if os.path.isdir(path):
                output += self.walk_files(path, with_details=with_details, prefix=prefix + ' ')
        return output

    def file_contents(self, path):
        with open(path) as f:
            contents = f.read()
        return f"CONTENTS OF {path}:\n\n{contents}"

    def summarize_file(self, path):
        if path.endswith(".py"):
            return f"--------------PYTHON FILE {path}--------------\n{PythonFileSummary(path)}"
        elif os.path.isfile(path):
            return f"--------------STATIC FILE {path}--------------\n{self.summarize_static_file(path)}"
        elif os.path.isdir(path):
            return f"--------------DIRECTORY {path}--------------\n{self.summarize_dir(path)}"
        else:
            return f"--------------UNKNOWN FILE TYPE {path}--------------"

    def summarize_static_file(self, path):
        # Static file summary
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        line_count = len(lines)
        preview = "".join(lines[:5])[:1500] # first 5 lines (or fewer)
        if not preview:
            preview = "EMPTY FILE"
        return (
            f"LINE COUNT: {line_count}\n"
            f"CONTENT PREVIEW:\n{preview}"
        )

    def summarize_dir(self, path):
        return f"CONTAINS FILES: {os.listdir(path)}"

    def summarize_project_dir(self, path):
        return f"SUMMARY OF PROJECT DIRECTORY: {path}\n{self.walk_files(path, with_details=True)}"

    def summarize_module_dir(self):
        s = f"SUMMARY OF SUBMODULES:\n"
        for sub in ["crudepg", "servelamb", "servelamb_users", "fancycli"]:
            path = os.path.join('subs', sub)
            s += f"{sub}: {self.walk_files(path, with_details=True)}\n"
        return s

    def summarize_project(self, args:dict):
        return f"{self.summarize_project_dir(self.project_dir)}\n{self.summarize_module_dir()}"


if __name__ == "__main__":
    pv = ProjectView(root_dir=".", project_dir="media", modules_di="subs")
    p = f"""{pv.summarize_project({})}"""
    print(p)