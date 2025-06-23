# 🥜🧈🍇 PB&J Pipeline
## Parse, Better, JSON - The Ultimate RAG Document Processing Pipeline

The **PB&J Pipeline** is a three-stage document processing system that transforms PDFs into clean, structured JSON optimized for RAG (Retrieval-Augmented Generation) applications.

### 🎯 **What is PB&J?**
- **🥜 Peanut (Parse)**: Extract raw content from PDFs using LlamaParse
- **🧈 Butter (Better)**: Enhance markdown structure and readability with AI
- **🍇 Jelly (JSON)**: Convert to clean, searchable JSON for RAG systems

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
result = sandwich.make("document.pdf")
print(f"Results saved to: {result['folder_structure']['main_folder']}")
```

```bash
# Or via command line
python3 -m pbj.sandwich document.pdf --premium --model gpt-4
```

### **Stage-by-Stage Execution**

#### **🥜 Peanut Only (Parse)**
```python
from pbj import Peanut

peanut = Peanut(use_premium=True)
parsed_docs = peanut.pdf2md("document.pdf")
result = peanut.save_parsed_documents(parsed_docs, source_pdf_path="document.pdf")
```

#### **🧈 Butter Only (Better)**
```python
from pbj import Butter

butter = Butter(model="gpt-4")
enhanced_docs = butter.enhance_document_folder("data/document_folder")
```

#### **🍇 Jelly Only (JSON)**
```python
from pbj import Jelly

jelly = Jelly(model="gpt-4")
processed_pages = jelly.process_document_folder("data/document_folder")
```

### **Individual Method Usage**
```python
from pbj import Peanut, Butter, Jelly

# Stage 1: Parse PDF to markdown
peanut = Peanut(use_premium=True)
parsed_docs = peanut.pdf2md("document.pdf")

# Stage 2: Enhance markdown structure  
butter = Butter(model="gpt-4")
enhanced_doc = butter.md2md(parsed_docs[0].content, "document.md")

# Stage 3: Extract structured JSON
jelly = Jelly(model="gpt-4")
json_result = jelly.md2json(enhanced_doc.enhanced_content, "document.md")
```

---

## 🛠️ **Configuration**

### **Peanut (Parse) Configuration**
- **Files**: `config/pdf_system_prompt.txt`, `config/pdf_user_prompt.txt`
- **Settings**: Premium mode, OCR enabled, HTML tables, visual marker detection

### **Butter (Better) Configuration**
- **File**: `config/markdown_enhancement_prompt.txt`
- **Focus**: Structure improvement while preserving all data

### **Jelly (JSON) Configuration**
- **File**: `config/data_cleaning_prompt.txt`
- **Focus**: RAG optimization and searchable JSON structure

---

## 📊 **Pipeline Features**

### **🔄 Immediate Saves**
- **Peanut**: Saves after complete PDF parsing
- **Butter**: Saves after each page enhancement
- **Jelly**: Saves after each page processing + final combined output

### **📈 Data Integrity**
- ✅ **Zero data loss**: Every table row preserved exactly
- ✅ **Numerical fidelity**: All measurements and values identical
- ✅ **Boolean integrity**: TRUE/FALSE values from visual markers
- ✅ **Complete tracking**: Metadata tracks every stage

### **🎯 RAG Optimization**
- Searchable keywords and summaries
- Technical terminology extraction
- Table structure with metadata
- Data type classification
- Measurement units standardization

---

## 🧪 **Testing**

### **Test Complete Pipeline**
```bash
python3 test_new_structure.py
```

### **Continue from Specific Stage**
```bash
# Continue from Butter stage (if Peanut already completed)
python3 continue_pipeline.py data/document_folder
```

---

## 📝 **File Structure**

```
🥜🧈🍇 PB&J Pipeline/
├── src/pbj/                       # Main PB&J package
│   ├── __init__.py               # Package imports
│   ├── 🥜 peanut.py              # Parse stage (LlamaParse)
│   ├── 🧈 butter.py              # Better stage (OpenAI)
│   ├── 🍇 jelly.py               # JSON stage (OpenAI)
│   ├── 🥪 sandwich.py            # Complete pipeline
│   └── pantry/                   # Configuration pantry
│       ├── pea.txt               # Peanut system prompt
│       ├── nut.txt               # Peanut user prompt  
│       ├── butter.txt            # Butter enhancement prompt
│       └── jelly.txt             # Jelly extraction prompt
├── 📋 Documentation
│   ├── README.md                 # This file
│   └── requirements.txt          # Dependencies
└── 🧪 Testing
    └── test_pbj.py               # Package structure test
```

### **Package Import Structure**
```python
# Main classes (fun names for humans)
from pbj import Peanut, Butter, Jelly, Sandwich

# Simple method names (for coding agents)
peanut.pdf2md()    # PDF → Markdown
butter.md2md()     # Markdown → Enhanced Markdown  
jelly.md2json()    # Markdown → JSON
sandwich.make()    # Complete pipeline

# Fun aliases (for the adventurous)
from pbj import Parse, Better, JSON, Pipeline
```

---

## 🎉 **Why PB&J?**

1. **🥜 Peanut (Parse)**: The foundation - extracts raw content like peanuts from shells
2. **🧈 Butter (Better)**: The enhancement - makes everything smoother and better
3. **🍇 Jelly (JSON)**: The sweetness - creates the final delicious, structured output

Together they make the perfect **PB&J sandwich** - a complete, satisfying solution for document processing! 🥪

---

## 📞 **Support**

The PB&J Pipeline transforms technical PDFs into RAG-ready JSON with:
- **6 tables extracted** from test document
- **19 unique keywords** generated
- **4 pages processed** in organized structure
- **Perfect data preservation** throughout all stages

**Made with ❤️ and a love for good sandwiches** 🥜🧈🍇
