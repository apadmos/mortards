import os


class ProjectView:

    def __init__(self, root_dir:str, project_dir:str, modules_di:str):
        self.root_dir = root_dir
        self.project_dir = project_dir
        self.modules_dir = modules_di

    def print_tree(self, startpath, prefix=''):
        output = ""
        for index, entry in enumerate(sorted(os.listdir(startpath))):
            path = os.path.join(startpath, entry)
            connector = '\n├── ' if index < len(os.listdir(startpath)) - 1 else '\n└── '
            output+= (prefix + connector + entry)
            if os.path.isdir(path):
                extension = '\n│   ' if index < len(os.listdir(startpath)) - 1 else '    '
                output += self.print_tree(path, prefix + extension)
        return output

if __name__ == "__main__":
    pv = ProjectView(root_dir=".", project_dir="cms", modules_di="subs")
    print(pv.print_tree(pv.root_dir))