#!/usr/bin/env python3
"""
SuproTools - A powerful Python CLI toolkit for developers.
File manager, code formatter, and system utilities.
"""

import argparse
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path


VERSION = "1.0.0"
AUTHOR = "SuproCode"


class FileManager:
    """Advanced file management utilities."""

    @staticmethod
    def find_duplicates(directory: str) -> list:
        """Find duplicate files in a directory based on file size and name."""
        seen = {}
        duplicates = []

        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    file_size = os.path.getsize(filepath)
                    key = (filename, file_size)
                    if key in seen:
                        duplicates.append((filepath, seen[key]))
                    else:
                        seen[key] = filepath
                except OSError:
                    continue

        return duplicates

    @staticmethod
    def organize_by_extension(directory: str) -> dict:
        """Organize files in a directory by their extensions."""
        organized = {}
        for item in Path(directory).iterdir():
            if item.is_file():
                ext = item.suffix.lower() if item.suffix else "no_extension"
                if ext not in organized:
                    organized[ext] = []
                organized[ext].append(str(item))
        return organized

    @staticmethod
    def get_dir_tree(directory: str, max_depth: int = 3, prefix: str = "") -> str:
        """Generate a visual tree structure of a directory."""
        result = []
        path = Path(directory)
        
        if not path.exists():
            return f"Error: Directory '{directory}' does not exist."

        def _build_tree(p, current_prefix, depth):
            if depth > max_depth:
                return
            items = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                result.append(f"{current_prefix}{connector}{item.name}")
                if item.is_dir() and depth < max_depth:
                    extension = "    " if is_last else "│   "
                    _build_tree(item, current_prefix + extension, depth + 1)

        result.append(path.name + "/")
        _build_tree(path, prefix, 0)
        return "\n".join(result)


class CodeFormatter:
    """Code formatting and analysis utilities."""

    @staticmethod
    def count_lines(filepath: str) -> dict:
        """Count lines of code, comments, and blank lines in a file."""
        total = 0
        blank = 0
        comments = 0
        code = 0

        comment_symbols = ["#", "//", "/*", "*/", "--", ";", "%"]

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    total += 1
                    stripped = line.strip()
                    if not stripped:
                        blank += 1
                    elif any(stripped.startswith(sym) for sym in comment_symbols):
                        comments += 1
                    else:
                        code += 1
        except Exception as e:
            return {"error": str(e)}

        return {
            "total": total,
            "code": code,
            "comments": comments,
            "blank": blank,
            "file": filepath,
        }

    @staticmethod
    def analyze_project(directory: str) -> dict:
        """Analyze an entire project directory."""
        stats = {
            "files": 0,
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "languages": {},
        }

        extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".rs": "Rust",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP",
            ".html": "HTML",
            ".css": "CSS",
            ".json": "JSON",
            ".yaml": "YAML",
            ".md": "Markdown",
            ".sh": "Shell",
        }

        skip_dirs = {".git", "node_modules", "__pycache__", "venv", ".venv", "dist", "build"}

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for filename in files:
                filepath = os.path.join(root, filename)
                ext = os.path.splitext(filename)[1].lower()
                
                if ext in extensions:
                    lang = extensions[ext]
                    if lang not in stats["languages"]:
                        stats["languages"][lang] = {"files": 0, "lines": 0}
                    stats["languages"][lang]["files"] += 1
                    
                    result = CodeFormatter.count_lines(filepath)
                    if "error" not in result:
                        stats["files"] += 1
                        stats["total_lines"] += result["total"]
                        stats["code_lines"] += result["code"]
                        stats["comment_lines"] += result["comments"]
                        stats["blank_lines"] += result["blank"]
                        stats["languages"][lang]["lines"] += result["total"]

        return stats


class SystemUtils:
    """System utility functions."""

    @staticmethod
    def get_system_info() -> dict:
        """Get basic system information."""
        import platform

        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
        }

    @staticmethod
    def benchmark(func, *args, iterations: int = 1000) -> dict:
        """Benchmark a function execution time."""
        start = time.perf_counter()
        for _ in range(iterations):
            func(*args)
        end = time.perf_counter()

        total_time = end - start
        avg_time = total_time / iterations

        return {
            "function": func.__name__,
            "iterations": iterations,
            "total_time": round(total_time, 6),
            "avg_time": round(avg_time, 8),
            "ops_per_second": round(1 / avg_time, 2) if avg_time > 0 else 0,
        }


def main():
    parser = argparse.ArgumentParser(
        prog="supro-tools",
        description="SuproTools - A powerful CLI toolkit for developers",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # find-duplicates command
    dup_parser = subparsers.add_parser("find-duplicates", help="Find duplicate files")
    dup_parser.add_argument("directory", help="Directory to scan")

    # organize command
    org_parser = subparsers.add_parser("organize", help="Organize files by extension")
    org_parser.add_argument("directory", help="Directory to organize")

    # tree command
    tree_parser = subparsers.add_parser("tree", help="Show directory tree")
    tree_parser.add_argument("directory", help="Directory path")
    tree_parser.add_argument("--depth", type=int, default=3, help="Max depth")

    # count-lines command
    count_parser = subparsers.add_parser("count-lines", help="Count lines in a file")
    count_parser.add_argument("file", help="File to analyze")

    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze project code")
    analyze_parser.add_argument("directory", help="Project directory")

    # sysinfo command
    subparsers.add_parser("sysinfo", help="Show system information")

    args = parser.parse_args()

    if args.command == "find-duplicates":
        dups = FileManager.find_duplicates(args.directory)
        if dups:
            print(f"Found {len(dups)} duplicate(s):")
            for dup, original in dups:
                print(f"  {dup} (duplicate of {original})")
        else:
            print("No duplicates found.")

    elif args.command == "organize":
        result = FileManager.organize_by_extension(args.directory)
        for ext, files in sorted(result.items()):
            print(f"\n{ext}:")
            for f in files:
                print(f"  {f}")

    elif args.command == "tree":
        tree = FileManager.get_dir_tree(args.directory, args.depth)
        print(tree)

    elif args.command == "count-lines":
        result = CodeFormatter.count_lines(args.file)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"File: {result['file']}")
            print(f"  Total lines:  {result['total']}")
            print(f"  Code lines:   {result['code']}")
            print(f"  Comments:     {result['comments']}")
            print(f"  Blank lines:  {result['blank']}")

    elif args.command == "analyze":
        result = CodeFormatter.analyze_project(args.directory)
        print(f"Project Analysis: {args.directory}")
        print(f"  Total files:      {result['files']}")
        print(f"  Total lines:      {result['total_lines']}")
        print(f"  Code lines:       {result['code_lines']}")
        print(f"  Comment lines:    {result['comment_lines']}")
        print(f"  Blank lines:      {result['blank_lines']}")
        print(f"\nLanguages:")
        for lang, data in sorted(result["languages"].items(), key=lambda x: x[1]["lines"], reverse=True):
            print(f"  {lang}: {data['files']} files, {data['lines']} lines")

    elif args.command == "sysinfo":
        info = SystemUtils.get_system_info()
        for key, value in info.items():
            print(f"  {key}: {value}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
