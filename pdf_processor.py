"""
Simple PDF Processing Pipeline using LlamaParse
Sends PDFs to LlamaParse API and returns clean markdown documents
"""

import os
import asyncio
from pathlib import Path
from typing import Optional, List
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

class PDFProcessor:
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
        """Load prompts from config file"""
        config_path = Path("config/pdf_processor_prompts.txt")
        
        if not config_path.exists():
            raise FileNotFoundError(f"Prompt config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # PARSE PROMPTS FROM CONFIG FILE
        prompts = {}
        sections = content.split('\n\n')
        
        for section in sections:
            if section.startswith('SYSTEM_PROMPT_APPEND:'):
                prompts['system_prompt'] = section.replace('SYSTEM_PROMPT_APPEND:\n', '').strip()
            elif section.startswith('USER_PROMPT:'):
                prompts['user_prompt'] = section.replace('USER_PROMPT:\n', '').strip()
        
        return prompts
    
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
    
    def parse_pdf(self, pdf_path: str) -> List[ParsedDocument]:
        """
        Synchronous wrapper for PDF parsing
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List[ParsedDocument]: List of parsed documents
        """
        # RUN ASYNC FUNCTION SYNCHRONOUSLY
        return asyncio.run(self.parse_pdf_async(pdf_path))
    
    def save_parsed_documents(self, parsed_docs: List[ParsedDocument], output_dir: Optional[str] = None) -> List[str]:
        """
        Save parsed documents to organized data directory with timestamps
        
        Args:
            parsed_docs: List of ParsedDocument objects to save
            output_dir: Custom output directory (if None, will create timestamped directory)
            
        Returns:
            List[str]: Paths to the saved files
        """
        # CREATE ORGANIZED DATA DIRECTORY STRUCTURE
        if output_dir is None:
            # CREATE TIMESTAMPED DIRECTORY WITH MODE IDENTIFIER
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            mode_suffix = "premium" if self.use_premium else "standard"
            run_id = f"{timestamp}_{mode_suffix}"
            output_path = Path("data") / run_id
        else:
            output_path = Path(output_dir)
        
        # CREATE OUTPUT DIRECTORY
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        
        # SAVE EACH DOCUMENT TO A SEPARATE MARKDOWN FILE
        for doc in parsed_docs:
            output_file = output_path / doc.filename
            
            # CREATE MARKDOWN FILE WITH COMPREHENSIVE METADATA HEADER
            content_with_metadata = f"""# {Path(doc.filename).stem.replace('_', ' ').title()}

*Parsed from PDF using LlamaParse on {doc.parse_timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*Processing time: {doc.parsing_time_seconds:.2f} seconds*
*Mode: {'Premium' if self.use_premium else 'Standard'}*
*Run ID: {output_path.name}*

---

{doc.content}
"""
            
            # WRITE FILE TO DISK
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content_with_metadata)
            
            print(f"SAVED: {output_file}")
            saved_files.append(str(output_file))
        
        # CREATE METADATA FILE FOR THE RUN
        metadata_file = output_path / "run_metadata.json"
        run_metadata = {
            "run_id": output_path.name,
            "timestamp": datetime.now().isoformat(),
            "mode": "premium" if self.use_premium else "standard",
            "processing_time_seconds": parsed_docs[0].parsing_time_seconds if parsed_docs else 0,
            "document_count": len(parsed_docs),
            "files": [doc.filename for doc in parsed_docs]
        }
        
        import json
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(run_metadata, f, indent=2)
        
        print(f"SAVED RUN METADATA: {metadata_file}")
        print(f"DATA STORED IN: {output_path}")
        
        return saved_files


# SIMPLE CONVENIENCE FUNCTION FOR ONE-LINER USAGE
def process_pdf(pdf_path: str, output_dir: Optional[str] = None, use_premium: bool = False) -> List[str]:
    """
    Simple function to process a PDF and save the results
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Custom output directory (if None, creates timestamped directory in data/)
        use_premium: Whether to use Premium mode for better quality (costs more)
        
    Returns:
        List[str]: Paths to saved markdown files
    """
    # CREATE PROCESSOR AND PROCESS PDF IN ONE GO
    processor = PDFProcessor(use_premium=use_premium)
    parsed_docs = processor.parse_pdf(pdf_path)
    return processor.save_parsed_documents(parsed_docs, output_dir)