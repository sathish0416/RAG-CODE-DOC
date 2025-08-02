import os
import shutil
import stat
from git import Repo

SUPPORTED_EXTENSIONS = ['.py', '.txt', '.md', '.json', '.yaml', '.yml' , '.js', '.ts', '.html', '.css','.java', '.c', '.cpp','.dart','.php']

def handle_remove_readonly(func, path, exc_info):
    """Allow force deletion of read-only or locked files (Windows fix)."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(repo_url, clone_dir="repo"):
    if os.path.exists(clone_dir):
        print(f"[INFO] Attempting to remove existing directory: {clone_dir}")
        shutil.rmtree(clone_dir, onerror=handle_remove_readonly)
        print(f"[INFO] Removed: {clone_dir}")
    
    print(f"[INFO] Cloning from {repo_url} ...")
    Repo.clone_from(repo_url, clone_dir)
    print(f"[INFO] Cloned into {clone_dir}")
    return clone_dir

def get_code_files(base_dir="repo"):
    code_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                code_files.append(os.path.join(root, file))
    print(f"[INFO] Found {len(code_files)} supported files.")
    return code_files