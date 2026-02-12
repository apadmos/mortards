import os


class BasicIO:

    def __init__(self, sandbox: str):
        self.sandbox = sandbox

    def sandbox_path(self, path: str):
        path = os.path.abspath(path)
        if not path.startswith(self.sandbox):
            raise Exception(f"Path {path} is not in your sandbox {self.sandbox}. "
                            f"Stop and ask the user for permissions.")
        return path

    def list_directory(self, path):
        try:
            items = os.listdir(path)
            return items
        except FileNotFoundError:
            return f"DIRECTORY NOT FOUND {path}"

    def write_file(self, path, content):
        path = self.sandbox_path(path)
        with open(path, 'w') as f:
            f.write(content)
        return f"SUCCESS wrote contents to file {path}"

    def rename_file(self, old_path, dest_path):
        try:
            old_path = self.sandbox_path(old_path)
            dest_path = self.sandbox_path(dest_path)
            os.rename(old_path, dest_path)
            return f"SUCCESS renamed {old_path} to {dest_path}"
        except FileNotFoundError:
            return f"FILE NOT FOUND {old_path}"

    def copy_file(self, current_path, dest_path):
        try:
            old_path = self.sandbox_path(current_path)
            new_path = self.sandbox_path(dest_path)

            content = self.read_file(old_path)
            self.write_file(new_path, content)

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
        path = self.sandbox_path(path)
        os.remove(path)
        return f"SUCCESS Deleted {path}"

    def find_file(self, name):
        hits = []
        for root, dirs, files in os.walk(self.sandbox):
            if name in files:
                hits.append(os.path.join(root, name))
        if hits:
            if len(hits) > 1:
                return f"Multiple files found: {hits}"
            return hits[0]

        return f"FILE NOT FOUND {name}"

    def backup_file(self, path):
        """Create a backup before modifying."""
        import shutil
        backup_path = f"{path}.backup"
        self.copy_file(path, backup_path)
        return backup_path

    def restore_backup(self, path):
        """Restore from backup."""
        import shutil
        backup_path = f"{path}.backup"
        if os.path.exists(backup_path):
            self.copy_file(backup_path, path)
            return True
        return False
