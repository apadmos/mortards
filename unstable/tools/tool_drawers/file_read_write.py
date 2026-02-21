import os

from agent_parts.chat_parts.tool_request import ToolRequest


class FileReadWriteTools:

    def __init__(self, write_sandbox: str = None):
        self.write_sandbox = write_sandbox
        self.has_read = set()

    def read_or_ls(self, args: ToolRequest):
        path = args.get("path,name,content")
        path = os.path.abspath(path)
        if os.path.isdir(path):
            recursive = bool(args.get("recursive,r") or False)
            if not recursive:
                files = os.listdir(path)
                return "\n".join(files)
            else:
                all = []
                for root, dirs, files in os.walk(path):
                    for file in files:
                        all.append(os.path.join(root, file))
                    for dir in dirs:
                        all.append(os.path.join(root, dir))
                all = "\n".join(all)
                return all

        elif os.path.isfile(path):
            contents = open(path).read()
            return contents
        return f"DIRECTORY NOT FOUND {path}"

    def write(self, args: ToolRequest):
        path = args.get("path,name")
        content = args.get("contents,content,body")
        """create the directory if that doesn't exist"""
        with open(path, 'w') as f:
            f.write(content)
        return f"SUCCESS wrote contents to file {path}"
