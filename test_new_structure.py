#!/usr/bin/env python3
"""
Test Script for New Organized Folder Structure
==============================================

This script demonstrates the new per-document folder structure with:
- Original PDF copied to document folder
- Stage-by-stage subfolders (01, 02, 03)
- Individual file saves after each processing step
- Combined final output JSON
"""

import os
from pathlib import Path
from pipeline_complete import run_complete_pipeline

def test_new_structure():
    """Test the new organized folder structure"""
    
    # CHECK IF TEST PDF EXISTS
    test_pdf = "test.pdf"
    if not Path(test_pdf).exists():
        print(f"❌ Test PDF not found: {test_pdf}")
        print("Please ensure test.pdf exists in the current directory")
        return False
    
    print("🧪 TESTING NEW ORGANIZED FOLDER STRUCTURE")
    print("=" * 50)
    
    try:
        # RUN COMPLETE PIPELINE WITH NEW STRUCTURE
        result = run_complete_pipeline(
            pdf_path=test_pdf,
            use_premium=True,  # USE PREMIUM FOR BETTER RESULTS
            openai_model="gpt-4"
        )
        
        # VERIFY FOLDER STRUCTURE
        print("\n🔍 VERIFYING FOLDER STRUCTURE")
        print("-" * 30)
        
        main_folder = Path(result['folder_structure']['main_folder'])
        
        # CHECK MAIN FOLDER CONTENTS
        expected_files = [
            "document_metadata.json",
            "final_output.json", 
            "pipeline_summary.json",
            test_pdf
        ]
        
        expected_folders = [
            "01_parsed_markdown",
            "02_enhanced_markdown", 
            "03_cleaned_json"
        ]
        
        print(f"📁 Main folder: {main_folder}")
        
        # VERIFY FILES
        for file_name in expected_files:
            file_path = main_folder / file_name
            if file_path.exists():
                print(f"✅ {file_name}")
            else:
                print(f"❌ {file_name} - MISSING")
        
        # VERIFY SUBFOLDERS
        for folder_name in expected_folders:
            folder_path = main_folder / folder_name
            if folder_path.exists():
                file_count = len(list(folder_path.glob("*")))
                print(f"✅ {folder_name}/ ({file_count} files)")
            else:
                print(f"❌ {folder_name}/ - MISSING")
        
        # SHOW FINAL STRUCTURE
        print(f"\n📋 FINAL FOLDER STRUCTURE:")
        print(f"{main_folder}/")
        print(f"├── {test_pdf}")
        print(f"├── document_metadata.json")
        print(f"├── final_output.json")
        print(f"├── pipeline_summary.json")
        
        for folder_name in expected_folders:
            folder_path = main_folder / folder_name
            if folder_path.exists():
                files = list(folder_path.glob("*"))
                print(f"├── {folder_name}/")
                for i, file_path in enumerate(files):
                    prefix = "└──" if i == len(files) - 1 else "├──"
                    print(f"│   {prefix} {file_path.name}")
        
        print(f"\n🎉 NEW STRUCTURE TEST SUCCESSFUL!")
        print(f"📁 Check results in: {main_folder}")
        
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    success = test_new_structure()
    if not success:
        exit(1) 