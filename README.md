# SuproTools

A powerful Python CLI toolkit for developers — file manager, code formatter, and system utilities.

## Features

- **File Manager** — Find duplicates, organize files by extension, display directory trees
- **Code Analyzer** — Count lines of code, analyze entire projects, detect languages
- **System Utils** — System information, function benchmarking
- **Zero Dependencies** — Pure Python, no external packages needed

## Installation

```bash
pip install supro-tools
```

## Usage

### Find duplicate files
```bash
supro-tools find-duplicates /path/to/directory
```

### Organize files by extension
```bash
supro-tools organize /path/to/directory
```

### Show directory tree
```bash
supro-tools tree /path/to/directory --depth 3
```

### Count lines in a file
```bash
supro-tools count-lines myfile.py
```

### Analyze entire project
```bash
supro-tools analyze /path/to/project
```

### System information
```bash
supro-tools sysinfo
```

## API Usage

```python
from supro_tools import FileManager, CodeFormatter, SystemUtils

# Find duplicates
duplicates = FileManager.find_duplicates("/path/to/dir")

# Analyze project
stats = CodeFormatter.analyze_project("/path/to/project")
print(stats["languages"])

# Get system info
info = SystemUtils.get_system_info()
print(info)
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**SuproCode** — [GitHub](https://github.com/suprocode54)
