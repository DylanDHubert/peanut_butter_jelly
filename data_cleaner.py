#!/usr/bin/env python3
"""
Data Cleaning and Standardization Pipeline
==========================================

SECOND-STAGE PROCESSING: CLEAN LLAMAPARSE OUTPUT INTO STANDARDIZED JSON
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import openai
from openai import OpenAI
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES FROM .ENV FILE
load_dotenv()

@dataclass
class ProcessedTable:
    """Standardized table structure for RAG systems"""
    table_id: str
    title: str
    description: str
    columns: List[str]
    rows: List[List[str]]
    metadata: Dict[str, Any]

@dataclass
class ProcessedPage:
    """Standardized page structure"""
    page_id: str
    title: str
    summary: str
    keywords: List[str]
    tables: List[ProcessedTable]
    raw_content: str
    processing_metadata: Dict[str, Any]

class DataCleaner:
    """
    INTELLIGENT DATA CLEANING USING OPENAI
    
    Takes raw LlamaParse markdown output and converts to standardized JSON
    optimized for RAG systems and consistent table structures.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the data cleaner
        
        Args:
            api_key: OpenAI API key (if not provided, will try to get from env)
            model: OpenAI model to use for processing
        """
        # GET API KEY FROM ENVIRONMENT OR PARAMETER
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass it directly to the constructor."
            )
        
        # INITIALIZE OPENAI CLIENT
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # LOAD PROMPTS FROM CONFIG FILE
        self.prompts = self._load_prompts()
        
        print(f"INITIALIZED DATA CLEANER WITH MODEL: {model}")
    
    def _load_prompts(self):
        """Load prompts from config file"""
        config_path = Path("config/data_cleaner_prompts.txt")
        
        if not config_path.exists():
            raise FileNotFoundError(f"Prompt config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # PARSE SINGLE CLEANING PROMPT FROM CONFIG FILE
        prompts = {}
        if content.startswith('CLEANING_PROMPT_TEMPLATE:'):
            prompts['cleaning_prompt'] = content.replace('CLEANING_PROMPT_TEMPLATE:\n', '').strip()
        
        return prompts
    
    def _create_cleaning_prompt(self, enhanced_content: str) -> str:
        """Create the prompt for OpenAI to clean and standardize the enhanced markdown"""
        
        return f"""{self.prompts['cleaning_prompt']}

ENHANCED MARKDOWN CONTENT:
{enhanced_content}

