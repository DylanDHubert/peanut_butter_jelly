#!/usr/bin/env python3
"""
🥪 Sandwich - Complete PB&J Pipeline
===================================

FULL 3-STAGE PIPELINE WITH ORGANIZED FOLDER STRUCTURE:
1. PDF Processing (LlamaParse) → 01_parsed_markdown/
2. Markdown Enhancement (OpenAI) → 02_enhanced_markdown/ 
3. Data Cleaning (OpenAI) → 03_cleaned_json/ + final_output.json

FOLDER STRUCTURE PER DOCUMENT:
document_folder/
├── original.pdf                    # Original PDF file
├── document_metadata.json          # Pipeline tracking metadata
├── final_output.json               # Final combined JSON output
├── 01_parsed_markdown/             # Stage 1: Raw LlamaParse output
│   ├── page_1.md
│   └── page_2.md
├── 02_enhanced_markdown/           # Stage 2: Enhanced with better structure
│   ├── page_1.md
│   └── page_2.md
└── 03_cleaned_json/                # Stage 3: Individual page JSON files
    ├── page_1.json
    └── page_2.json
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# IMPORT OUR PB&J PIPELINE MODULES
from .peanut import Peanut
from .butter import Butter
from .jelly import Jelly
from .config import PipelineConfig, create_config

class Sandwich:
    """
    🥪 Sandwich - Complete PB&J Pipeline Orchestrator
    
    Combines Peanut (Parse), Butter (Better), and Jelly (JSON) 
    into one delicious document processing sandwich.
    """
    
    def __init__(self, config: Optional[PipelineConfig] = None, use_premium: bool = False, openai_model: str = "gpt-4"):
        """
        Initialize the Sandwich with pipeline configuration
        
        Args:
            config: PipelineConfig object with all settings
            use_premium: Whether to use LlamaParse Premium mode (overrides config)
            openai_model: OpenAI model for enhancement and cleaning (overrides config)
        """
        # LOAD CONFIGURATION - PRIORITY: config parameter > individual parameters > defaults
        if config:
            self.config = config
            # OVERRIDE CONFIG WITH PROVIDED PARAMETERS
            if use_premium:
                self.config.use_premium_mode = use_premium
            if openai_model:
                self.config.openai_model = openai_model
        else:
            # CREATE CONFIG WITH PROVIDED PARAMETERS
            self.config = create_config(
                use_premium_mode=use_premium,
                openai_model=openai_model
            )
        
        # INITIALIZE OUR PB&J COMPONENTS WITH CONFIGURATION
        self.peanut = Peanut(config=self.config)
        self.butter = Butter(model=self.config.openai_model, config=self.config)
        self.jelly = Jelly(model=self.config.openai_model, config=self.config)
    
    def process(self, pdf_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        🥪 Process PDF → Complete JSON pipeline
        Main Sandwich processing method - runs the complete 3-stage PB&J pipeline
        """
        print("🥪 STARTING COMPLETE PB&J PIPELINE")
        print("=" * 60)
        
        pipeline_start = datetime.now()
        
        try:
            # STAGE 1: PEANUT (PARSE) - PDF PROCESSING WITH LLAMAPARSE
            print("\n🥜 STAGE 1: PEANUT (PARSE) - PDF PROCESSING")
            print("-" * 40)
            
            parsed_docs = self.peanut.process(pdf_path)
            stage1_result = self.peanut.save_parsed_documents(parsed_docs, output_dir, pdf_path)
            
            document_folder = stage1_result["main_folder"]
            print(f"✅ PEANUT COMPLETE - Document folder: {document_folder}")
            
            # STAGE 2: BUTTER (BETTER) - MARKDOWN ENHANCEMENT
            print("\n🧈 STAGE 2: BUTTER (BETTER) - MARKDOWN ENHANCEMENT")
            print("-" * 40)
            
            enhanced_docs = self.butter._process_document_folder(document_folder)
            
            print(f"✅ BUTTER COMPLETE - Enhanced {len(enhanced_docs)} documents")
            
            # STAGE 3: JELLY (JSON) - DATA CLEANING AND JSON EXTRACTION
            print("\n🍇 STAGE 3: JELLY (JSON) - DATA EXTRACTION")
            print("-" * 40)
            
            processed_pages = self.jelly._process_document_folder(document_folder)
            
            print(f"✅ JELLY COMPLETE - Processed {len(processed_pages)} pages")
            
            # PIPELINE COMPLETION SUMMARY
            pipeline_end = datetime.now()
            total_time = (pipeline_end - pipeline_start).total_seconds()
            
            print("\n🥪 PB&J SANDWICH COMPLETE!")
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
                    "llamaparse_mode": "premium" if self.config.use_premium_mode else "standard",
                    "openai_model": self.config.openai_model,
                    "output_base_dir": self.config.output_base_dir
                },
                "stage_results": {
                    "stage_1_peanut_parse": {
                        "pages_parsed": len(parsed_docs),
                        "folder": stage1_result["parsed_markdown_folder"]
                    },
                    "stage_2_butter_better": {
                        "documents_enhanced": len(enhanced_docs),
                        "folder": str(Path(document_folder) / "02_enhanced_markdown")
                    },
                    "stage_3_jelly_json": {
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
            print(f"\n❌ PB&J PIPELINE FAILED: {e}")
            raise

    def make(self, pdf_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        🥪 Make a complete PB&J sandwich
        User-friendly alias for process() method
        """
        return self.process(pdf_path, output_dir)


def main():
    """🥪 Command line interface for the PB&J Pipeline"""
    
    if len(sys.argv) < 2:
        print("🥪 PB&J Pipeline - Parse, Better, JSON")
        print("Usage: python -m pbj.sandwich <pdf_path> [--premium] [--model MODEL]")
        print("\nExamples:")
        print("  python -m pbj.sandwich test.pdf")
        print("  python -m pbj.sandwich document.pdf --premium")
        print("  python -m pbj.sandwich report.pdf --premium --model gpt-4")
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
    print("🥪 PB&J PIPELINE CONFIGURATION:")
    print(f"  📄 PDF File: {pdf_path}")
    print(f"  🔧 LlamaParse Mode: {'Premium' if use_premium else 'Standard'}")
    print(f"  🤖 OpenAI Model: {openai_model}")
    print()
    
    try:
        # RUN COMPLETE PB&J PIPELINE
        sandwich = Sandwich(use_premium=use_premium, openai_model=openai_model)
        result = sandwich.process(pdf_path)
        
        print(f"\n🎯 SUCCESS! Check your results in: {result['folder_structure']['main_folder']}")
        
    except Exception as e:
        print(f"\n💥 PB&J PIPELINE ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 