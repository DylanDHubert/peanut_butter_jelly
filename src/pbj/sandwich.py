#!/usr/bin/env python3
"""
🥪 Sandwich - Complete PB&J Pipeline Orchestrator
=================================================

Complete 4-stage document processing pipeline with organized folder structure:
1. Peanut (Parse): PDF → Markdown using LlamaParse
2. Butter (Better): Markdown → Enhanced Markdown using OpenAI
3. Jelly (JSON): Enhanced Markdown → Structured JSON using OpenAI
4. Toast (Format): Column-based → Row-based JSON conversion

FOLDER STRUCTURE PER DOCUMENT:
document_folder/
├── original.pdf                    # Original PDF file
├── document_metadata.json          # Pipeline tracking metadata
├── final_output.json               # Final combined JSON output (toasted format)
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
from .toast import Toast
from .config import PipelineConfig, create_config

class Sandwich:
    """
    🥪 Sandwich - Complete PB&J Pipeline Orchestrator
    
    Complete 4-stage document processing pipeline that combines Peanut (Parse), 
    Butter (Better), Jelly (JSON), and Toast (Format) into one delicious document 
    processing sandwich.
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
        # Note: Peanut is created fresh per PDF to avoid LlamaParse job conflicts
        self.butter = Butter(model=self.config.openai_model, config=self.config)
        self.jelly = Jelly(model=self.config.openai_model, config=self.config)
        self.toast = Toast()
    
    def process(self, pdf_path: str, output_dir: Optional[str] = None, skip_butter: bool = False) -> Dict[str, Any]:
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
            
            # Create fresh Peanut instance for each PDF to avoid LlamaParse job conflicts
            peanut = Peanut(config=self.config)
            parsed_docs = peanut.process(pdf_path)
            stage1_result = peanut.save_parsed_documents(parsed_docs, output_dir, pdf_path)
            
            document_folder = stage1_result["main_folder"]
            print(f"✅ PEANUT COMPLETE - Document folder: {document_folder}")
            
            enhanced_docs = None
            if not skip_butter:
                # STAGE 2: BUTTER (BETTER) - MARKDOWN ENHANCEMENT
                print("\n🧈 STAGE 2: BUTTER (BETTER) - MARKDOWN ENHANCEMENT")
                print("-" * 40)
                enhanced_docs = self.butter._process_document_folder(document_folder)
                print(f"✅ BUTTER COMPLETE - Enhanced {len(enhanced_docs)} documents")
            else:
                print("\n⏩ SKIPPING BUTTER STAGE -- Using raw markdown from Peanut")
            
            # STAGE 3: JELLY (JSON) - DATA CLEANING AND JSON EXTRACTION
            print("\n🍇 STAGE 3: JELLY (JSON) - DATA EXTRACTION")
            print("-" * 40)
            processed_pages = self.jelly._process_document_folder(document_folder, skip_butter=skip_butter)
            print(f"✅ JELLY COMPLETE - Processed {len(processed_pages)} pages")
            
            # STAGE 4: TOAST (FORMAT CONVERSION) - CONVERT TO ROW-BASED FORMAT
            print("\n🍞 STAGE 4: TOAST (FORMAT CONVERSION)")
            print("-" * 40)
            
            # Convert final output to toasted format
            final_output_path = Path(document_folder) / "final_output.json"
            if final_output_path.exists():
                self.toast.convert_file(str(final_output_path))
                print(f"✅ TOAST COMPLETE - Converted to row-based format")
            else:
                print(f"⚠️  TOAST SKIPPED - No final_output.json found")
            
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
                    "output_base_dir": self.config.output_base_dir,
                    "butter_skipped": skip_butter
                },
                "stage_results": {
                    "stage_1_peanut_parse": {
                        "pages_parsed": len(parsed_docs),
                        "folder": stage1_result["parsed_markdown_folder"]
                    },
                    "stage_2_butter_better": {
                        "documents_enhanced": len(enhanced_docs) if enhanced_docs is not None else 0,
                        "folder": str(Path(document_folder) / "02_enhanced_markdown")
                    },
                    "stage_3_jelly_json": {
                        "pages_processed": len(processed_pages),
                        "individual_json_folder": str(Path(document_folder) / "03_cleaned_json"),
                        "final_output": str(Path(document_folder) / "final_output.json")
                    },
                    "stage_4_toast_format": {
                        "format_converted": "column-based to row-based",
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
            print(f"   Pipeline crashed - check your API keys and document format")
            print(f"   Error details: {str(e)}")
            # Return partial results instead of crashing
            return {
                "pipeline_info": {
                    "completed_at": datetime.now().isoformat(),
                    "total_processing_time_seconds": (datetime.now() - pipeline_start).total_seconds(),
                    "pdf_source": pdf_path,
                    "document_folder": "PIPELINE_FAILED",
                    "llamaparse_mode": "premium" if self.config.use_premium_mode else "standard",
                    "openai_model": self.config.openai_model,
                    "output_base_dir": self.config.output_base_dir,
                    "status": "FAILED",
                    "error": str(e)
                },
                "error_info": {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "failed_at_stage": "unknown"
                }
            }

    def make(self, pdf_path: str, output_dir: Optional[str] = None, skip_butter: bool = False) -> Dict[str, Any]:
        """
        🥪 Make a complete PB&J sandwich
        User-friendly alias for process() method
        """
        return self.process(pdf_path, output_dir, skip_butter=skip_butter)


def main():
    """
    CLI entry point for the PB&J pipeline
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🥪 PB&J Pipeline - Parse, Better, JSON document processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pbj document.pdf                    # Process with default settings
  pbj document.pdf --premium         # Use LlamaParse premium mode
  pbj document.pdf --model gpt-4     # Use specific OpenAI model
  pbj document.pdf --premium --model gpt-4-turbo  # Both options
  pbj document.pdf --skip-butter     # Skip Butter stage (Peanut → Jelly)
        """
    )
    
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to process"
    )
    
    parser.add_argument(
        "--premium",
        action="store_true",
        help="Use LlamaParse premium mode for better parsing"
    )
    
    parser.add_argument(
        "--model",
        default="gpt-4",
        help="OpenAI model to use for enhancement and cleaning (default: gpt-4)"
    )
    
    parser.add_argument(
        "--output-dir",
        help="Custom output directory (optional)"
    )
    
    parser.add_argument(
        "--skip-butter",
        action="store_true",
        help="Skip Butter stage and go directly from Peanut to Jelly"
    )
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_path):
        print(f"❌ Error: PDF file '{args.pdf_path}' not found")
        sys.exit(1)
    
    try:
        # Create and run the pipeline
        sandwich = Sandwich(
            use_premium=args.premium,
            openai_model=args.model
        )
        
        result = sandwich.process(args.pdf_path, args.output_dir, skip_butter=args.skip_butter)
        
        if result.get("pipeline_info", {}).get("status") == "FAILED":
            print(f"\n❌ Pipeline failed: {result.get('error_info', {}).get('error_message', 'Unknown error')}")
            sys.exit(1)
        else:
            print(f"\n✅ Pipeline completed successfully!")
            print(f"📁 Output saved to: {result['pipeline_info']['document_folder']}")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()