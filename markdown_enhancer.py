#!/usr/bin/env python3
"""
Markdown Enhancement Pipeline
============================

STAGE 2: ENHANCE LLAMAPARSE MARKDOWN WITH BETTER CONTEXT AND STRUCTURE
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

@dataclass
class EnhancedDocument:
    """Container for enhanced markdown document with original preserved"""
    enhanced_content: str
    original_content: str
    filename: str
    enhancement_timestamp: datetime
    enhancement_notes: List[str]

class MarkdownEnhancer:
    """
    INTELLIGENT MARKDOWN ENHANCEMENT USING OPENAI
    
    Takes raw LlamaParse markdown and enhances it with:
    - Better column names from document context
    - Integrated footnotes and legends
    - Standardized formatting
    - Cross-reference resolution
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the markdown enhancer
        
        Args:
            api_key: OpenAI API key (if not provided, will try to get from env)
            model: OpenAI model to use for enhancement
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
        
        print(f"INITIALIZED MARKDOWN ENHANCER WITH MODEL: {model}")
    
    def _load_prompts(self):
        """Load prompts from config file"""
        config_path = Path("config/markdown_enhancer_prompts.txt")
        
        if not config_path.exists():
            raise FileNotFoundError(f"Prompt config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # PARSE PROMPTS FROM CONFIG FILE
        prompts = {}
        if content.startswith('ENHANCEMENT_PROMPT_TEMPLATE:'):
            prompts['enhancement_prompt'] = content.replace('ENHANCEMENT_PROMPT_TEMPLATE:\n', '').strip()
        
        return prompts
    
    def _create_enhancement_prompt(self, markdown_content: str) -> str:
        """Create the prompt for OpenAI to enhance the markdown structure only"""
        
        return self.prompts['enhancement_prompt'].format(markdown_content=markdown_content)

    async def enhance_markdown_async(self, markdown_content: str, filename: str) -> EnhancedDocument:
        """
        Enhance a single markdown document
        
        Args:
            markdown_content: Raw markdown content from LlamaParse
            filename: Name of the source file
            
        Returns:
            EnhancedDocument: Enhanced markdown with improvements
        """
        print(f"ENHANCING MARKDOWN: {filename}")
        
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
                temperature=0.1,  # LOW TEMPERATURE FOR CONSISTENT OUTPUT
                max_tokens=6000   # HIGHER LIMIT FOR LONGER DOCUMENTS
            )
            
            # EXTRACT ENHANCED CONTENT
            enhanced_content = response.choices[0].message.content
            if not enhanced_content:
                raise ValueError("Empty response from OpenAI")
            
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
            raise
    
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
    
    def enhance_markdown(self, markdown_content: str, filename: str) -> EnhancedDocument:
        """Synchronous wrapper for markdown enhancement"""
        return asyncio.run(self.enhance_markdown_async(markdown_content, filename))
    
    def enhance_file(self, markdown_file_path: str) -> EnhancedDocument:
        """
        Enhance a single markdown file
        
        Args:
            markdown_file_path: Path to the markdown file
            
        Returns:
            EnhancedDocument: Enhanced markdown
        """
        file_path = Path(markdown_file_path)
        
        # READ THE MARKDOWN FILE
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        return self.enhance_markdown(markdown_content, file_path.name)
    
    def enhance_folder(self, folder_path: str, output_dir: Optional[str] = None) -> List[EnhancedDocument]:
        """
        Enhance all markdown files in a folder
        
        Args:
            folder_path: Path to folder containing raw markdown files
            output_dir: Optional directory to save enhanced markdown files
            
        Returns:
            List[EnhancedDocument]: All enhanced documents
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        # FIND ALL MARKDOWN FILES
        md_files = list(folder.glob("*.md"))
        if not md_files:
            raise ValueError(f"No markdown files found in: {folder_path}")
        
        print(f"FOUND {len(md_files)} MARKDOWN FILES TO ENHANCE")
        
        # PROCESS EACH FILE
        enhanced_docs = []
        for md_file in sorted(md_files):
            try:
                enhanced_doc = self.enhance_file(str(md_file))
                enhanced_docs.append(enhanced_doc)
            except Exception as e:
                print(f"⚠️  FAILED TO ENHANCE {md_file.name}: {e}")
                continue
        
        # SAVE ENHANCED FILES IF REQUESTED
        if output_dir:
            self._save_enhanced_documents(enhanced_docs, output_dir, folder.name)
        
        print(f"🎉 SUCCESSFULLY ENHANCED {len(enhanced_docs)}/{len(md_files)} FILES")
        return enhanced_docs
    
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


# CONVENIENCE FUNCTION FOR ONE-LINER USAGE
def enhance_markdown_folder(folder_path: str, output_dir: Optional[str] = None, model: str = "gpt-4") -> List[EnhancedDocument]:
    """
    Simple function to enhance a folder of markdown files
    
    Args:
        folder_path: Path to folder containing raw LlamaParse markdown
        output_dir: Optional directory to save enhanced files
        model: OpenAI model to use
        
    Returns:
        List[EnhancedDocument]: Enhanced documents
    """
    enhancer = MarkdownEnhancer(model=model)
    return enhancer.enhance_folder(folder_path, output_dir)


if __name__ == "__main__":
    # EXAMPLE USAGE
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python markdown_enhancer.py <folder_path> [output_dir]")
        print("Example: python markdown_enhancer.py data/20250621_1726_premium/ data/enhanced_20250621_1726_premium/")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        enhanced_docs = enhance_markdown_folder(folder_path, output_dir)
        print(f"\n✅ MARKDOWN ENHANCEMENT COMPLETE!")
        print(f"Enhanced {len(enhanced_docs)} documents")
        
        # PRINT SUMMARY
        for doc in enhanced_docs:
            print(f"\n📄 {doc.filename}")
            print(f"   Enhancements: {len(doc.enhancement_notes)}")
            for note in doc.enhancement_notes[:2]:
                print(f"     - {note}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1) 