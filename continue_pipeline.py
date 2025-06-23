#!/usr/bin/env python3
"""
Continue Pipeline from Stage 2
==============================

This script continues the pipeline from stage 2 (markdown enhancement) onwards
using an existing document folder that already has stage 1 (parsed markdown) completed.
"""

import sys
from pathlib import Path
from markdown_enhancer import MarkdownEnhancer
from data_cleaner import DataCleaner

def continue_from_stage2(document_folder_path: str, openai_model: str = "gpt-4"):
    """
    Continue pipeline from stage 2 onwards
    
    Args:
        document_folder_path: Path to existing document folder with 01_parsed_markdown
        openai_model: OpenAI model to use for enhancement and cleaning
    """
    
    document_folder = Path(document_folder_path)
    if not document_folder.exists():
        raise FileNotFoundError(f"Document folder not found: {document_folder_path}")
    
    parsed_md_folder = document_folder / "01_parsed_markdown"
    if not parsed_md_folder.exists():
        raise FileNotFoundError(f"Parsed markdown folder not found: {parsed_md_folder}")
    
    print(f"🔄 CONTINUING PIPELINE FROM STAGE 2")
    print(f"📁 Document Folder: {document_folder}")
    print(f"🤖 OpenAI Model: {openai_model}")
    print("=" * 60)
    
    try:
        # STAGE 2: MARKDOWN ENHANCEMENT
        print("\n🔧 STAGE 2: MARKDOWN ENHANCEMENT WITH OPENAI")
        print("-" * 40)
        
        enhancer = MarkdownEnhancer(model=openai_model)
        enhanced_docs = enhancer.enhance_document_folder(str(document_folder))
        
        print(f"✅ STAGE 2 COMPLETE - Enhanced {len(enhanced_docs)} documents")
        
        # STAGE 3: DATA CLEANING AND JSON EXTRACTION
        print("\n🧹 STAGE 3: DATA CLEANING AND JSON EXTRACTION")
        print("-" * 40)
        
        cleaner = DataCleaner(model=openai_model)
        processed_pages = cleaner.process_document_folder(str(document_folder))
        
        print(f"✅ STAGE 3 COMPLETE - Processed {len(processed_pages)} pages")
        
        # COMPLETION SUMMARY
        print("\n🎉 PIPELINE CONTINUATION SUCCESSFUL!")
        print("=" * 60)
        print(f"📁 Document Folder: {document_folder}")
        print(f"📄 Pages Processed: {len(processed_pages)}")
        print(f"📊 Tables Extracted: {sum(len(page.tables) for page in processed_pages)}")
        print(f"🔍 Unique Keywords: {len(set().union(*[page.keywords for page in processed_pages])) if processed_pages else 0}")
        print(f"💾 Final Output: {document_folder / 'final_output.json'}")
        
        return {
            "document_folder": str(document_folder),
            "enhanced_docs": len(enhanced_docs),
            "processed_pages": len(processed_pages),
            "final_output": str(document_folder / "final_output.json")
        }
        
    except Exception as e:
        print(f"\n❌ PIPELINE CONTINUATION FAILED: {e}")
        raise

def main():
    """Command line interface"""
    
    if len(sys.argv) < 2:
        print("Usage: python continue_pipeline.py <document_folder_path> [--model MODEL]")
        print("\nExamples:")
        print("  python continue_pipeline.py data/test_20250622_180155_premium")
        print("  python continue_pipeline.py data/test_20250622_180155_premium --model gpt-4")
        print("\nOptions:")
        print("  --model      OpenAI model for enhancement/cleaning (default: gpt-4)")
        sys.exit(1)
    
    # PARSE ARGUMENTS
    document_folder_path = sys.argv[1]
    
    # GET MODEL ARGUMENT
    openai_model = "gpt-4"  # DEFAULT
    if "--model" in sys.argv:
        model_index = sys.argv.index("--model")
        if model_index + 1 < len(sys.argv):
            openai_model = sys.argv[model_index + 1]
    
    try:
        result = continue_from_stage2(document_folder_path, openai_model)
        print(f"\n🎯 SUCCESS! Check results in: {result['document_folder']}")
        
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 