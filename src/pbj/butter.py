#!/usr/bin/env python3
"""
🧈 Butter - Markdown Enhancement Processor
=========================================

Stage 2 of the PB&J Pipeline. Enhances raw LlamaParse markdown with better structure,
improved column names, integrated footnotes, and standardized formatting using OpenAI.
"""

import os
import re
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES FROM .ENV FILE
load_dotenv()

# IMPORT CONFIGURATION
from .config import PipelineConfig

@dataclass
class EnhancedDocument:
    """Container for enhanced markdown document with original preserved"""
    enhanced_content: str
    original_content: str
    filename: str
    enhancement_timestamp: datetime
    enhancement_notes: List[str]

class Butter:
    """
    🧈 Butter - Markdown Enhancement Processor
    
    Stage 2 of the PB&J Pipeline. Enhances raw LlamaParse markdown with better structure,
    improved column names, integrated footnotes, and standardized formatting using OpenAI.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", config: Optional[PipelineConfig] = None):
        """
        Initialize the markdown enhancer
        
        Args:
            api_key: OpenAI API key (if not provided, will try to get from env)
            model: OpenAI model to use for enhancement
            config: PipelineConfig object with settings including max_tokens
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
        
        # SET MAX TOKENS FROM CONFIG WITH SAFETY CHECK
        if config and hasattr(config, 'max_tokens'):
            # SAFETY CHECK: PREVENT CONTEXT OVERFLOW
            self.max_tokens = min(config.max_tokens, 8192)
        else:
            self.max_tokens = 8192  # FALLBACK TO SAFE DEFAULT
        
        # LOAD PROMPTS FROM CONFIG FILE
        self.prompts = self._load_prompts()
        
        print(f"INITIALIZED MARKDOWN ENHANCER WITH MODEL: {model}, MAX_TOKENS: {self.max_tokens}")
    
    def _load_prompts(self):
        """Load prompts from pantry - much cleaner approach"""
        # GET PANTRY PATH RELATIVE TO THIS MODULE
        pantry_path = Path(__file__).parent / "pantry"
        prompt_path = pantry_path / "butter.txt"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Enhancement prompt file not found: {prompt_path}")
        
        # LOAD PROMPT FROM SIMPLE TEXT FILE
        with open(prompt_path, 'r', encoding='utf-8') as f:
            enhancement_prompt = f.read().strip()
        
        return {
            'enhancement_prompt': enhancement_prompt
        }
    
    def _create_enhancement_prompt(self, markdown_content: str) -> str:
        """Create the prompt for OpenAI to enhance the markdown structure only"""
        
        return f"""{self.prompts['enhancement_prompt']}

MARKDOWN CONTENT TO ENHANCE:
{markdown_content}

ENHANCED OUTPUT:"""

    async def enhance_markdown_async(self, markdown_content: str, filename: str) -> Optional[EnhancedDocument]:
        """
        Enhance a single markdown document
        
        Args:
            markdown_content: Raw markdown content from LlamaParse
            filename: Name of the source file
            
        Returns:
            EnhancedDocument: Enhanced markdown with improvements
        """
        print(f"ENHANCING MARKDOWN: {filename}")
        
        # Check if content needs chunking
        chunks = self._chunk_content(markdown_content, self.max_tokens)
        
        if len(chunks) == 1:
            # No chunking needed - process normally
            return await self._enhance_single_chunk(chunks[0], filename)
        else:
            # Chunking required - process each chunk and merge
            print(f"🔄 PROCESSING {len(chunks)} CHUNKS FOR LARGE DOCUMENT")
            enhanced_chunks = []
            
            for i, chunk in enumerate(chunks):
                print(f"   📄 PROCESSING CHUNK {i+1}/{len(chunks)}")
                enhanced_chunk = await self._enhance_single_chunk(chunk, f"{filename}_chunk_{i+1}")
                if enhanced_chunk:
                    enhanced_chunks.append(enhanced_chunk)
            
            if not enhanced_chunks:
                print(f"❌ ALL CHUNKS FAILED TO ENHANCE")
                return None
            
            # Merge enhanced chunks
            merged_content = "\n\n---\n\n".join([chunk.enhanced_content for chunk in enhanced_chunks])
            merged_notes = []
            for chunk in enhanced_chunks:
                merged_notes.extend(chunk.enhancement_notes)
            
            # Create merged enhanced document
            enhanced_doc = EnhancedDocument(
                enhanced_content=merged_content,
                original_content=markdown_content,
                filename=filename,
                enhancement_timestamp=datetime.now(),
                enhancement_notes=merged_notes
            )
            
            print(f"✅ ENHANCED: {len(merged_notes)} improvements across {len(chunks)} chunks")
            return enhanced_doc
    
    async def _enhance_single_chunk(self, markdown_content: str, filename: str) -> Optional[EnhancedDocument]:
        """
        Enhance a single chunk of markdown content
        """
        # CREATE ENHANCEMENT PROMPT
        prompt = self._create_enhancement_prompt(markdown_content)
        
        try:
            # CALL OPENAI TO ENHANCE THE MARKDOWN
            print("SENDING TO OPENAI FOR ENHANCEMENT...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert document enhancement specialist focusing on technical and medical documents."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,  # ZERO TEMPERATURE FOR DETERMINISTIC OUTPUT
                max_tokens=self.max_tokens   # USE MAX_TOKENS FROM CONFIG
            )
            
            # EXTRACT ENHANCED CONTENT
            enhanced_content = response.choices[0].message.content
            if not enhanced_content:
                raise ValueError("Empty response from OpenAI")
            
            # SAFETY CHECK: DETECT HTML COMMENTS AND FALLBACK TO ORIGINAL
            if '<!--' in enhanced_content and '-->' in enhanced_content:
                print(f"⚠️  WARNING: HTML comments detected in enhanced content for {filename}")
                print(f"   Falling back to original markdown to preserve data integrity")
                print(f"   HTML comment found: {enhanced_content[enhanced_content.find('<!--'):enhanced_content.find('<!--')+100]}...")
                enhanced_content = markdown_content  # FALLBACK TO ORIGINAL
            
            # ANALYZE ENHANCEMENTS MADE
            enhancement_notes = self._analyze_enhancements(markdown_content, enhanced_content)
            
            # CREATE ENHANCED DOCUMENT
            enhanced_doc = EnhancedDocument(
                enhanced_content=enhanced_content,
                original_content=markdown_content,
                filename=filename,
                enhancement_timestamp=datetime.now(),
                enhancement_notes=enhancement_notes
            )
            
            print(f"✅ ENHANCED: {len(enhancement_notes)} improvements made")
            for note in enhancement_notes[:3]:  # SHOW FIRST 3 IMPROVEMENTS
                print(f"   - {note}")
            
            return enhanced_doc
            
        except Exception as e:
            print(f"❌ ENHANCEMENT ERROR: {e}")
            print(f"   Skipping chunk {filename} due to error")
            return None  # Return None instead of raising to allow pipeline to continue
    
    def _analyze_enhancements(self, original: str, enhanced: str) -> List[str]:
        """Analyze what enhancements were made"""
        notes = []
        
        # CHECK FOR HEADER IMPROVEMENTS
        original_headers = re.findall(r'<th[^>]*>([^<]+)</th>', original)
        enhanced_headers = re.findall(r'<th[^>]*>([^<]+)</th>', enhanced)
        
        if len(enhanced_headers) > 0 and enhanced_headers != original_headers:
            notes.append("Improved table column names with descriptive labels")
              # CHECK FOR STRUCTURE CLEANUP
        enhanced_lines = len(enhanced.split('\n'))
        original_lines = len(original.split('\n'))
        if abs(enhanced_lines - original_lines) > 5:
            notes.append("Restructured document for better organization")
        
        return notes or ["General formatting and structure improvements"]
    
    def process(self, markdown_content: str, filename: str = "document.md") -> Optional[EnhancedDocument]:
        """
        🧈 Process Markdown → Enhanced Markdown
        Main Butter processing method
        """
        return asyncio.run(self.enhance_markdown_async(markdown_content, filename))
    
    def process_async(self, markdown_content: str, filename: str = "document.md") -> Optional[EnhancedDocument]:
        """
        🧈 Async Process Markdown → Enhanced Markdown
        Async Butter processing method
        """
        return asyncio.run(self.enhance_markdown_async(markdown_content, filename))
    
    def process_file(self, markdown_file_path: str) -> Optional[EnhancedDocument]:
        """
        🧈 Process markdown file → Enhanced markdown
        File-based Butter processing method
        """
        file_path = Path(markdown_file_path)
        
        # READ THE MARKDOWN FILE
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        return self.process(markdown_content, file_path.name)
    
    def process_folder(self, folder_path: str, output_dir: Optional[str] = None) -> List[EnhancedDocument]:
        """
        🧈 Process folder → Enhanced documents
        Folder-based Butter processing method
        """
        folder = Path(folder_path)
        
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        # FIND ALL MARKDOWN FILES
        markdown_files = list(folder.glob("*.md"))
        if not markdown_files:
            raise ValueError(f"No markdown files found in: {folder_path}")
        
        print(f"FOUND {len(markdown_files)} MARKDOWN FILES TO ENHANCE")
        
        enhanced_docs = []
        for md_file in markdown_files:
            try:
                enhanced_doc = self.process_file(str(md_file))
                if enhanced_doc is not None:
                    enhanced_docs.append(enhanced_doc)
                    print(f"✅ ENHANCED: {md_file.name}")
                else:
                    print(f"⚠️  SKIPPED: {md_file.name} (enhancement failed)")
            except Exception as e:
                print(f"❌ FAILED TO ENHANCE {md_file.name}: {e}")
                continue
        
        # SAVE ENHANCED DOCUMENTS IF OUTPUT DIR SPECIFIED
        if output_dir:
            self._save_enhanced_documents(enhanced_docs, output_dir, str(folder))
        
        return enhanced_docs
    
    def _process_document_folder(self, document_folder_path: str) -> List[EnhancedDocument]:
        """
        🧈 INTERNAL: Process document folder → Enhanced documents
        Internal pipeline method - not intended for direct user calls
        """
        doc_folder = Path(document_folder_path)
        
        if not doc_folder.exists():
            raise FileNotFoundError(f"Document folder not found: {document_folder_path}")
        
        # LOOK FOR PARSED MARKDOWN FOLDER (STAGE 1 OUTPUT)
        parsed_folder = doc_folder / "01_parsed_markdown"
        
        if not parsed_folder.exists():
            raise FileNotFoundError(f"Parsed markdown folder not found: {parsed_folder}")
        
        # FIND ALL MARKDOWN FILES IN PARSED FOLDER
        markdown_files = list(parsed_folder.glob("*.md"))
        if not markdown_files:
            raise ValueError(f"No markdown files found in: {parsed_folder}")
        
        print(f"ENHANCING {len(markdown_files)} PARSED DOCUMENTS")
        
        # CREATE ENHANCED FOLDER
        enhanced_folder = doc_folder / "02_enhanced_markdown"
        enhanced_folder.mkdir(exist_ok=True)
        
        enhanced_docs = []
        skipped_pages = []
        for md_file in markdown_files:
            try:
                enhanced_doc = self.process_file(str(md_file))
                if enhanced_doc is None:
                    # Page was skipped due to error
                    skipped_pages.append({
                        "filename": md_file.name,
                        "error": "Enhancement failed - page skipped",
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"⚠️  SKIPPED: {md_file.name} (enhancement failed)")
                    continue
                    
                enhanced_docs.append(enhanced_doc)
                
                # SAVE EACH ENHANCED DOCUMENT IMMEDIATELY (PAGE-WISE SAVING)
                self._save_single_enhanced_document(enhanced_doc, enhanced_folder, doc_folder.name)
                
                print(f"✅ ENHANCED AND SAVED: {md_file.name}")
            except Exception as e:
                print(f"❌ FAILED TO ENHANCE {md_file.name}: {e}")
                skipped_pages.append({
                    "filename": md_file.name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                continue
        
        # UPDATE DOCUMENT METADATA
        self._update_document_metadata(doc_folder, "enhancement", enhanced_docs, skipped_pages)
        
        print(f"✅ ENHANCED AND SAVED {len(enhanced_docs)} DOCUMENTS TO: {enhanced_folder}")
        
        return enhanced_docs

    def _save_single_enhanced_document(self, enhanced_doc: EnhancedDocument, output_folder: Path, document_id: str):
        """Save a single enhanced document immediately after processing"""
        output_file = output_folder / enhanced_doc.filename
        
        # ADD ENHANCEMENT METADATA HEADER
        content_with_metadata = f"""# {Path(enhanced_doc.filename).stem.replace('_', ' ').title()} (Enhanced)

*Enhanced on {enhanced_doc.enhancement_timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*Document ID: {document_id}*
*Enhancements applied: {len(enhanced_doc.enhancement_notes)}*

**Enhancement Notes:**
{chr(10).join(f'- {note}' for note in enhanced_doc.enhancement_notes)}

---

{enhanced_doc.enhanced_content}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content_with_metadata)
        
        print(f"SAVED ENHANCED PAGE: {output_file}")

    def _update_document_metadata(self, doc_folder: Path, stage: str, enhanced_docs: List[EnhancedDocument], skipped_pages: List[Dict[str, Any]]):
        """Update the document metadata with completed stage info"""
        metadata_file = doc_folder / "document_metadata.json"
        
        if metadata_file.exists():
            import json
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # ENSURE stages_completed FIELD EXISTS
            if "stages_completed" not in metadata:
                metadata["stages_completed"] = []
            
            # UPDATE STAGES COMPLETED
            if stage not in metadata["stages_completed"]:
                metadata["stages_completed"].append(stage)
            
            # ADD ENHANCEMENT INFO
            metadata[f"{stage}_info"] = {
                "enhanced_at": datetime.now().isoformat(),
                "files_enhanced": len(enhanced_docs),
                "enhancement_summary": {
                    doc.filename: doc.enhancement_notes 
                    for doc in enhanced_docs
                },
                "skipped_pages": skipped_pages
            }
            
            # SAVE UPDATED METADATA
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"UPDATED DOCUMENT METADATA: {metadata_file}")
        else:
            print(f"WARNING: No metadata file found at {metadata_file}")
    
    def _save_enhanced_documents(self, enhanced_docs: List[EnhancedDocument], output_dir: str, source_folder: str):
        """Save enhanced documents to directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        
        for doc in enhanced_docs:
            # SAVE ENHANCED MARKDOWN
            output_file = output_path / doc.filename
            
            # ADD ENHANCEMENT METADATA HEADER
            content_with_metadata = f"""# {Path(doc.filename).stem.replace('_', ' ').title()} (Enhanced)

*Enhanced from {source_folder} on {doc.enhancement_timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*Enhancements applied: {len(doc.enhancement_notes)}*

**Enhancement Notes:**
{chr(10).join(f'- {note}' for note in doc.enhancement_notes)}

---

{doc.enhanced_content}
"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content_with_metadata)
            
            print(f"SAVED ENHANCED: {output_file}")
            saved_files.append(str(output_file))
        
        # CREATE ENHANCEMENT METADATA
        metadata_file = output_path / "enhancement_metadata.json"
        enhancement_metadata = {
            "source_folder": source_folder,
            "enhanced_at": datetime.now().isoformat(),
            "total_files": len(enhanced_docs),
            "enhancements": {
                doc.filename: doc.enhancement_notes 
                for doc in enhanced_docs
            }
        }
        
        import json
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(enhancement_metadata, f, indent=2)
        
        print(f"SAVED ENHANCEMENT METADATA: {metadata_file}")
        print(f"ENHANCED DOCUMENTS STORED IN: {output_path}")

    def _estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (4 chars ≈ 1 token)
        Includes safety margin for prompt overhead
        """
        # Rough estimation: 4 characters ≈ 1 token
        base_tokens = len(text) // 4
        
        # Add safety margin for prompt overhead (system + user prompts)
        prompt_overhead = 500  # Conservative estimate for prompt tokens
        
        return base_tokens + prompt_overhead
    
    def _detect_table_boundaries(self, content: str) -> List[tuple]:
        """
        Detect table boundaries to avoid splitting tables
        Returns list of (start_pos, end_pos) for each table
        """
        table_boundaries = []
        
        # Look for HTML tables
        import re
        table_pattern = r'<table[^>]*>.*?</table>'
        for match in re.finditer(table_pattern, content, re.DOTALL):
            table_boundaries.append((match.start(), match.end()))
        
        # Look for markdown tables (lines with | characters)
        lines = content.split('\n')
        table_start = None
        
        for i, line in enumerate(lines):
            if '|' in line and line.strip().startswith('|') or line.strip().endswith('|'):
                if table_start is None:
                    table_start = i
            elif table_start is not None:
                # End of table found
                table_boundaries.append((table_start, i))
                table_start = None
        
        # Handle table that ends at end of content
        if table_start is not None:
            table_boundaries.append((table_start, len(lines)))
        
        return table_boundaries
    
    def _chunk_content(self, content: str, max_tokens: int) -> List[str]:
        """
        Split content into chunks that fit within token limit
        NEVER splits tables - keeps them together
        """
        if self._estimate_tokens(content) <= max_tokens:
            return [content]  # No chunking needed
        
        print(f"📏 CONTENT TOO LARGE ({self._estimate_tokens(content)} tokens), CHUNKING REQUIRED")
        
        # Detect table boundaries
        table_boundaries = self._detect_table_boundaries(content)
        print(f"   📊 FOUND {len(table_boundaries)} TABLES TO PRESERVE")
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        # Split by paragraphs, respecting table boundaries
        paragraphs = content.split('\n\n')
        
        # Track character position for accurate table detection
        char_pos = 0
        
        for paragraph in paragraphs:
            paragraph_tokens = self._estimate_tokens(paragraph)
            
            # Check if this paragraph contains a table by checking if any table boundary overlaps
            paragraph_start = char_pos
            paragraph_end = char_pos + len(paragraph)
            
            paragraph_has_table = any(
                (start <= paragraph_start and end >= paragraph_start) or  # Table starts before paragraph
                (start <= paragraph_end and end >= paragraph_end) or      # Table ends after paragraph  
                (start >= paragraph_start and end <= paragraph_end)       # Table is completely within paragraph
                for start, end in table_boundaries
            )
            
            # If adding this paragraph would exceed limit
            if current_tokens + paragraph_tokens > max_tokens:
                # If current chunk is not empty, save it
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    print(f"   📄 CHUNK {len(chunks)}: {self._estimate_tokens(current_chunk)} tokens")
                
                # Start new chunk
                current_chunk = paragraph
                current_tokens = paragraph_tokens
                
                # If single paragraph is too large, we have a problem
                if paragraph_tokens > max_tokens:
                    print(f"⚠️  WARNING: Single paragraph too large ({paragraph_tokens} tokens)")
                    if paragraph_has_table:
                        print(f"   🚨 CRITICAL: Large paragraph contains table - cannot split safely!")
                        print(f"   This may cause token limit issues")
                    # Split at sentence level as fallback
                    sentences = paragraph.split('. ')
                    current_chunk = ""
                    current_tokens = 0
                    for sentence in sentences:
                        sentence_tokens = self._estimate_tokens(sentence)
                        if current_tokens + sentence_tokens > max_tokens:
                            if current_chunk.strip():
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence
                            current_tokens = sentence_tokens
                        else:
                            current_chunk += ". " + sentence if current_chunk else sentence
                            current_tokens += sentence_tokens
            else:
                # Add to current chunk
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
                current_tokens += paragraph_tokens
            
            # Update character position for next iteration
            char_pos += len(paragraph) + 2  # +2 for the \n\n separator
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            print(f"   📄 CHUNK {len(chunks)}: {self._estimate_tokens(current_chunk)} tokens")
        
        print(f"✅ SPLIT INTO {len(chunks)} CHUNKS")
        return chunks





 