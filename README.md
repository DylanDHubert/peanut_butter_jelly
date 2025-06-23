# PB&J Pipeline

A Python RAG document processing pipeline that combines PDF parsing, markdown enhancement, and JSON extraction.

## API Keys

- **LlamaParse:** https://cloud.llamaindex.ai/ (sign up and get your API key)
- **OpenAI:** https://platform.openai.com/account/api-keys (sign up and get your API key)

## Quick Start

```python
from pbj.sandwich import Sandwich

# Create pipeline (automatically loads configuration)
sandwich = Sandwich()

# Process a PDF through the complete pipeline
result = sandwich.process("document.pdf")
print(f"Output saved to: {result['pipeline_info']['document_folder']}")
```

## Command Line Usage

You can also run the pipeline from the command line:

```bash
python -m pbj.sandwich document.pdf
```

Options:
- `--premium` : Use LlamaParse premium mode
- `--model MODEL` : Specify OpenAI model for enhancement/cleaning (e.g., `gpt-4`)

Example:
```bash
python -m pbj.sandwich document.pdf --premium --model gpt-4
```

## Configuration

The pipeline supports multiple configuration sources (priority order):

1. Environment Variables (highest priority)
2. Configuration Files (`config.yaml`, `config.json`)
3. `.env` Files (fallback)
4. Default Values (lowest priority)

### Environment Variables
```bash
export LLAMAPARSE_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
export PBJ_OUTPUT_DIR="uploads/processed_docs"
export PBJ_PREMIUM_MODE="true"
```

### Configuration File (config.yaml)
```yaml
llamaparse_api_key: "your_llamaparse_api_key_here"
openai_api_key: "your_openai_api_key_here"
output_base_dir: "my_project_documents"
use_premium_mode: false
openai_model: "gpt-4"
```

### Programmatic Configuration
```python
from pbj.config import create_config
from pbj.sandwich import Sandwich

config = create_config(
    output_base_dir="uploads/processed",
    use_premium_mode=True,
    openai_model="gpt-4-turbo"
)

sandwich = Sandwich(config=config)
result = sandwich.process("document.pdf")
```

## Pipeline Stages

### Stage 1: Peanut (Parse)
PDF processing with LlamaParse
```python
from pbj.peanut import Peanut

peanut = Peanut(use_premium=True)
parsed_docs = peanut.process("document.pdf")
```

### Stage 2: Butter (Better)
Markdown enhancement with OpenAI
```python
from pbj.butter import Butter

butter = Butter(model="gpt-4")
enhanced_docs = butter.process_document_folder("document_folder")
```

### Stage 3: Jelly (JSON)
Data cleaning and JSON extraction
```python
from pbj.jelly import Jelly

jelly = Jelly(model="gpt-4")
processed_pages = jelly.process_document_folder("document_folder")
```

## Output Structure

```
processed_documents/
└── document_20241201_143022/
    ├── original.pdf
    ├── document_metadata.json
    ├── pipeline_summary.json
    ├── final_output.json
    ├── 01_parsed_markdown/
    │   ├── page_1.md
    │   └── page_2.md
    ├── 02_enhanced_markdown/
    │   ├── page_1.md
    │   └── page_2.md
    └── 03_cleaned_json/
        ├── page_1.json
        └── page_2.json
```

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `output_base_dir` | `"processed_documents"` | Base directory for all output |
| `create_timestamped_folders` | `true` | Create timestamped folders for each run |
| `use_premium_mode` | `false` | Use LlamaParse Premium mode |
| `openai_model` | `"gpt-4"` | OpenAI model for enhancement/cleaning |
| `enable_verbose_logging` | `true` | Show detailed processing logs |
| `page_separator` | `"\n---\n"` | Page separator in markdown output |
| `max_timeout` | `180` | Maximum processing time in seconds |

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.8+
- LlamaParse API key
- OpenAI API key (for enhancement and cleaning stages)

## Use Cases

### Web Application
```python
config = create_config(
    output_base_dir="uploads/processed_docs",
    create_timestamped_folders=True,
    use_premium_mode=True,
    enable_verbose_logging=False
)
```

### CLI Tool
```python
config = create_config(
    output_base_dir=".",
    create_timestamped_folders=False,
    use_premium_mode=False,
    enable_verbose_logging=True
)
```

### Library Integration
```python
config = create_config(
    output_base_dir="/tmp/pbj_processing",
    create_timestamped_folders=True,
    save_intermediate_files=False
)
```

## Examples

See `example.py` for comprehensive configuration examples.
 