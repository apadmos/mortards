import re


class ToolCmdInterface:

    def parse_tool_requests(self, llm_output: str) -> list[dict]:
        """
        More robust version that handles multi-line content better.
        Preserves indentation in <content> blocks.
        """

        tools = []

        # Find all <tool> tags with their positions
        tool_matches = list(re.finditer(r'<tool>(.*?)</tool>', llm_output, re.DOTALL))

        if not tool_matches:
            return []

        for i, tool_match in enumerate(tool_matches):

            # Determine boundaries for this tool's parameters
            tool_start = tool_match.start()

            if i + 1 < len(tool_matches):
                tool_end = tool_matches[i + 1].start()
            else:
                tool_end = len(llm_output)

            tool_section = llm_output[tool_start:tool_end]

            tools.append(self.parse_tool_request(tool_section))

        return tools


    def parse_tool_request(self, llm_output: str) -> dict:

        # Extract tool name
        tool_match = re.search(r'<tool>(.*?)</tool>', llm_output, re.DOTALL)
        if not tool_match:
            return None

        tool_name = tool_match.group(1).strip()

        # Extract all other tags dynamically
        params = {}

        # Find all XML tags (excluding <tool>)
        tag_pattern = r'<(\w+)>(.*?)</\1>'
        matches = re.findall(tag_pattern, llm_output, re.DOTALL)

        for tag_name, tag_content in matches:
            if tag_name != 'tool':
                # Strip leading/trailing whitespace but preserve internal formatting
                params[tag_name] = tag_content.strip()

        return {
            'tool': tool_name,
            **params
        }


if __name__ == "__main__":
    tc = ToolCmdInterface()
    print(tc.parse_tool_requests("""
    TOOL EXECUTION FORMAT:
    I think i'll tool around
<tool>write_file</tool>
<path>main.py</path>
<content>
def hello():
    print("world")
</content>

<tool>write_file2</tool>
<path>main_tst.py</path>

Then there is more text

<tool>delete_file</tool>
<path>main_tst.py</path>

Rules:
- No quotes around content
- Content goes between <content> tags exactly as written
    """))