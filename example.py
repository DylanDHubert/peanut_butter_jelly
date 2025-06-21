#!/usr/bin/env python3
"""
Enhanced PDF Processing Pipeline with LlamaParse
===============================================

ORGANIZED DATA STRUCTURE WITH AUTOMATIC TIMESTAMPING AND RUN TRACKING
"""

from pdf_processor import PDFProcessor, process_pdf
from pathlib import Path
import json

def main():
    """DEMONSTRATE THE ENHANCED PDF PROCESSING PIPELINE"""
    
    # EXAMPLE 1: SIMPLE ONE-LINER WITH AUTOMATIC DATA ORGANIZATION
    print("🚀 EXAMPLE 1: SIMPLE ONE-LINER (AUTO-ORGANIZED)")
    print("=" * 60)
    
    # THIS WILL CREATE: data/YYYYMMDD_HHMM_standard/
    saved_files = process_pdf("test.pdf", use_premium=False)
    print(f"✅ SAVED {len(saved_files)} FILES WITH AUTOMATIC ORGANIZATION")
    print()
    
    # EXAMPLE 2: PREMIUM MODE WITH AUTO-ORGANIZATION
    print("🚀 EXAMPLE 2: PREMIUM MODE (AUTO-ORGANIZED)")
    print("=" * 60)
    
    # THIS WILL CREATE: data/YYYYMMDD_HHMM_premium/
    saved_files_premium = process_pdf("test.pdf", use_premium=True)
    print(f"✅ SAVED {len(saved_files_premium)} FILES IN PREMIUM MODE")
    print()
    
    # EXAMPLE 3: CUSTOM OUTPUT DIRECTORY
    print("🚀 EXAMPLE 3: CUSTOM OUTPUT DIRECTORY")
    print("=" * 60)
    
    custom_dir = "data/custom_test_run"
    saved_files_custom = process_pdf("test.pdf", output_dir=custom_dir)
    print(f"✅ SAVED {len(saved_files_custom)} FILES TO CUSTOM DIRECTORY: {custom_dir}")
    print()
    
    # EXAMPLE 4: DETAILED PROCESSING WITH METADATA
    print("🚀 EXAMPLE 4: DETAILED PROCESSING")
    print("=" * 60)
    
    # CREATE PROCESSOR INSTANCE
    processor = PDFProcessor(use_premium=True)
    
    # PARSE THE PDF
    print("PARSING PDF...")
    parsed_docs = processor.parse_pdf("test.pdf")
    
    # SAVE WITH DETAILED LOGGING
    print("SAVING PARSED DOCUMENTS...")
    saved_files_detailed = processor.save_parsed_documents(parsed_docs)
    
    print(f"✅ PROCESSING COMPLETE!")
    print(f"   - {len(parsed_docs)} DOCUMENTS PARSED")
    print(f"   - {len(saved_files_detailed)} FILES SAVED")
    
    # SHOW RUN METADATA
    data_dir = Path(saved_files_detailed[0]).parent
    metadata_file = data_dir / "run_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        print(f"   - RUN ID: {metadata['run_id']}")
        print(f"   - PROCESSING TIME: {metadata['processing_time_seconds']:.2f}s")
        print(f"   - MODE: {metadata['mode'].upper()}")
    
    print()
    
    # EXAMPLE 5: DATA DIRECTORY OVERVIEW
    print("📁 DATA DIRECTORY OVERVIEW")
    print("=" * 60)
    
    data_path = Path("data")
    if data_path.exists():
        runs = sorted([d for d in data_path.iterdir() if d.is_dir()])
        print(f"FOUND {len(runs)} PROCESSING RUNS:")
        
        for run_dir in runs[-5:]:  # SHOW LAST 5 RUNS
            metadata_file = run_dir / "run_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                files_count = metadata.get('document_count', 0)
                mode = metadata.get('mode', 'unknown').upper()
                processing_time = metadata.get('processing_time_seconds', 0)
                print(f"   📂 {run_dir.name}")
                print(f"      - Mode: {mode}")
                print(f"      - Files: {files_count}")
                print(f"      - Time: {processing_time:.2f}s")
            else:
                md_files = list(run_dir.glob("*.md"))
                print(f"   📂 {run_dir.name}")
                print(f"      - Files: {len(md_files)}")
    
    print("\n🎉 ALL EXAMPLES COMPLETED!")
    print("\nYOUR DATA IS ORGANIZED IN THE 'data/' DIRECTORY WITH:")
    print("   ✅ AUTOMATIC TIMESTAMPING")
    print("   ✅ MODE IDENTIFICATION (standard/premium)")
    print("   ✅ RUN METADATA TRACKING")
    print("   ✅ CLEAN FILE ORGANIZATION")

if __name__ == "__main__":
    main() 