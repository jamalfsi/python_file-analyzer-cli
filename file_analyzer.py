import os      # Work with files and folders
import hashlib # For file hashing (checks for duplicates)
from functools import wraps
import time

# ======= Decorators =======

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"⏱️ {func.__name__} took {round(time.time()-start, 2)}s")
        return result
    return wrapper

# ======= MAIN CLASS =======

class FileAnalyzer:
    """
    FileAnalyzer scans, reports, and finds duplicates in directories.

    Methods:
      - scan(): Walk through all files and subfolders
      - get_size_report(): Report file sizes
      - find_duplicates(): Find duplicate files by content
      - print_summary(): Pretty print info
    """

    def __init__(self, root_path):
        self.root_path = root_path
        self.file_info = []    # List for details about each file

    @timer
    def scan(self):
        """
        Recursively scan directory, collect info.
        """
        for folder, subfolders, files in os.walk(self.root_path):
            for f in files:
                path = os.path.join(folder, f)
                try:
                    size = os.path.getsize(path)
                    mtime = os.path.getmtime(path)
                    typ = os.path.splitext(f)[1]
                    self.file_info.append({
                        "path": path,
                        "size": size,
                        "type": typ,
                        "modified": mtime
                    })
                except Exception as e:
                    print(f"❌ Could not access {path}: {e}")

    def get_size_report(self):
        """
        Summarize file sizes by type.
        """
        report = {}
        for file in self.file_info:
            typ = file["type"]
            report[typ] = report.get(typ, 0) + file["size"]
        return report

    @timer
    def find_duplicates(self):
        """
        Find duplicate files using hash.
        """
        hash_map = {}
        duplicates = []
        for file in self.file_info:
            try:
                with open(file["path"], "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in hash_map:
                    duplicates.append((file["path"], hash_map[file_hash]))
                else:
                    hash_map[file_hash] = file["path"]
            except Exception as e:
                print(f"❌ Error hashing {file['path']}: {e}")
        return duplicates

    def print_summary(self):
        """
        Print summary: total files, size by type, duplicates.
        """
        print(f"\n🔎 Directory: {self.root_path}")
        print(f"Total files: {len(self.file_info)}")
        sizes = self.get_size_report()
        print("Size by type:")
        for typ, size in sizes.items():
            print(f" - {typ or '[none]'}: {size/1024:.2f} KB")
