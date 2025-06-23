#!/usr/bin/env python3
"""
🥜🧈🍇🥪 PB&J Pipeline Examples
===============================

Clean examples showing the standardized PB&J interface.
No confusing methods - just clean, consistent processing!
"""

import os
from pathlib import Path

def example_complete_pipeline():
    """Example 1: Complete PB&J pipeline - the easiest way!"""
    print("🥪 Example 1: Complete PB&J Pipeline")
    print("-" * 40)
    
    from src.pbj import Sandwich
    
    # Create a sandwich with premium parsing and GPT-4
    sandwich = Sandwich(use_premium=True, openai_model="gpt-4")
    
    print("✅ Sandwich created successfully!")
    print("📝 To process a PDF:")
    print("   result = sandwich.process('document.pdf')  # Standardized method")
    print("   # or")
    print("   result = sandwich.make('document.pdf')     # User-friendly alias")
    print("   print(f'Results: {result[\"folder_structure\"][\"main_folder\"]}')")

def example_individual_stages():
    """Example 2: Individual processing stages with clean interface"""
    print("\n🥜🧈🍇 Example 2: Individual Processing Stages")
    print("-" * 50)
    
    from src.pbj import Peanut, Butter, Jelly
    
    # Stage 1: Peanut (Parse) - Clean interface
    print("🥜 Peanut (Parse) - Clean Interface:")
    peanut = Peanut(use_premium=True)
    print("   parsed = peanut.process('document.pdf')        # Main method")
    print("   parsed = peanut.process_async('document.pdf')  # Async version")
    
    # Stage 2: Butter (Better) - Clean interface  
    print("\n🧈 Butter (Better) - Clean Interface:")
    butter = Butter(model="gpt-4")
    print("   enhanced = butter.process(content, 'file.md')    # Process content")
    print("   enhanced = butter.process_file('document.md')    # Process file")
    print("   docs = butter.process_folder('folder/')          # Process folder")
    print("   enhanced = butter.process_async(content)         # Async version")
    
    # Stage 3: Jelly (JSON) - Clean interface
    print("\n🍇 Jelly (JSON) - Clean Interface:")
    jelly = Jelly(model="gpt-4")
    print("   json_data = jelly.process(content, 'file.md')   # Process content")
    print("   json_data = jelly.process_file('document.md')   # Process file")
    print("   pages = jelly.process_folder('folder/')         # Process folder")
    print("   json_data = jelly.process_async('file.md')      # Async version")
    
    print("\n✅ All classes have consistent, clean interfaces!")

def example_fun_aliases():
    """Example 3: Fun themed aliases"""
    print("\n🎭 Example 3: Fun Themed Aliases")
    print("-" * 35)
    
    from src.pbj import Parse, Better, JSON, Pipeline
    
    print("🎪 For those who like the themed experience:")
    
    parser = Parse(use_premium=True)
    print("   parser = Parse(use_premium=True)")
    print("   parsed = parser.process('document.pdf')")
    
    enhancer = Better(model="gpt-4")
    print("   enhancer = Better(model='gpt-4')")
    print("   enhanced = enhancer.process(content)")
    
    extractor = JSON(model="gpt-4")
    print("   extractor = JSON(model='gpt-4')")
    print("   json_data = extractor.process(content)")
    
    pipeline = Pipeline(use_premium=True)
    print("   pipeline = Pipeline(use_premium=True)")
    print("   result = pipeline.process('document.pdf')  # or pipeline.make()")
    
    print("\n✅ Same functionality, themed names!")

