# 🥜🧈🍇🥪 PB&J Pipeline
## Parse, Better, JSON - The Ultimate RAG Document Processing Pipeline

The **PB&J Pipeline** is a three-stage document processing system that transforms PDFs into clean, structured JSON optimized for RAG (Retrieval-Augmented Generation) applications.

### 🎯 **What is PB&J?**
- **🥜 Peanut (Parse)**: Extract raw content from PDFs using LlamaParse
- **🧈 Butter (Better)**: Enhance markdown structure and readability with AI
- **🍇 Jelly (JSON)**: Convert to clean, searchable JSON for RAG systems
- **🥪 Sandwich**: Complete pipeline orchestrator

---

## 🏗️ **Pipeline Architecture**

### **Stage 1: 🥜 Peanut (Parse)**
- **Tool**: LlamaParse Premium API
- **Input**: PDF documents
- **Output**: Raw markdown with tables and technical content
- **Features**: 
  - Premium mode for complex technical documents
  - Visual marker detection (checkboxes, bullets → TRUE/FALSE)
  - Table structure preservation
  - OCR for faint marks and symbols

### **Stage 2: 🧈 Butter (Better)**
- **Tool**: OpenAI GPT-4
- **Input**: Raw markdown from Peanut stage
- **Output**: Enhanced markdown with improved structure
- **Features**:
  - Better table headers with units (e.g., "Diameter" → "Diameter (mm)")
  - Integrated footnotes and legends
  - Expanded abbreviations
  - Context-aware descriptions
  - Perfect data preservation (no data loss)

### **Stage 3: 🍇 Jelly (JSON)**
- **Tool**: OpenAI GPT-4
- **Input**: Enhanced markdown from Butter stage
- **Output**: Structured JSON optimized for RAG
- **Features**:
  - Searchable keywords and summaries
  - Complete table extraction
  - Technical metadata
  - Data type classification
  - RAG-optimized structure

---

## 📁 **Organized Output Structure**

Each document gets its own organized folder:

```
document_folder/
├── 🥜 Peanut Stage
│   ├── original.pdf                    # Original PDF file
│   └── 01_parsed_markdown/             # Raw LlamaParse output
│       ├── page_1.md
│       └── page_2.md
├── 🧈 Butter Stage  
│   └── 02_enhanced_markdown/           # Enhanced structure
│       ├── page_1.md (saved immediately)
│       └── page_2.md
├── 🍇 Jelly Stage
│   └── 03_cleaned_json/               # Individual page JSONs
│       ├── page_1.json (saved immediately)
│       └── page_2.json
└── 🥜🧈🍇 Final PB&J Output
    ├── final_output.json              # Combined JSON
    ├── document_metadata.json         # Pipeline tracking
    └── pipeline_summary.json          # Complete summary
```

---

## 🚀 **Quick Start**

### **Prerequisites**
```bash
pip install -r requirements.txt
```

**Required API Keys:**
- `LLAMA_CLOUD_API_KEY` - For LlamaParse (Peanut stage)
- `OPENAI_API_KEY` - For enhancement and cleaning (Butter & Jelly stages)

### **Complete PB&J Pipeline**
```python
# Complete pipeline in one line
from pbj import Sandwich

sandwich = Sandwich(use_premium=True, openai_model="gpt-4")
result = sandwich.process("document.pdf")  # or sandwich.make()
print(f"Results saved to: {result['folder_structure']['main_folder']}")
```

```bash
# Or via command line
python3 -m src.pbj.sandwich document.pdf --premium --model gpt-4
```

### **Clean Standardized Interface**

All classes follow the same consistent pattern:

```python
from pbj import Peanut, Butter, Jelly, Sandwich

# 🥜 Peanut (Parse) - Clean interface
peanut = Peanut(use_premium=True)
parsed = peanut.process("document.pdf")        # Main method
parsed = peanut.process_async("document.pdf")  # Async version

# 🧈 Butter (Better) - Clean interface
butter = Butter(model="gpt-4")
enhanced = butter.process(content, "file.md")    # Process content
enhanced = butter.process_file("document.md")    # Process file
docs = butter.process_folder("folder/")          # Process folder
enhanced = butter.process_async(content)         # Async version

# 🍇 Jelly (JSON) - Clean interface
jelly = Jelly(model="gpt-4")
json_data = jelly.process(content, "file.md")   # Process content
json_data = jelly.process_file("document.md")   # Process file
pages = jelly.process_folder("folder/")         # Process folder
json_data = jelly.process_async("file.md")      # Async version

# 🥪 Sandwich (Complete) - Clean interface
sandwich = Sandwich(use_premium=True)
result = sandwich.process("document.pdf")       # Standardized method
result = sandwich.make("document.pdf")          # User-friendly alias
```

