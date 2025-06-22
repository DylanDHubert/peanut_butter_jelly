#!/usr/bin/env python3
"""
Complete Three-Stage PDF Processing Pipeline
===========================================

STAGE 1: PDF → Raw Markdown (LlamaParse)
STAGE 2: Raw Markdown → Enhanced Markdown (OpenAI Enhancement)
STAGE 3: Enhanced Markdown → Clean JSON (OpenAI Extraction)
"""

from pdf_processor import process_pdf
from markdown_enhancer import enhance_markdown_folder
from data_cleaner import clean_data_folder
from pathlib import Path
import json
import time

def complete_pipeline(pdf_path: str, output_base_dir: str = "data", use_premium: bool = True, model: str = "gpt-4") -> dict:
    """
    Run the complete three-stage PDF processing pipeline
    
    Args:
        pdf_path: Path to the PDF file
        output_base_dir: Base directory for all outputs
        use_premium: Whether to use Premium mode for LlamaParse
        model: OpenAI model to use for enhancement and cleaning
        
    Returns:
        dict: Pipeline results with file paths and statistics
    """
    print("🚀 STARTING COMPLETE THREE-STAGE PIPELINE")
    print("=" * 60)
    
    pipeline_start = time.time()
    results = {}
    
    # STAGE 1: PDF TO RAW MARKDOWN
    print("\n📄 STAGE 1: PDF → RAW MARKDOWN (LlamaParse)")
    print("-" * 40)
    
    stage1_start = time.time()
    raw_markdown_files = process_pdf(pdf_path, use_premium=use_premium)
    raw_markdown_dir = Path(raw_markdown_files[0]).parent
    stage1_time = time.time() - stage1_start
    
    print(f"✅ STAGE 1 COMPLETE: {stage1_time:.2f}s")
    print(f"   Raw markdown saved to: {raw_markdown_dir}")
    
    results['stage1'] = {
        'time_seconds': stage1_time,
        'output_dir': str(raw_markdown_dir),
        'files': len(raw_markdown_files)
    }
    
    # STAGE 2: RAW MARKDOWN TO ENHANCED MARKDOWN
    print("\n🧠 STAGE 2: RAW MARKDOWN → ENHANCED MARKDOWN (AI Enhancement)")
    print("-" * 40)
    
    stage2_start = time.time()
    enhanced_dir = f"{output_base_dir}/enhanced_{raw_markdown_dir.name}"
    enhanced_docs = enhance_markdown_folder(str(raw_markdown_dir), enhanced_dir, model=model)
    stage2_time = time.time() - stage2_start
    
    print(f"✅ STAGE 2 COMPLETE: {stage2_time:.2f}s")
    print(f"   Enhanced markdown saved to: {enhanced_dir}")
    
    # COUNT TOTAL ENHANCEMENTS
    total_enhancements = sum(len(doc.enhancement_notes) for doc in enhanced_docs)
    
    results['stage2'] = {
        'time_seconds': stage2_time,
        'output_dir': enhanced_dir,
        'files': len(enhanced_docs),
        'total_enhancements': total_enhancements
    }
    
    # STAGE 3: ENHANCED MARKDOWN TO CLEAN JSON
    print("\n📊 STAGE 3: ENHANCED MARKDOWN → CLEAN JSON (AI Extraction)")
    print("-" * 40)
    
    stage3_start = time.time()
    final_json = f"{output_base_dir}/final_{raw_markdown_dir.name}.json"
    processed_pages = clean_data_folder(enhanced_dir, final_json, model=model)
    stage3_time = time.time() - stage3_start
    
    print(f"✅ STAGE 3 COMPLETE: {stage3_time:.2f}s")
    print(f"   Final JSON saved to: {final_json}")
    
    # COUNT TOTAL TABLES
    total_tables = sum(len(page.tables) for page in processed_pages)
    
    results['stage3'] = {
        'time_seconds': stage3_time,
        'output_file': final_json,
        'pages': len(processed_pages),
        'total_tables': total_tables
    }
    
    # PIPELINE SUMMARY
    total_time = time.time() - pipeline_start
    
    print("\n🎉 COMPLETE PIPELINE FINISHED!")
    print("=" * 60)
    print(f"⏱️  TOTAL TIME: {total_time:.2f} seconds")
    print(f"   Stage 1 (PDF Parse): {stage1_time:.2f}s ({stage1_time/total_time*100:.1f}%)")
    print(f"   Stage 2 (Enhancement): {stage2_time:.2f}s ({stage2_time/total_time*100:.1f}%)")
    print(f"   Stage 3 (JSON Extract): {stage3_time:.2f}s ({stage3_time/total_time*100:.1f}%)")
    
    print(f"\n📊 PROCESSING RESULTS:")
    print(f"   📄 Pages processed: {len(processed_pages)}")
    print(f"   🔧 Total enhancements: {total_enhancements}")
    print(f"   🗂️  Tables extracted: {total_tables}")
    print(f"   📁 Final output: {final_json}")
    
    results['pipeline_summary'] = {
        'total_time_seconds': total_time,
        'pdf_file': pdf_path,
        'final_output': final_json,
        'use_premium': use_premium,
        'model_used': model,
        'success': True
    }
    
    return results