JSON OUTPUT:"""

    async def process_file_async(self, markdown_file_path: str) -> ProcessedPage:
        """
        Process a single markdown file and return cleaned data
        
        Args:
            markdown_file_path: Path to the markdown file
            
        Returns:
            ProcessedPage: Cleaned and standardized data
        """
        file_path = Path(markdown_file_path)
        
        # READ THE MARKDOWN FILE
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print(f"PROCESSING FILE: {file_path.name}")
        
        # CREATE CLEANING PROMPT
        prompt = self._create_cleaning_prompt(markdown_content)
        
        try:
            # CALL OPENAI TO CLEAN THE DATA
            print("SENDING TO OPENAI FOR CLEANING...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert data cleaning agent specializing in technical document processing."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # LOW TEMPERATURE FOR CONSISTENT OUTPUT
                max_tokens=4000
            )
            
            # EXTRACT AND PARSE JSON RESPONSE
            json_content = response.choices[0].message.content
            if not json_content:
                raise ValueError("Empty response from OpenAI")
            cleaned_data = json.loads(json_content)
            
            # CONVERT TO STRUCTURED FORMAT
            tables = []
            for i, table_data in enumerate(cleaned_data.get("tables", [])):
                table = ProcessedTable(
                    table_id=table_data.get("table_id", f"table_{i+1}"),
                    title=table_data.get("title", ""),
                    description=table_data.get("description", ""),
                    columns=table_data.get("columns", []),
                    rows=table_data.get("rows", []),
                    metadata=table_data.get("metadata", {})
                )
                tables.append(table)
            
            # CREATE PROCESSED PAGE
            processed_page = ProcessedPage(
                page_id=file_path.stem,
                title=cleaned_data.get("title", file_path.stem),
                summary=cleaned_data.get("summary", ""),
                keywords=cleaned_data.get("keywords", []),
                tables=tables,
                raw_content=markdown_content,
                processing_metadata={
                    "source_file": str(file_path),
                    "processed_at": datetime.now().isoformat(),
                    "model_used": self.model,
                    "tables_found": len(tables)
                }
            )
            
            print(f"✅ CLEANED: {len(tables)} tables, {len(cleaned_data.get('keywords', []))} keywords")
            return processed_page
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON PARSING ERROR: {e}")
            print(f"RAW RESPONSE: {response.choices[0].message.content}")
            raise
        except Exception as e:
            print(f"❌ PROCESSING ERROR: {e}")
            raise
    
    def process_file(self, markdown_file_path: str) -> ProcessedPage:
        """Synchronous wrapper for file processing"""
        return asyncio.run(self.process_file_async(markdown_file_path))
    
    def process_folder(self, folder_path: str, output_file: Optional[str] = None) -> List[ProcessedPage]:
        """
        Process all markdown files in a folder
        
        Args:
            folder_path: Path to folder containing markdown files
            output_file: Optional path to save consolidated JSON output
            
        Returns:
            List[ProcessedPage]: All processed pages
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        # FIND ALL MARKDOWN FILES
        md_files = list(folder.glob("*.md"))
        if not md_files:
            raise ValueError(f"No markdown files found in: {folder_path}")
        
        print(f"FOUND {len(md_files)} MARKDOWN FILES TO PROCESS")
        
        # PROCESS EACH FILE
        processed_pages = []
        for md_file in sorted(md_files):
            try:
                processed_page = self.process_file(str(md_file))
                processed_pages.append(processed_page)
            except Exception as e:
                print(f"⚠️  FAILED TO PROCESS {md_file.name}: {e}")
                continue
        
        # SAVE CONSOLIDATED OUTPUT IF REQUESTED
        if output_file:
            self._save_processed_data(processed_pages, output_file)
        
        print(f"🎉 SUCCESSFULLY PROCESSED {len(processed_pages)}/{len(md_files)} FILES")
        return processed_pages
    
    def _save_processed_data(self, processed_pages: List[ProcessedPage], output_file: str):
        """Save processed data to JSON file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # CONVERT TO SERIALIZABLE FORMAT
        data = {
            "processed_at": datetime.now().isoformat(),
            "total_pages": len(processed_pages),
            "total_tables": sum(len(page.tables) for page in processed_pages),
            "pages": [asdict(page) for page in processed_pages]
        }
        
        # SAVE TO JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 SAVED PROCESSED DATA: {output_path}")
        print(f"   - {data['total_pages']} pages")
        print(f"   - {data['total_tables']} tables total")

    async def process_enhanced_document_async(self, enhanced_doc) -> ProcessedPage:
        """
        Process an enhanced document using only enhanced content (original kept as backup)
        
        Args:
            enhanced_doc: EnhancedDocument object with both versions
            
        Returns:
            ProcessedPage: Cleaned and standardized data
        """
        print(f"PROCESSING ENHANCED DOCUMENT: {enhanced_doc.filename}")
        
        # USE ENHANCED CONTENT FOR EXTRACTION
        prompt = self._create_cleaning_prompt(enhanced_doc.enhanced_content)
        
        try:
            # CALL OPENAI TO CLEAN THE ENHANCED DATA
            print("SENDING ENHANCED CONTENT TO OPENAI FOR CLEANING...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert data cleaning agent specializing in technical document processing."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # LOW TEMPERATURE FOR CONSISTENT OUTPUT
                max_tokens=4000   # STANDARD LIMIT FOR SINGLE DOCUMENT
            )
            
            # EXTRACT AND PARSE JSON RESPONSE
            json_content = response.choices[0].message.content
            if not json_content:
                raise ValueError("Empty response from OpenAI")
            cleaned_data = json.loads(json_content)
            
            # CONVERT TO STRUCTURED FORMAT
            tables = []
            for i, table_data in enumerate(cleaned_data.get("tables", [])):
                table = ProcessedTable(
                    table_id=table_data.get("table_id", f"table_{i+1}"),
                    title=table_data.get("title", ""),
                    description=table_data.get("description", ""),
                    columns=table_data.get("columns", []),
                    rows=table_data.get("rows", []),
                    metadata=table_data.get("metadata", {})
                )
                tables.append(table)
            
            # CREATE PROCESSED PAGE WITH ENHANCEMENT INFO
            processed_page = ProcessedPage(
                page_id=Path(enhanced_doc.filename).stem,
                title=cleaned_data.get("title", Path(enhanced_doc.filename).stem),
                summary=cleaned_data.get("summary", ""),
                keywords=cleaned_data.get("keywords", []),
                tables=tables,
                raw_content=enhanced_doc.enhanced_content,  # STORE ENHANCED VERSION
                processing_metadata={
                    "source_file": enhanced_doc.filename,
                    "processed_at": datetime.now().isoformat(),
                    "model_used": self.model,
                    "tables_found": len(tables),
                    "enhancement_applied": True,
                    "enhancement_notes": enhanced_doc.enhancement_notes,
                    "original_preserved": True,  # ORIGINAL CONTENT AVAILABLE AS BACKUP
                    "data_integrity": "Enhanced content with all data preserved"
                }
            )
            
            print(f"✅ ENHANCED-PROCESSED: {len(tables)} tables, {len(cleaned_data.get('keywords', []))} keywords")
            print(f"   📊 Using enhanced content with improved structure")
            print(f"   🔧 Structure enhancements: {len(enhanced_doc.enhancement_notes)}")
            print(f"   💾 Original content preserved as backup")
            return processed_page
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON PARSING ERROR: {e}")
            print(f"RAW RESPONSE: {response.choices[0].message.content}")
            raise
        except Exception as e:
            print(f"❌ PROCESSING ERROR: {e}")
            raise

    def process_enhanced_document(self, enhanced_doc) -> ProcessedPage:
        """Synchronous wrapper for enhanced document processing"""
        return asyncio.run(self.process_enhanced_document_async(enhanced_doc))

    def process_enhanced_documents(self, enhanced_docs: List, output_file: Optional[str] = None) -> List[ProcessedPage]:
        """
        Process a list of enhanced documents with dual content approach
        
        Args:
            enhanced_docs: List of EnhancedDocument objects
            output_file: Optional path to save consolidated JSON output
            
        Returns:
            List[ProcessedPage]: All processed pages with data integrity
        """
        print(f"PROCESSING {len(enhanced_docs)} ENHANCED DOCUMENTS WITH DUAL APPROACH")
        
        # PROCESS EACH ENHANCED DOCUMENT
        processed_pages = []
        for enhanced_doc in enhanced_docs:
            try:
                processed_page = self.process_enhanced_document(enhanced_doc)
                processed_pages.append(processed_page)
            except Exception as e:
                print(f"⚠️  FAILED TO PROCESS {enhanced_doc.filename}: {e}")
                continue
        
        # SAVE CONSOLIDATED OUTPUT IF REQUESTED
        if output_file:
            self._save_processed_data(processed_pages, output_file)
        
        print(f"🎉 SUCCESSFULLY PROCESSED {len(processed_pages)}/{len(enhanced_docs)} ENHANCED DOCUMENTS")
        return processed_pages


# CONVENIENCE FUNCTION FOR ONE-LINER USAGE
def clean_data_folder(folder_path: str, output_file: Optional[str] = None, model: str = "gpt-4") -> List[ProcessedPage]:
    """
    Simple function to clean a folder of markdown files
    
    Args:
        folder_path: Path to folder containing LlamaParse markdown output
        output_file: Optional path to save consolidated JSON
        model: OpenAI model to use
        
    Returns:
        List[ProcessedPage]: Cleaned and standardized pages
    """
    cleaner = DataCleaner(model=model)
    return cleaner.process_folder(folder_path, output_file)

# ENHANCED PIPELINE CONVENIENCE FUNCTION
def clean_enhanced_documents(enhanced_docs: List, output_file: Optional[str] = None, model: str = "gpt-4") -> List[ProcessedPage]:
    """
    Simple function to clean enhanced documents with dual approach
    
    Args:
        enhanced_docs: List of EnhancedDocument objects from markdown enhancer
        output_file: Optional path to save consolidated JSON
        model: OpenAI model to use
        
    Returns:
        List[ProcessedPage]: Cleaned and standardized pages with data integrity
    """
    cleaner = DataCleaner(model=model)
    return cleaner.process_enhanced_documents(enhanced_docs, output_file)


if __name__ == "__main__":
    # EXAMPLE USAGE
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_cleaner.py <folder_path> [output_file]")
        print("Example: python data_cleaner.py data/20250621_1726_premium/ cleaned_output.json")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        processed_pages = clean_data_folder(folder_path, output_file)
        print(f"\n✅ DATA CLEANING COMPLETE!")
        print(f"Processed {len(processed_pages)} pages")
        
        # PRINT SUMMARY
        for page in processed_pages:
            print(f"\n📄 {page.title}")
            print(f"   Summary: {page.summary[:100]}...")
            print(f"   Keywords: {', '.join(page.keywords[:3])}...")
            print(f"   Tables: {len(page.tables)}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1) 