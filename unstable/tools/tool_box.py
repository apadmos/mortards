import os

from tools.tool_drawers.python_file_summary import get_file_summary
from tools.tool_drawers.search_functions import find_file, search_in_files, get_project_structure


class ToolBox:

    def all_tools(self):
        return {
            "ls": self.ls,
            "write_file":  self.write_file,
            "rename_file": self.rename_file,
            "read_file": self.read_file,
            "delete_file": self.delete_file,
            "copy_file": self.copy_file,
            "backup_file": self.backup_file,
            "restore_backup": self.restore_backup,
            "inspect_python_file": get_file_summary,
            "locate_file": find_file,
            "find_file": find_file,
            "search_in_files": search_in_files,
            "get_project_structure": lambda: get_project_structure(self.write_sandbox)
        }

    def execute_tool(self, args:dict):
        tool_name = args.pop("tool")
        tool = self.all_tools()[tool_name]
        return tool(**args)


    def check_path(self, path: str, sandbox: str) -> str:
        """Expands a path to absolute and checks if it's in one of the sandboxes."""
        path = os.path.abspath(path)
        if not sandbox:
            return path
        if not path.startswith(sandbox):
            raise Exception(f"Path {path} is not in your sandbox {sandbox}. "
                            f"Stop and ask the user for permissions.")
        return path

    def ls(self, path):
        path = self.check_path(path, self.read_sandbox)
        try:
            items = os.listdir(path)
            return items
        except FileNotFoundError:
            return f"DIRECTORY NOT FOUND {path}"

    def write_file(self, path, content):
        path = self.check_path(path, self.write_sandbox)
        with open(path, 'w') as f:
            f.write(content)
        return f"SUCCESS wrote contents to file {path}"

    def rename_file(self, old_path, dest_path):
        try:
            os.rename(old_path, dest_path)
            return f"SUCCESS renamed {old_path} to {dest_path}"
        except FileNotFoundError:
            return f"FILE NOT FOUND {old_path}"

    def copy_file(self, current_path, dest_path):
        try:

            content = self.read_file(current_path)
            self.write_file(dest_path, content)

            return f"SUCCESS copied {current_path} to {dest_path}"
        except FileNotFoundError:
            return f"FILE NOT FOUND {current_path}"

    def read_file(self, path) -> str:
        try:
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"FILE NOT FOUND {path}"

    def delete_file(self, path):
        os.remove(path)
        return f"SUCCESS Deleted {path}"

    def backup_file(self, path):
        """Create a backup before modifying."""
        backup_path = f"{path}.backup"
        self.copy_file(path, backup_path)
        return backup_path

    def restore_backup(self, path):
        """Restore from backup."""
        backup_path = f"{path}.backup"
        if os.path.exists(backup_path):
            self.copy_file(backup_path, path)
            return True
        return False