def pipeline_comparison(pdf_path: str, output_base_dir: str = "data") -> dict:
    """
    Compare two-stage vs three-stage pipeline results
    
    Args:
        pdf_path: Path to the PDF file
        output_base_dir: Base directory for outputs
        
    Returns:
        dict: Comparison results
    """
    print("🔬 PIPELINE COMPARISON: 2-STAGE vs 3-STAGE")
    print("=" * 60)
    
    # RUN TWO-STAGE PIPELINE (ORIGINAL)
    print("\n📊 RUNNING 2-STAGE PIPELINE (Original)")
    print("-" * 40)
    
    two_stage_start = time.time()
    raw_files = process_pdf(pdf_path, use_premium=True)
    raw_dir = Path(raw_files[0]).parent
    two_stage_json = f"{output_base_dir}/two_stage_{raw_dir.name}.json"
    two_stage_pages = clean_data_folder(str(raw_dir), two_stage_json)
    two_stage_time = time.time() - two_stage_start
    
    print(f"✅ 2-STAGE COMPLETE: {two_stage_time:.2f}s")
    
    # RUN THREE-STAGE PIPELINE (ENHANCED)
    print("\n📊 RUNNING 3-STAGE PIPELINE (Enhanced)")
    print("-" * 40)
    
    three_stage_results = complete_pipeline(pdf_path, output_base_dir, use_premium=True)
    three_stage_time = three_stage_results['pipeline_summary']['total_time_seconds']
    
    # COMPARISON ANALYSIS
    print("\n🔍 COMPARISON RESULTS")
    print("=" * 60)
    print(f"⏱️  Processing Time:")
    print(f"   2-Stage: {two_stage_time:.2f}s")
    print(f"   3-Stage: {three_stage_time:.2f}s")
    print(f"   Overhead: {three_stage_time - two_stage_time:.2f}s ({(three_stage_time/two_stage_time - 1)*100:.1f}% increase)")
    
    print(f"\n📊 Enhancement Benefits:")
    print(f"   Enhancements applied: {three_stage_results['stage2']['total_enhancements']}")
    print(f"   Column improvements: Enhanced names and context")
    print(f"   Structure cleanup: Integrated footnotes and legends")
    
    return {
        'two_stage': {
            'time_seconds': two_stage_time,
            'output_file': two_stage_json,
            'pages': len(two_stage_pages)
        },
        'three_stage': three_stage_results,
        'improvement_overhead': three_stage_time - two_stage_time,
        'overhead_percentage': (three_stage_time/two_stage_time - 1) * 100
    }

def batch_pipeline(pdf_files: list, output_base_dir: str = "data", use_premium: bool = True) -> dict:
    """
    Process multiple PDFs through the complete pipeline
    
    Args:
        pdf_files: List of PDF file paths
        output_base_dir: Base directory for outputs
        use_premium: Whether to use Premium mode
        
    Returns:
        dict: Batch processing results
    """
    print(f"🔄 BATCH PROCESSING: {len(pdf_files)} PDFs")
    print("=" * 60)
    
    batch_start = time.time()
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n📄 PROCESSING PDF {i}/{len(pdf_files)}: {Path(pdf_file).name}")
        print("-" * 40)
        
        try:
            pdf_results = complete_pipeline(pdf_file, output_base_dir, use_premium)
            results.append(pdf_results)
            print(f"✅ PDF {i} COMPLETE")
        except Exception as e:
            print(f"❌ PDF {i} FAILED: {e}")
            results.append({'error': str(e), 'pdf_file': pdf_file})
    
    batch_time = time.time() - batch_start
    successful = len([r for r in results if 'error' not in r])
    
    print(f"\n🎉 BATCH PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"⏱️  Total time: {batch_time:.2f} seconds")
    print(f"📊 Success rate: {successful}/{len(pdf_files)} ({successful/len(pdf_files)*100:.1f}%)")
    print(f"⚡ Average per PDF: {batch_time/len(pdf_files):.2f} seconds")
    
    return {
        'total_time_seconds': batch_time,
        'total_pdfs': len(pdf_files),
        'successful': successful,
        'results': results
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pipeline_complete.py <pdf_path> [comparison|batch]")
        print("Examples:")
        print("  python pipeline_complete.py test.pdf")
        print("  python pipeline_complete.py test.pdf comparison")
        print("  python pipeline_complete.py \"*.pdf\" batch")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "normal"
    
    try:
        if mode == "comparison":
            results = pipeline_comparison(pdf_path)
        elif mode == "batch":
            import glob
            pdf_files = glob.glob(pdf_path)
            if not pdf_files:
                print(f"No PDF files found matching: {pdf_path}")
                sys.exit(1)
            results = batch_pipeline(pdf_files)
        else:
            results = complete_pipeline(pdf_path)
        
        # SAVE RESULTS
        results_file = f"pipeline_results_{int(time.time())}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Pipeline results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ PIPELINE ERROR: {e}")
        sys.exit(1) 