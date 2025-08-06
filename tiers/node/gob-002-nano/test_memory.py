#!/usr/bin/env python3
"""Test script for semantic memory search functionality"""

import os
from tools.embed_memory import VectorMemory

def main():
    print("🧠 Testing Vector Memory Semantic Search")
    print("=" * 50)
    
    # Initialize vector memory
    memory = VectorMemory(
        embedding_model="all-MiniLM-L6-v2",
        persist_path="memory/vector_memory.json"
    )
    
    print(f"📊 Memory loaded with {len(memory.texts)} texts")
    print(f"🔍 Testing semantic search...")
    
    # Test queries
    test_queries = [
        "Python programming",
        "humpback whale",
        "prime numbers",
        "France capital",
        "API calls database",
        "large language model"
    ]
    
    for query in test_queries:
        print(f"\n🔎 Query: '{query}'")
        results = memory.semantic_search(query, top_k=3)
        if results:
            print(f"   Found {len(results)} relevant memories:")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result[:100]}...")
        else:
            print("   No relevant memories found")
    
    print(f"\n✅ Test completed!")

if __name__ == "__main__":
    main()