### **Fun Themed Aliases**
```python
# For those who like the themed experience
from pbj import Parse, Better, JSON, Pipeline

parser = Parse(use_premium=True)
enhancer = Better(model="gpt-4")
extractor = JSON(model="gpt-4")
pipeline = Pipeline(use_premium=True)

# Same clean interface
parsed = parser.process("document.pdf")
enhanced = enhancer.process(parsed[0].content)
json_data = extractor.process(enhanced.enhanced_content)
complete = pipeline.process("document.pdf")  # or pipeline.make()
```

---

## 🎯 **Interface Design**

### **Consistent Method Patterns**
| Class | Main Method | File Method | Folder Method | Async Method |
|-------|-------------|-------------|---------------|--------------|
| **🥜 Peanut** | `process()` | - | - | `process_async()` |
| **🧈 Butter** | `process()` | `process_file()` | `process_folder()` | `process_async()` |
| **🍇 Jelly** | `process()` | `process_file()` | `process_folder()` | `process_async()` |
| **🥪 Sandwich** | `process()` / `make()` | - | - | - |

### **Clean Design Principles**
- **Consistent**: Same method names across all classes
- **Predictable**: `process()` is always the main method
- **Intuitive**: Method names clearly indicate their purpose
- **Private**: Internal pipeline methods are hidden (prefixed with `_`)
- **No Confusion**: No legacy or duplicate method names

---

## 📂 **Project Structure**

```
pipeline/
├── 🥜🧈🍇 Core Pipeline
│   └── src/pbj/
│       ├── __init__.py               # Clean package imports
│       ├── 🥜 peanut.py              # Parse stage (LlamaParse)
│       ├── 🧈 butter.py              # Better stage (OpenAI)
│       ├── 🍇 jelly.py               # JSON stage (OpenAI)
│       ├── 🥪 sandwich.py            # Complete pipeline
│       └── pantry/                   # Configuration pantry
│           ├── pea.txt               # Peanut system prompt
│           ├── nut.txt               # Peanut user prompt  
│           ├── butter.txt            # Butter enhancement prompt
│           └── jelly.txt             # Jelly extraction prompt
├── 📋 Documentation
│   ├── README.md                     # This file
│   ├── STANDARDIZED_INTERFACE.md     # Detailed interface docs
│   └── requirements.txt              # Dependencies
└── 🧪 Examples
    └── example_pbj.py                # Clean interface examples
```

### **Package Import Structure**
```python
# Main classes (clean, standardized interface)
from pbj import Peanut, Butter, Jelly, Sandwich

# Consistent method names across all classes
peanut.process()      # PDF → Markdown
butter.process()      # Markdown → Enhanced Markdown  
jelly.process()       # Markdown → JSON
sandwich.process()    # Complete pipeline

# Fun aliases (for the adventurous)
from pbj import Parse, Better, JSON, Pipeline
```

---

## 🎉 **Why PB&J?**

1. **🥜 Peanut (Parse)**: The foundation - extracts raw content like peanuts from shells
2. **🧈 Butter (Better)**: The enhancement - makes everything smoother and better
3. **🍇 Jelly (JSON)**: The sweetness - creates the final delicious, structured output
4. **🥪 Sandwich**: The complete meal - orchestrates everything together

Together they make the perfect **PB&J sandwich** - a complete, satisfying solution for document processing! 🥪

### **Clean Interface Benefits**
- **No Confusion**: Only one way to do each operation
- **Consistent**: Same patterns across all classes
- **Predictable**: `process()` always works the same way
- **Future-Proof**: Easy to extend with new classes
- **AI-Friendly**: Simple method names for coding agents
- **Human-Friendly**: Clear, descriptive functionality

---

## 📞 **Support**

The PB&J Pipeline transforms technical PDFs into RAG-ready JSON with:
- **Clean, standardized interface** across all classes
- **Private internal methods** hidden from users
- **Consistent method patterns** for predictable usage
- **Complete pipeline automation** with organized output structure

Ready to make some delicious document processing sandwiches! 🥪
