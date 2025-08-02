# chunker.py

import os
import re

def chunk_python_code(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()

    # Split code by class and function definitions
    pattern = re.compile(r'(^\s*(def|class)\s+.*?:)', re.MULTILINE)
    matches = list(pattern.finditer(code))

    if not matches:
        return [code]  # Return entire file as single chunk

    chunks = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(code)
        chunks.append(code[start:end].strip())

    return chunks


def chunk_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    chunks = []
    current_chunk = []
    for line in lines:
        if line.strip() == "" and current_chunk:
            chunks.append("".join(current_chunk).strip())
            current_chunk = []
        else:
            current_chunk.append(line)

    if current_chunk:
        chunks.append("".join(current_chunk).strip())

    return chunks


def chunk_generic_code(file_path):
    """Generic chunking for various code files (JS, TS, HTML, CSS, etc.)"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # For code files, try to split by logical blocks
    # Look for function/class declarations, export/import statements, etc.
    patterns = [
        r'(^\s*(function|class|const|let|var|export|import)\s+.*?:)',  # JS/TS
        r'(^\s*<[^>]*>.*)',  # HTML tags
        r'(^\s*[.#][a-zA-Z].*\{)',  # CSS selectors
        r'(^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*[:=])',  # General assignments
    ]
    
    for pattern in patterns:
        matches = list(re.finditer(pattern, content, re.MULTILINE))
        if matches:
            chunks = []
            for i in range(len(matches)):
                start = matches[i].start()
                end = matches[i+1].start() if i+1 < len(matches) else len(content)
                chunk = content[start:end].strip()
                if chunk:  # Only add non-empty chunks
                    chunks.append(chunk)
            
            if chunks:
                return chunks
    
    # Fallback: split by double newlines or return entire content
    if '\n\n' in content:
        return [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
    
    return [content] if content.strip() else []