def example_consistent_interface():
    """Example 4: Consistent interface across all classes"""
    print("\n🎯 Example 4: Consistent Interface Pattern")
    print("-" * 42)
    
    print("🔄 Every class follows the same pattern:")
    print()
    print("📋 ALL CLASSES:")
    print("   .process()       # Main processing method")
    print("   .process_async() # Async version")
    print()
    print("📋 BUTTER & JELLY ALSO HAVE:")
    print("   .process_file()   # Process single file")
    print("   .process_folder() # Process folder of files")
    print()
    print("📋 SANDWICH SPECIAL:")
    print("   .process()  # Standardized method")
    print("   .make()     # User-friendly alias (same as process)")
    print()
    print("🔒 INTERNAL METHODS (users don't see these):")
    print("   ._process_document_folder()  # Private pipeline methods")
    print()
    print("✅ Clean, predictable, no confusion!")

def example_real_usage_patterns():
    """Example 5: Real-world usage patterns"""
    print("\n💼 Example 5: Real-World Usage Patterns")
    print("-" * 40)
    
    print("🚀 Most Common: Complete Pipeline")
    print("   from src.pbj import Sandwich")
    print("   sandwich = Sandwich(use_premium=True)")
    print("   result = sandwich.process('report.pdf')")
    print()
    
    print("🔧 Advanced: Individual Control")
    print("   from src.pbj import Peanut, Butter, Jelly")
    print("   peanut = Peanut(use_premium=True)")
    print("   butter = Butter(model='gpt-4')")
    print("   jelly = Jelly(model='gpt-4')")
    print("   ")
    print("   # Process step by step")
    print("   parsed = peanut.process('document.pdf')")
    print("   enhanced = butter.process(parsed[0].content)")
    print("   json_data = jelly.process(enhanced.enhanced_content)")
    print()
    
    print("📁 Bulk Processing: Multiple Files")
    print("   from src.pbj import Butter, Jelly")
    print("   butter = Butter()")
    print("   jelly = Jelly()")
    print("   ")
    print("   # Process entire folders")
    print("   enhanced_docs = butter.process_folder('markdown_files/')")
    print("   json_pages = jelly.process_folder('enhanced_files/')")
    print()
    
    print("⚡ Async Processing: High Performance")
    print("   import asyncio")
    print("   async def async_processing():")
    print("       peanut = Peanut()")
    print("       parsed = await peanut.process_async('doc.pdf')")
    print("       return parsed")
    print("   ")
    print("   result = asyncio.run(async_processing())")

def example_command_line():
    """Example 6: Command line usage"""
    print("\n💻 Example 6: Command Line Interface")
    print("-" * 37)
    
    print("🖥️  Simple command line usage:")
    print("   python3 -m src.pbj.sandwich document.pdf")
    print()
    print("🔧 With premium mode:")
    print("   python3 -m src.pbj.sandwich document.pdf --premium")
    print()
    print("🤖 With custom model:")
    print("   python3 -m src.pbj.sandwich report.pdf --premium --model gpt-4")
    print()
    print("✅ Same clean processing, command line convenience!")

def check_environment():
    """Check if API keys are configured"""
    print("🔍 Environment Check:")
    
    llama_key = os.getenv("LLAMA_CLOUD_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if llama_key:
        print("✅ LLAMA_CLOUD_API_KEY is set")
    else:
        print("⚠️  LLAMA_CLOUD_API_KEY not set - PDF parsing won't work")
    
    if openai_key:
        print("✅ OPENAI_API_KEY is set")
    else:
        print("⚠️  OPENAI_API_KEY not set - enhancement/extraction won't work")
    
    if llama_key and openai_key:
        print("🎉 All API keys configured - ready to process!")
    else:
        print("📝 Set missing API keys in your .env file")

def main():
    """Run all examples"""
    print("🥜🧈🍇🥪 PB&J Pipeline - Clean Interface Examples")
    print("=" * 55)
    
    check_environment()
    print()
    
    example_complete_pipeline()
    example_individual_stages()
    example_fun_aliases()
    example_consistent_interface()
    example_real_usage_patterns()
    example_command_line()
    
    print(f"\n🎯 All examples completed!")
    print("🧹 Clean interface - no confusing methods!")
    print("🔒 Private pipeline methods hidden from users!")
    print("🥪 Ready to make some delicious document processing sandwiches!")

if __name__ == "__main__":
    main() 