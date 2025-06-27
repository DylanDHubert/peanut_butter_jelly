#!/usr/bin/env python3
"""
Test script for Butter chunking functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pbj.butter import Butter
from pbj.peanut import Peanut

def test_chunking():
    """Test chunking with artificially large content"""
    
    # Get page 3 content
    print("📄 EXTRACTING PAGE 3 FROM PDF...")
    peanut = Peanut()
    docs = peanut.process('data/pb&j.pdf')
    page3_content = docs[2].content
    
    print(f"📏 ORIGINAL PAGE 3: {len(page3_content)} characters (~{len(page3_content) // 4} tokens)")
    
    # Create artificially large content by repeating page 3
    large_content = page3_content * 10  # 10x larger
    print(f"📏 ARTIFICIALLY LARGE CONTENT: {len(large_content)} characters (~{len(large_content) // 4} tokens)")
    
    # Test chunking with different max_tokens values
    butter = Butter()
    
    # Test 1: Small max_tokens to force chunking
    print("\n🧪 TEST 1: Small max_tokens (1000) to force chunking")
    chunks_small = butter._chunk_content(large_content, 1000)
    print(f"   Result: {len(chunks_small)} chunks")
    for i, chunk in enumerate(chunks_small):
        tokens = butter._estimate_tokens(chunk)
        print(f"   Chunk {i+1}: {len(chunk)} chars, ~{tokens} tokens")
    
    # Test 2: Medium max_tokens
    print("\n🧪 TEST 2: Medium max_tokens (3000)")
    chunks_medium = butter._chunk_content(large_content, 3000)
    print(f"   Result: {len(chunks_medium)} chunks")
    for i, chunk in enumerate(chunks_medium):
        tokens = butter._estimate_tokens(chunk)
        print(f"   Chunk {i+1}: {len(chunk)} chars, ~{tokens} tokens")
    
    # Test 3: Large max_tokens (should not chunk)
    print("\n🧪 TEST 3: Large max_tokens (10000) - should not chunk")
    chunks_large = butter._chunk_content(large_content, 10000)
    print(f"   Result: {len(chunks_large)} chunks")
    for i, chunk in enumerate(chunks_large):
        tokens = butter._estimate_tokens(chunk)
        print(f"   Chunk {i+1}: {len(chunk)} chars, ~{tokens} tokens")
    
    # Test 4: Content with tables
    print("\n🧪 TEST 4: Content with tables")
    table_content = f"""
{page3_content}

| Component | Purpose | Code Equivalent |
|-----------|---------|-----------------|
| Bread | Foundation | Architecture, directory structure |
| Peanut Butter | Logic Layer | Core functions, data transformations |
| Jelly | Interface | UI, API responses, logs |
| Dependencies | Ingredients | Libraries, packages |
| Testing | Bite Test | Unit tests, integration tests |
| Documentation | Label | README, comments, guides |

{page3_content}
"""
    chunks_with_tables = butter._chunk_content(table_content, 2000)
    print(f"   Result: {len(chunks_with_tables)} chunks")
    for i, chunk in enumerate(chunks_with_tables):
        tokens = butter._estimate_tokens(chunk)
        has_table = '|' in chunk or '<table' in chunk
        print(f"   Chunk {i+1}: {len(chunk)} chars, ~{tokens} tokens, has_table: {has_table}")

if __name__ == "__main__":
    test_chunking() 