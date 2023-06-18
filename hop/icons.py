from collections import defaultdict

icon_mapping = {
    ".py": ":snake:",
    ".ipynb": ":snake:",
    ".rs": ":crab:",
    ".ts": "",
    ".tsx": "",
    ".js": "",
    ".jsx": "",
    ".md": ":blue_book:",
    ".txt": ":book:",
    ".yaml": ":closed_book:",
    ".yml": ":closed_book:",
    ".html": ":globe_showing_americas:",
    ".css": ":paintbrush:",
    ".exe": ":floppy_disk:",
    ".cc": "",
    ".cpp": "",
    ".jar": ":robot:",
    ".java": ":robot:",
}

icons = defaultdict(lambda x: ":herb:", icon_mapping)