import os
import json
import re

def extract_h1(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        return match.group(1) if match else None

def create_markdown_index(docs_dir, output_file):
    index = {}
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, docs_dir)
                h1_title = extract_h1(file_path)
                if h1_title:
                    index[relative_path] = h1_title

    with open(output_file, 'w') as f:
        json.dump(index, f, indent=2)