# 🥜🧈🍇🥪 PB&J Pipeline - Clean Standardized Interface

## Overview

The PB&J Pipeline features a **clean, standardized interface** across all classes. Every class uses consistent method naming patterns for predictable and intuitive usage.

## Standardized Methods

### Core Interface
All classes support these standardized methods:

| Method | Purpose | Available On |
|--------|---------|--------------|
| `process()` | Main processing method | All classes |
| `process_file()` | Process single file | Butter, Jelly |
| `process_folder()` | Process folder of files | Butter, Jelly |
| `process_async()` | Async processing | All classes |

### Class-Specific Methods

#### 🥜 Peanut (Parse)
```python
from pbj import Peanut

peanut = Peanut(use_premium=True)

# Main processing method
result = peanut.process("document.pdf")

# Async processing
result = peanut.process_async("document.pdf")
```

#### 🧈 Butter (Better)
```python
from pbj import Butter

butter = Butter()

# Main processing method
enhanced = butter.process(markdown_content, "file.md")

# File-based processing
enhanced = butter.process_file("document.md")

# Folder-based processing
enhanced_list = butter.process_folder("folder/")

# Async processing
enhanced = butter.process_async(markdown_content, "file.md")
```

#### 🍇 Jelly (JSON)
```python
from pbj import Jelly

jelly = Jelly()

# Main processing method
json_data = jelly.process(markdown_content, "file.md")

# File-based processing
json_data = jelly.process_file("document.md")

# Folder-based processing
json_list = jelly.process_folder("folder/")

# Async processing
json_data = jelly.process_async("document.md")
```

#### 🥪 Sandwich (Complete Pipeline)
```python
from pbj import Sandwich

sandwich = Sandwich(use_premium=True)

# Main processing method
result = sandwich.process("document.pdf")

# User-friendly alias (same as process)
result = sandwich.make("document.pdf")
```

## Usage Examples

### Simple Processing
```python
from pbj import Peanut, Butter, Jelly, Sandwich

# Individual stages with consistent interface
peanut = Peanut()
parsed = peanut.process("document.pdf")

butter = Butter()
enhanced = butter.process(parsed[0].content)

jelly = Jelly()
json_data = jelly.process(enhanced.enhanced_content)

# Complete pipeline
sandwich = Sandwich(use_premium=True)
result = sandwich.process("document.pdf")  # or sandwich.make()
```

### File Processing
```python
from pbj import Butter, Jelly

# Process single files consistently
butter = Butter()
enhanced = butter.process_file("document.md")

jelly = Jelly()
json_data = jelly.process_file("enhanced.md")
```

### Folder Processing
```python
from pbj import Butter, Jelly

# Process folders consistently
butter = Butter()
enhanced_docs = butter.process_folder("markdown_folder/")

jelly = Jelly()
json_pages = jelly.process_folder("enhanced_folder/")
```

### Async Processing
```python
import asyncio
from pbj import Peanut, Butter, Jelly

async def async_pipeline():
    peanut = Peanut()
    parsed = await peanut.process_async("document.pdf")
    
    butter = Butter()
    enhanced = await butter.process_async(parsed[0].content)
    
    jelly = Jelly()
    json_data = await jelly.process_async("enhanced.md")

# Run async pipeline
asyncio.run(async_pipeline())
```

## Fun Aliases

For those who prefer the themed names:

```python
from pbj import Parse, Better, JSON, Pipeline

# Same functionality, themed names
parser = Parse()
enhancer = Better()
extractor = JSON()
pipeline = Pipeline()

# Use with standardized interface
parsed = parser.process("document.pdf")
enhanced = enhancer.process(parsed[0].content)
json_data = extractor.process(enhanced.enhanced_content)
complete = pipeline.process("document.pdf")  # or pipeline.make()
```

## Command Line Interface

The CLI continues to work as before:

```bash
# Complete pipeline
python3 -m src.pbj.sandwich document.pdf

# With premium mode
python3 -m src.pbj.sandwich document.pdf --premium

# With custom model
python3 -m src.pbj.sandwich document.pdf --premium --model gpt-4
```

## Benefits

1. **Clean Interface**: No legacy methods to confuse users
2. **Consistent API**: All classes use the same method naming patterns
3. **Predictable Interface**: `process()`, `process_file()`, `process_folder()` work the same everywhere
4. **AI-Friendly**: Simple method names for coding agents
5. **Human-Friendly**: Clear, descriptive method names
6. **Future-Proof**: Standardized interface makes adding new classes easier
7. **Intuitive**: Method names clearly indicate their purpose

## Method Summary Table

| Class | Main Method | File Method | Folder Method | Async Method |
|-------|-------------|-------------|---------------|--------------|
| **🥜 Peanut** | `process()` | - | - | `process_async()` |
| **🧈 Butter** | `process()` | `process_file()` | `process_folder()` | `process_async()` |
| **🍇 Jelly** | `process()` | `process_file()` | `process_folder()` | `process_async()` |
| **🥪 Sandwich** | `process()` / `make()` | - | - | - |

## Interface Consistency

- **All classes** have `process()` as their main method
- **Butter & Jelly** have file and folder processing variants
- **All classes** have async processing capabilities  
- **Sandwich** offers both `process()` and `make()` (same functionality)
- **Method signatures** are consistent across similar operations
- **Internal pipeline methods** are private (prefixed with `_`)