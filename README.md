# mortards
A collection of LLM idiots trying to look smart and write code with the help of a lot of deterministic tools an tricks.


What to do next:

Add more tools to the LLM doesn't have to think or read as much:

Prioriy tools:
list_functions(path) - Lets agent understand files without reading them
search_in_files(pattern) - Find examples of existing code
syntax_check(path) - Self-correct errors immediately
get_file_summary(path) - Quick context gathering
save_note(key, value) - Remember important details across conversation


A pile of tool suggestions:
AVAILABLE TOOLS:

read_file(path) - Read entire file
write_file(path, content) - Write/overwrite file
delete_file(path) - Delete a file
rename_file(old_path, new_path) - Rename/move file
copy_file(src, dest) - Copy a file


list_directory(path) - List files in directory
find_file(name) - Find file by name
get_project_structure() - See entire project layout
get_related_files(path) - Find related files (templates, data access, etc)


list_functions(path) - List all functions in a file
list_classes(path) - List all classes and methods
get_imports(path) - See what a file imports
get_file_summary(path) - Get overview without reading whole file


search_in_files(pattern, directory=".", extensions=[".py"]) - Search across files
find_usage(identifier) - Find where something is used
find_definition(name) - Find where class/function is defined


syntax_check(path) - Check for syntax errors
lint_file(path) - Run linter


list_tables(schema) - List all database tables
describe_table(name) - Get column info for table


save_note(key, value) - Remember something for later
get_note(key) - Retrieve saved note
list_notes() - See all notes


show_diff(path) - See changes made to file
backup_file(path) - Backup before modifying


Select RAG examples based on the incoming prompt (typically that's me)
```
def build_prompt_with_examples(task, examples):
    """Present multiple examples clearly."""
    
    prompt = f"Task: {task}\n\n"
    
    LOOK FOR HINTS ON WHAT EXAMPLES TO USE HERE
    
    if len(examples) > 1:
        prompt += "REFERENCE EXAMPLES (follow these patterns):\n\n"
        
        for i, ex in enumerate(examples, 1):
            prompt += f"--- Example {i}: {ex['label']} ---\n"
            prompt += f"File: {ex['file']}\n"
            prompt += f"{ex['content']}\n\n"
        
        prompt += "\nNow create your code following these patterns.\n"
    else:
        prompt += f"REFERENCE EXAMPLE:\n{examples[0]['content']}\n\n"
    
    return prompt
 ```
Curate the context:
```

       for attempt in range(3):
            response = self.llm(self.messages)
            
            if self.task_complete(response):
                # IMPORTANT: Remove file contents from context
                self.cleanup_file_reads()
                break
    
    def cleanup_file_reads(self):
        """Remove large file contents, keep only references."""
        for msg in self.messages:
            if 'read_file' in msg.get('content', ''):
                # Replace file contents with just a note
                msg['content'] = re.sub(
                    r'<content>.*?</content>',
                    '<content>[File contents removed to save context]</content>',
                    msg['content'],
                    flags=re.DOTALL
                )
```