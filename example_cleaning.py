#!/usr/bin/env python3
"""
Data Cleaning Pipeline Example
=============================

DEMONSTRATES THE TWO-STAGE PROCESSING PIPELINE:
1. LlamaParse: PDF → Raw Markdown
2. OpenAI Agent: Raw Markdown → Clean JSON
"""

from pdf_processor import process_pdf
from data_cleaner import clean_data_folder, DataCleaner
from pathlib import Path
import json

def main():
    """DEMONSTRATE THE COMPLETE PIPELINE"""
    
    print("🚀 TWO-STAGE PDF PROCESSING PIPELINE")
    print("=" * 60)
    
    # STAGE 1: PDF TO RAW MARKDOWN WITH LLAMAPARSE
    print("\n📄 STAGE 1: PDF → RAW MARKDOWN (LlamaParse)")
    print("-" * 40)
    
    # PROCESS PDF WITH PREMIUM MODE
    saved_files = process_pdf("test.pdf", use_premium=True)
    
    # GET THE OUTPUT DIRECTORY
    output_dir = Path(saved_files[0]).parent
    print(f"✅ RAW MARKDOWN SAVED TO: {output_dir}")
    
    # STAGE 2: RAW MARKDOWN TO CLEAN JSON WITH OPENAI
    print("\n🧠 STAGE 2: RAW MARKDOWN → CLEAN JSON (OpenAI)")
    print("-" * 40)
    
    # CLEAN THE DATA
    output_json = f"data/cleaned_{output_dir.name}.json"
    processed_pages = clean_data_folder(str(output_dir), output_json)
    
    print(f"✅ CLEAN JSON SAVED TO: {output_json}")
    
    # DEMONSTRATE RESULTS
    print("\n📊 PROCESSING RESULTS")
    print("-" * 40)
    
    total_tables = sum(len(page.tables) for page in processed_pages)
    print(f"📄 Pages processed: {len(processed_pages)}")
    print(f"🗂️  Total tables: {total_tables}")
    
    # SHOW SAMPLE RESULTS
    for i, page in enumerate(processed_pages[:2]):  # SHOW FIRST 2 PAGES
        print(f"\n📄 PAGE {i+1}: {page.title}")
        print(f"   Summary: {page.summary}")
        print(f"   Keywords: {', '.join(page.keywords)}")
        print(f"   Tables: {len(page.tables)}")
        
        for j, table in enumerate(page.tables):
            print(f"      🗂️  Table {j+1}: {table.title}")
            print(f"         - {len(table.columns)} columns, {len(table.rows)} rows")
            print(f"         - Description: {table.description}")
    
    print("\n🎉 PIPELINE COMPLETE!")
    print("\nYOUR DATA IS NOW:")
    print("   ✅ CLEANED AND STANDARDIZED")
    print("   ✅ OPTIMIZED FOR RAG SYSTEMS")
    print("   ✅ SEARCHABLE WITH KEYWORDS")
    print("   ✅ STRUCTURED AS JSON")

def demonstrate_single_file_cleaning():
    """DEMONSTRATE CLEANING A SINGLE FILE"""
    
    print("\n🔧 SINGLE FILE CLEANING DEMO")
    print("-" * 40)
    
    # INITIALIZE CLEANER
    cleaner = DataCleaner(model="gpt-4")
    
    # PROCESS LATEST OUTPUT FILE
    latest_dir = max(Path("data").glob("*_premium"), key=lambda p: p.stat().st_mtime)
    test_file = next(latest_dir.glob("test_part_*.md"))
    
    print(f"PROCESSING: {test_file}")
    
    # CLEAN THE FILE
    processed_page = cleaner.process_file(str(test_file))
    
    # SHOW RESULTS
    print(f"\n✅ CLEANED RESULTS:")
    print(f"Title: {processed_page.title}")
    print(f"Summary: {processed_page.summary}")
    print(f"Keywords: {', '.join(processed_page.keywords)}")
    print(f"Tables found: {len(processed_page.tables)}")
    
    # SHOW TABLE STRUCTURE
    for i, table in enumerate(processed_page.tables):
        print(f"\nTable {i+1}: {table.title}")
        print(f"  Columns: {table.columns}")
        print(f"  Rows: {len(table.rows)}")
        print(f"  Sample row: {table.rows[0] if table.rows else 'No data'}")

def demonstrate_json_structure():
    """SHOW THE STANDARDIZED JSON STRUCTURE"""
    
    print("\n📋 STANDARDIZED JSON STRUCTURE")
    print("-" * 40)
    
    # SAMPLE JSON STRUCTURE
    sample_structure = {
        "processed_at": "2025-06-21T17:30:00",
        "total_pages": 4,
        "total_tables": 8,
        "pages": [
            {
                "page_id": "test_part_1",
                "title": "Femoral Component Dimensions",
                "summary": "Technical specifications for JOURNEY II BCS femoral components including dimensions and measurements for sizes 1-10.",
                "keywords": ["femoral", "component", "dimensions", "specifications", "medical"],
                "tables": [
                    {
                        "table_id": "table_1",
                        "title": "Femoral Component Measurements",
                        "description": "Dimensional specifications for femoral components across all sizes",
                        "columns": ["Size", "Anterior Posterior", "Medial Lateral", "PS Box Width"],
                        "rows": [
                            ["1", "51.7", "59.0", "16.5"],
                            ["2", "53.7", "60.0", "16.5"]
                        ],
                        "metadata": {
                            "row_count": 10,
                            "column_count": 11,
                            "data_types": ["number", "number", "number", "number"],
                            "notes": "All measurements in millimeters"
                        }
                    }
                ],
                "raw_content": "# Test Part 1...",
                "processing_metadata": {
                    "source_file": "test_part_1.md",
                    "processed_at": "2025-06-21T17:30:00",
                    "model_used": "gpt-4",
                    "tables_found": 1
                }
            }
        ]
    }
    
    print("SAMPLE JSON OUTPUT:")
    print(json.dumps(sample_structure, indent=2)[:1000] + "...")
    
    print("\n🎯 PERFECT FOR:")
    print("   • Vector embeddings")
    print("   • Semantic search")
    print("   • RAG retrieval")
    print("   • Database storage")
    print("   • API responses")

if __name__ == "__main__":
    # RUN MAIN PIPELINE
    main()
    
    # UNCOMMENT TO RUN OTHER DEMOS
    # demonstrate_single_file_cleaning()
    # demonstrate_json_structure() 