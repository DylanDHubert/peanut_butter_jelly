#!/usr/bin/env python3
"""
Complete RAG Document Processing Pipeline
========================================

FULL 3-STAGE PIPELINE WITH ORGANIZED FOLDER STRUCTURE:
1. PDF Processing (LlamaParse) → 01_parsed_markdown/
2. Markdown Enhancement (OpenAI) → 02_enhanced_markdown/ 
3. Data Cleaning (OpenAI) → 03_cleaned_json/ + final_output.json

FOLDER STRUCTURE PER DOCUMENT:
document_folder/
├── original.pdf                    # Original PDF file
├── document_metadata.json          # Pipeline tracking metadata
├── final_output.json              # Final combined JSON output
├── 01_parsed_markdown/             # Stage 1: Raw LlamaParse output
│   ├── page_1.md
│   └── page_2.md
├── 02_enhanced_markdown/           # Stage 2: Enhanced with better structure
│   ├── page_1.md
│   └── page_2.md
└── 03_cleaned_json/               # Stage 3: Individual page JSON files
    ├── page_1.json
    └── page_2.json
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# IMPORT OUR PIPELINE MODULES
from pdf_processor import PDFProcessor
from markdown_enhancer import MarkdownEnhancer  
from data_cleaner import DataCleaner

def run_complete_pipeline(
    pdf_path: str, 
    output_dir: Optional[str] = None,
    use_premium: bool = False,
    openai_model: str = "gpt-4"
) -> Dict[str, Any]:
    """
    Run the complete 3-stage RAG document processing pipeline
    
    Args:
        pdf_path: Path to the PDF file to process
        output_dir: Optional custom output directory
        use_premium: Whether to use LlamaParse Premium mode
        openai_model: OpenAI model for enhancement and cleaning
        
    Returns:
        Dict[str, Any]: Complete pipeline results and folder structure info
    """
    
    print("🚀 STARTING COMPLETE RAG DOCUMENT PROCESSING PIPELINE")
    print("=" * 60)
    
    pipeline_start = datetime.now()
    
    try:
        # STAGE 1: PDF PROCESSING WITH LLAMAPARSE
        print("\n📄 STAGE 1: PDF PROCESSING WITH LLAMAPARSE")
        print("-" * 40)
        
        processor = PDFProcessor(use_premium=use_premium)
        parsed_docs = processor.parse_pdf(pdf_path)
        stage1_result = processor.save_parsed_documents(parsed_docs, output_dir, pdf_path)
        
        document_folder = stage1_result["main_folder"]
        print(f"✅ STAGE 1 COMPLETE - Document folder: {document_folder}")
        
        # STAGE 2: MARKDOWN ENHANCEMENT
        print("\n🔧 STAGE 2: MARKDOWN ENHANCEMENT WITH OPENAI")
        print("-" * 40)
        
        enhancer = MarkdownEnhancer(model=openai_model)
        enhanced_docs = enhancer.enhance_document_folder(document_folder)
        
        print(f"✅ STAGE 2 COMPLETE - Enhanced {len(enhanced_docs)} documents")
        
        # STAGE 3: DATA CLEANING AND JSON EXTRACTION
        print("\n🧹 STAGE 3: DATA CLEANING AND JSON EXTRACTION")
        print("-" * 40)
        
        cleaner = DataCleaner(model=openai_model)
        processed_pages = cleaner.process_document_folder(document_folder)
        
        print(f"✅ STAGE 3 COMPLETE - Processed {len(processed_pages)} pages")
        
        # PIPELINE COMPLETION SUMMARY
        pipeline_end = datetime.now()
        total_time = (pipeline_end - pipeline_start).total_seconds()
        
        print("\n🎉 COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📁 Document Folder: {document_folder}")
        print(f"⏱️  Total Processing Time: {total_time:.2f} seconds")
        print(f"📄 Pages Processed: {len(processed_pages)}")
        print(f"📊 Tables Extracted: {sum(len(page.tables) for page in processed_pages)}")
        print(f"🔍 Unique Keywords: {len(set().union(*[page.keywords for page in processed_pages])) if processed_pages else 0}")
        
        # CREATE FINAL PIPELINE SUMMARY
        pipeline_summary = {
            "pipeline_info": {
                "completed_at": pipeline_end.isoformat(),
                "total_processing_time_seconds": total_time,
                "pdf_source": pdf_path,
                "document_folder": document_folder,
                "llamaparse_mode": "premium" if use_premium else "standard",
                "openai_model": openai_model
            },
            "stage_results": {
                "stage_1_pdf_processing": {
                    "pages_parsed": len(parsed_docs),
                    "folder": stage1_result["parsed_markdown_folder"]
                },
                "stage_2_enhancement": {
                    "documents_enhanced": len(enhanced_docs),
                    "folder": str(Path(document_folder) / "02_enhanced_markdown")
                },
                "stage_3_cleaning": {
                    "pages_processed": len(processed_pages),
                    "individual_json_folder": str(Path(document_folder) / "03_cleaned_json"),
                    "final_output": str(Path(document_folder) / "final_output.json")
                }
            },
            "data_summary": {
                "total_pages": len(processed_pages),
                "total_tables": sum(len(page.tables) for page in processed_pages),
                "unique_keywords": len(set().union(*[page.keywords for page in processed_pages])) if processed_pages else 0,
                "page_titles": [page.title for page in processed_pages]
            },
            "folder_structure": {
                "main_folder": document_folder,
                "original_pdf": str(Path(document_folder) / Path(pdf_path).name),
                "metadata": str(Path(document_folder) / "document_metadata.json"),
                "final_output": str(Path(document_folder) / "final_output.json"),
                "subfolders": {
                    "parsed_markdown": str(Path(document_folder) / "01_parsed_markdown"),
                    "enhanced_markdown": str(Path(document_folder) / "02_enhanced_markdown"),
                    "cleaned_json": str(Path(document_folder) / "03_cleaned_json")
                }
            }
        }
        
        # SAVE PIPELINE SUMMARY
        summary_file = Path(document_folder) / "pipeline_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(pipeline_summary, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Pipeline Summary Saved: {summary_file}")
        
        return pipeline_summary
        
    except Exception as e:
        print(f"\n❌ PIPELINE FAILED: {e}")
        raise


def main():
    """Command line interface for the complete pipeline"""
    
    if len(sys.argv) < 2:
        print("Usage: python pipeline_complete.py <pdf_path> [--premium] [--model MODEL]")
        print("\nExamples:")
        print("  python pipeline_complete.py test.pdf")
        print("  python pipeline_complete.py document.pdf --premium")
        print("  python pipeline_complete.py report.pdf --premium --model gpt-4")
        print("\nOptions:")
        print("  --premium    Use LlamaParse Premium mode (better quality, costs more)")
        print("  --model      OpenAI model for enhancement/cleaning (default: gpt-4)")
        sys.exit(1)
    
    # PARSE COMMAND LINE ARGUMENTS
    pdf_path = sys.argv[1]
    use_premium = "--premium" in sys.argv
    
    # GET MODEL ARGUMENT
    openai_model = "gpt-4"  # DEFAULT
    if "--model" in sys.argv:
        model_index = sys.argv.index("--model")
        if model_index + 1 < len(sys.argv):
            openai_model = sys.argv[model_index + 1]
    
    # VALIDATE PDF FILE
    if not Path(pdf_path).exists():
        print(f"❌ ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.lower().endswith('.pdf'):
        print(f"❌ ERROR: File must be a PDF: {pdf_path}")
        sys.exit(1)
    
    # SHOW CONFIGURATION
    print("PIPELINE CONFIGURATION:")
    print(f"  📄 PDF File: {pdf_path}")
    print(f"  🔧 LlamaParse Mode: {'Premium' if use_premium else 'Standard'}")
    print(f"  🤖 OpenAI Model: {openai_model}")
    print()
    
    try:
        # RUN COMPLETE PIPELINE
        result = run_complete_pipeline(
            pdf_path=pdf_path,
            use_premium=use_premium,
            openai_model=openai_model
        )
        
        print(f"\n🎯 SUCCESS! Check your results in: {result['folder_structure']['main_folder']}")
        
    except Exception as e:
        print(f"\n💥 PIPELINE ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 