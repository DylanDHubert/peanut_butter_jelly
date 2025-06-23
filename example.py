#!/usr/bin/env python3
"""
PB&J Pipeline Examples
======================

Examples showing how to use the PB&J Pipeline with different configuration methods.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pbj.config import PipelineConfig, create_config
from pbj.sandwich import Sandwich
from pbj.peanut import Peanut
from pbj.butter import Butter
from pbj.jelly import Jelly

def basic_usage():
    """Basic usage with automatic configuration loading"""
    print("Example 1: Basic Usage")
    print("-" * 30)
    
    # The pipeline automatically loads configuration from:
    # 1. Environment variables (LLAMAPARSE_API_KEY, etc.)
    # 2. config.yaml or config.json files
    # 3. .env file
    # 4. Default values
    
    sandwich = Sandwich()
    
    try:
        result = sandwich.process("test.pdf")
        print(f"Processing complete: {result['pipeline_info']['document_folder']}")
    except Exception as e:
        print(f"Error: {e}")

def custom_output_directory():
    """Custom output directory for specific project"""
    print("\nExample 2: Custom Output Directory")
    print("-" * 40)
    
    config = create_config(
        output_base_dir="my_project_documents",
        create_timestamped_folders=False
    )
    
    sandwich = Sandwich(config=config)
    
    try:
        result = sandwich.process("test.pdf")
        print(f"Processing complete: {result['pipeline_info']['document_folder']}")
    except Exception as e:
        print(f"Error: {e}")

def environment_variables():
    """Using environment variables for configuration"""
    print("\nExample 3: Environment Variables")
    print("-" * 35)
    
    # Set environment variables (in real usage, do this in your shell)
    os.environ["PBJ_OUTPUT_DIR"] = "uploads/processed"
    os.environ["PBJ_PREMIUM_MODE"] = "true"
    os.environ["PBJ_VERBOSE"] = "false"
    
    # The pipeline automatically picks up these settings
    sandwich = Sandwich()
    
    try:
        result = sandwich.process("test.pdf")
        print(f"Processing complete: {result['pipeline_info']['document_folder']}")
        print(f"Output dir: {result['pipeline_info']['output_base_dir']}")
    except Exception as e:
        print(f"Error: {e}")

def programmatic_configuration():
    """Programmatic configuration for different use cases"""
    print("\nExample 4: Programmatic Configuration")
    print("-" * 40)
    
    # Web app configuration
    web_config = create_config(
        output_base_dir="uploads/processed_docs",
        create_timestamped_folders=True,
        use_premium_mode=True,
        openai_model="gpt-4-turbo",
        enable_verbose_logging=False
    )
    
    # CLI tool configuration
    cli_config = create_config(
        output_base_dir=".",
        create_timestamped_folders=False,
        use_premium_mode=False,
        enable_verbose_logging=True
    )
    
    # Library configuration
    library_config = create_config(
        output_base_dir="/tmp/pbj_processing",
        create_timestamped_folders=True,
        save_intermediate_files=False
    )
    
    print("Created configurations for different use cases:")
    print(f"  Web App: {web_config.output_base_dir}")
    print(f"  CLI Tool: {cli_config.output_base_dir}")
    print(f"  Library: {library_config.output_base_dir}")

def individual_stages():
    """Individual processing stages"""
    print("\nExample 5: Individual Stages")
    print("-" * 30)
    
    # Stage 1: Peanut (Parse)
    peanut = Peanut(use_premium=True)
    print("Peanut (Parse):")
    print("  parsed = peanut.process('document.pdf')")
    print("  parsed = peanut.process_async('document.pdf')")
    
    # Stage 2: Butter (Better)
    butter = Butter(model="gpt-4")
    print("\nButter (Better):")
    print("  enhanced = butter.process_document_folder('folder/')")
    
    # Stage 3: Jelly (JSON)
    jelly = Jelly(model="gpt-4")
    print("\nJelly (JSON):")
    print("  processed = jelly.process_document_folder('folder/')")

def save_and_load_config():
    """Save and load configuration files"""
    print("\nExample 6: Save and Load Configuration")
    print("-" * 40)
    
    # Create a custom configuration
    config = create_config(
        output_base_dir="my_custom_output",
        use_premium_mode=True,
        openai_model="gpt-4-turbo",
        max_tokens=8000
    )
    
    # Save configuration to file
    config.save_config("my_custom_config.yaml")
    
    # Load configuration from file (happens automatically)
    new_config = PipelineConfig()
    print(f"Loaded config: {new_config.output_base_dir}")

def check_environment():
    """Check if API keys are configured"""
    print("Environment Check:")
    
    llama_key = os.getenv("LLAMAPARSE_API_KEY") or os.getenv("LLAMA_CLOUD_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if llama_key:
        print("  LLAMAPARSE_API_KEY is set")
    else:
        print("  LLAMAPARSE_API_KEY not set - PDF parsing won't work")
    
    if openai_key:
        print("  OPENAI_API_KEY is set")
    else:
        print("  OPENAI_API_KEY not set - enhancement/extraction won't work")
    
    if llama_key and openai_key:
        print("  All API keys configured - ready to process")
    else:
        print("  Set missing API keys in environment or config files")

def main():
    """Run all examples"""
    print("PB&J Pipeline Examples")
    print("=" * 25)
    print("This demonstrates how to configure the pipeline for different projects.")
    print("The pipeline automatically loads configuration from multiple sources.")
    print()
    
    check_environment()
    print()
    
    basic_usage()
    custom_output_directory()
    environment_variables()
    programmatic_configuration()
    individual_stages()
    save_and_load_config()
    
    print("\nConfiguration Examples Complete!")
    print("=" * 35)
    print("Key benefits:")
    print("- No need to manually create .env files")
    print("- Configurable output directories for any project")
    print("- Environment variable support for deployment")
    print("- Configuration file support for project settings")
    print("- Programmatic configuration for different use cases")

if __name__ == "__main__":
    main() 