"""
🥜 Peanut - Parse PDFs to Markdown
=================================

The Parse stage of the PB&J Pipeline. Extracts raw content from PDFs 
using LlamaParse API and returns clean markdown documents.
"""

import os
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from llama_parse import LlamaParse
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES FROM .ENV FILE
load_dotenv()

@dataclass
class ParsedDocument:
    """Container for parsed document data"""
    content: str
    filename: str
    parse_timestamp: datetime
    parsing_time_seconds: float

class Peanut:
    """
    Simple PDF processor using LlamaParse
    Optimized for technical and table-heavy documents
    """
    
    def __init__(self, api_key: Optional[str] = None, use_premium: bool = False):
        """
        Initialize the PDF processor
        
        Args:
            api_key: LlamaParse API key (if not provided, will try to get from env)
            use_premium: Whether to use Premium mode for better parsing quality (costs more)
        """
        # GET API KEY FROM ENVIRONMENT OR PARAMETER
        self.api_key = api_key or os.getenv("LLAMA_CLOUD_API_KEY")
        if not self.api_key:
            raise ValueError(
                "LlamaParse API key is required. Set LLAMA_CLOUD_API_KEY environment variable "
                "or pass it directly to the constructor."
            )
        
        # LOAD PROMPTS FROM CONFIG FILE
        prompts = self._load_prompts()
        
        # CONFIGURE LLAMAPARSE WITH OPTIMIZED SETTINGS FOR TECHNICAL DOCUMENTS
        # USING NEW API PARAMETERS INSTEAD OF DEPRECATED parsing_instruction
        self.parser = LlamaParse(
            api_key=self.api_key,
            result_type="markdown",  # OUTPUT FORMAT AS MARKDOWN
            verbose=True,            # ENABLE VERBOSE LOGGING
            language="en",           # SET LANGUAGE TO ENGLISH
            
            # PAGE BREAK CONFIGURATION - LLAMAPARSE HAS BUILT-IN PAGE SEPARATOR SUPPORT
            page_separator="\n---\n",  # USE HORIZONTAL RULES FOR PAGE BREAKS
            
            # NEW API: USE system_prompt_append INSTEAD OF DEPRECATED parsing_instruction
            # THIS APPENDS TO LLAMAPARSE'S SYSTEM PROMPT INSTEAD OF REPLACING IT
            system_prompt_append=prompts['system_prompt'],
            
            # ADD USER PROMPT FOR TABLE AND DATA EXTRACTION
            user_prompt=prompts['user_prompt'],
            
            # PREMIUM MODE SETTINGS FOR BETTER PARSING QUALITY
            premium_mode=use_premium,  # ENABLE PREMIUM MODE FOR COMPLEX DOCUMENTS
            
            # OTHER OPTIMIZATIONS FOR TECHNICAL DOCUMENTS
            output_tables_as_HTML=True,  # USE HTML TABLES FOR COMPLEX TABLE STRUCTURES
            
            # ADDITIONAL OPTIONS FOR BETTER CHECKBOX/BULLET DETECTION
            disable_ocr=False,  # ENSURE OCR IS ENABLED TO DETECT FAINT MARKS
            skip_diagonal_text=False,  # DON'T SKIP DIAGONAL TEXT THAT MIGHT BE CHECKMARKS
            
            max_timeout=180,  # 3 MINUTES TIMEOUT FOR PREMIUM MODE
        )
        
        # STORE MODE FOR REPORTING
        self.use_premium = use_premium
    
    def _load_prompts(self):
        """Load prompts from pantry - much cleaner approach"""
        # GET PANTRY PATH RELATIVE TO THIS MODULE
        pantry_path = Path(__file__).parent / "pantry"
        system_prompt_path = pantry_path / "pea.txt"
        user_prompt_path = pantry_path / "nut.txt"
        
        # CHECK IF FILES EXIST
        if not system_prompt_path.exists():
            raise FileNotFoundError(f"System prompt file not found: {system_prompt_path}")
        if not user_prompt_path.exists():
            raise FileNotFoundError(f"User prompt file not found: {user_prompt_path}")
        
        # LOAD PROMPTS FROM SIMPLE TEXT FILES
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()
        
        with open(user_prompt_path, 'r', encoding='utf-8') as f:
            user_prompt = f.read().strip()
        
        return {
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }
    
    async def parse_pdf_async(self, pdf_path: str) -> List[ParsedDocument]:
        """
        Asynchronously parse a PDF file using LlamaParse
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List[ParsedDocument]: List of parsed documents (one per page/section if split)
        """
        # VALIDATE PDF FILE EXISTS AND IS CORRECT FORMAT
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_file.suffix.lower() == '.pdf':
            raise ValueError(f"File must be a PDF: {pdf_path}")
        
        # START PROCESSING WITH TIMING
        mode_text = "PREMIUM" if self.use_premium else "BALANCED"
        print(f"STARTING PDF PARSING WITH {mode_text} MODE: {pdf_file.name}")
        start_time = datetime.now()
        
        try:
            # SEND PDF TO LLAMAPARSE API - LET LLAMAPARSE HANDLE ALL THE HEAVY LIFTING
            print("SENDING PDF TO LLAMAPARSE API...")
            documents = await self.parser.aload_data(str(pdf_file))
            
            # CHECK IF WE GOT ANY CONTENT BACK
            if not documents:
                raise ValueError("NO CONTENT EXTRACTED FROM PDF")
            
            # CALCULATE PROCESSING TIME
            end_time = datetime.now()
            parsing_time = (end_time - start_time).total_seconds()
            
            # CONVERT LLAMAPARSE DOCUMENTS TO OUR FORMAT
            parsed_docs = []
            for i, doc in enumerate(documents):
                # CREATE PARSED DOCUMENT OBJECT
                parsed_doc = ParsedDocument(
                    content=doc.text,  # LLAMAPARSE ALREADY RETURNS CLEAN MARKDOWN WITH PAGE BREAKS
                    filename=f"{pdf_file.stem}_part_{i+1}.md" if len(documents) > 1 else f"{pdf_file.stem}.md",
                    parse_timestamp=end_time,
                    parsing_time_seconds=parsing_time
                )
                parsed_docs.append(parsed_doc)
            
            # PRINT SUCCESS STATISTICS
            print(f"SUCCESSFULLY PARSED PDF IN {parsing_time:.2f} SECONDS")
            print(f"EXTRACTED {len(parsed_docs)} DOCUMENT(S)")
            for i, doc in enumerate(parsed_docs):
                print(f"   - PART {i+1}: {len(doc.content)} CHARACTERS")
            
            return parsed_docs
            
        except Exception as e:
            # PRINT ERROR AND RE-RAISE
            print(f"ERROR PARSING PDF {pdf_file.name}: {str(e)}")
            raise
    
    def process(self, pdf_path: str) -> List[ParsedDocument]:
        """
        🥜 Process PDF → Markdown
        Main Peanut processing method
        """
        return asyncio.run(self.parse_pdf_async(pdf_path))
    
    def process_async(self, pdf_path: str) -> List[ParsedDocument]:
        """
        🥜 Async Process PDF → Markdown
        Async Peanut processing method
        """
        return asyncio.run(self.parse_pdf_async(pdf_path))
    
    def save_parsed_documents(self, parsed_docs: List[ParsedDocument], output_dir: Optional[str] = None, source_pdf_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Save parsed documents to organized per-document directory structure
        
        Args:
            parsed_docs: List of ParsedDocument objects to save
            output_dir: Custom output directory (if None, will create timestamped directory)
            source_pdf_path: Path to original PDF file to copy to output
            
        Returns:
            Dict[str, Any]: Information about the created directory structure
        """
        # CREATE ORGANIZED PER-DOCUMENT DIRECTORY STRUCTURE
        if output_dir is None:
            # CREATE TIMESTAMPED DIRECTORY WITH MODE IDENTIFIER
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode_suffix = "premium" if self.use_premium else "standard"
            if source_pdf_path:
                pdf_name = Path(source_pdf_path).stem
                run_id = f"{pdf_name}_{timestamp}_{mode_suffix}"
            else:
                run_id = f"document_{timestamp}_{mode_suffix}"
            output_path = Path("data") / run_id
        else:
            output_path = Path(output_dir)
        
        # CREATE MAIN DOCUMENT DIRECTORY
        output_path.mkdir(parents=True, exist_ok=True)
        
        # CREATE SUBDIRECTORIES FOR ORGANIZED STORAGE
        parsed_md_dir = output_path / "01_parsed_markdown"
        parsed_md_dir.mkdir(exist_ok=True)
        
        # COPY ORIGINAL PDF TO DOCUMENT FOLDER
        if source_pdf_path and Path(source_pdf_path).exists():
            import shutil
            pdf_dest = output_path / Path(source_pdf_path).name
            shutil.copy2(source_pdf_path, pdf_dest)
            print(f"COPIED ORIGINAL PDF: {pdf_dest}")
        
        saved_files = []
        
        # SAVE EACH DOCUMENT TO PARSED MARKDOWN SUBFOLDER
        for doc in parsed_docs:
            output_file = parsed_md_dir / doc.filename
            
            # CREATE MARKDOWN FILE WITH COMPREHENSIVE METADATA HEADER
            content_with_metadata = f"""# {Path(doc.filename).stem.replace('_', ' ').title()}

*Parsed from PDF using LlamaParse on {doc.parse_timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*Processing time: {doc.parsing_time_seconds:.2f} seconds*
*Mode: {'Premium' if self.use_premium else 'Standard'}*
*Document ID: {output_path.name}*

---

{doc.content}
"""
            
            # WRITE FILE TO DISK
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content_with_metadata)
            
            print(f"SAVED PARSED PAGE: {output_file}")
            saved_files.append(str(output_file))
        
        # CREATE METADATA FILE FOR THE DOCUMENT
        metadata_file = output_path / "document_metadata.json"
        document_metadata = {
            "document_id": output_path.name,
            "timestamp": datetime.now().isoformat(),
            "source_pdf": Path(source_pdf_path).name if source_pdf_path else None,
            "parsing_mode": "premium" if self.use_premium else "standard",
            "processing_time_seconds": parsed_docs[0].parsing_time_seconds if parsed_docs else 0,
            "page_count": len(parsed_docs),
            "stages_completed": ["01_parsed_markdown"],
            "directory_structure": {
                "main_folder": str(output_path),
                "original_pdf": str(output_path / Path(source_pdf_path).name) if source_pdf_path else None,
                "parsed_markdown": str(parsed_md_dir),
                "enhanced_markdown": str(output_path / "02_enhanced_markdown"),
                "cleaned_json": str(output_path / "03_cleaned_json"),
                "final_output": str(output_path / "final_output.json")
            },
            "files": [doc.filename for doc in parsed_docs]
        }
        
        import json
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(document_metadata, f, indent=2)
        
        print(f"SAVED DOCUMENT METADATA: {metadata_file}")
        print(f"DOCUMENT FOLDER CREATED: {output_path}")
        print(f"STAGE 1 COMPLETE - PARSED MARKDOWN SAVED IN: {parsed_md_dir}")
        
        return {
            "document_id": output_path.name,
            "main_folder": str(output_path),
            "parsed_markdown_folder": str(parsed_md_dir),
            "saved_files": saved_files,
            "metadata_file": str(metadata_file)
        }


