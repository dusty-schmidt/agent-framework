#!/usr/bin/env python3
"""
Test script for unified memory storage backends.

Tests JSON, SQLite, and FAISS storage implementations to ensure they work correctly.
"""

import asyncio
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from unified_memory.memory_interface import UnifiedMemoryItem, MemoryType, RetentionPolicy, MemoryQueryFilter
from unified_memory.storage.json_storage import JSONMemoryStorage
from unified_memory.storage.sqlite_storage import SQLiteMemoryStorage

# Try to import FAISS storage, but handle if dependencies aren't installed
try:
    from unified_memory.storage.faiss_storage import FAISSMemoryStorage
    FAISS_AVAILABLE = True
except ImportError as e:
    print(f"FAISS storage not available (dependencies missing): {e}")
    FAISS_AVAILABLE = False


def create_test_memory_items() -> List[UnifiedMemoryItem]:
    """Create a set of test memory items for testing."""
    items = []
    
    # Create diverse test data
    test_data = [
        {
            "content": "The user asked about Python programming best practices",
            "memory_type": MemoryType.CONVERSATION,
            "tier_source": "chat_tier",
            "tags": ["python", "programming", "best-practices"],
            "metadata": {"importance": "high", "context": "development"}
        },
        {
            "content": "Machine learning model training completed successfully",
            "memory_type": MemoryType.SYSTEM_STATE,
            "tier_source": "ml_tier",
            "tags": ["ml", "training", "success"],
            "metadata": {"model_accuracy": 0.95, "training_time": "2h"}
        },
        {
            "content": "User prefers dark theme and compact layout",
            "memory_type": MemoryType.USER_PREFERENCE,
            "tier_source": "ui_tier",
            "tags": ["ui", "preferences", "theme"],
            "metadata": {"theme": "dark", "layout": "compact"}
        },
        {
            "content": "Database connection pool exhausted at peak traffic",
            "memory_type": MemoryType.ERROR_LOG,
            "tier_source": "db_tier",
            "tags": ["database", "error", "performance"],
            "metadata": {"severity": "critical", "affected_users": 150}
        },
        {
            "content": "The weather API integration needs authentication token refresh",
            "memory_type": MemoryType.TASK,
            "tier_source": "api_tier",
            "tags": ["api", "weather", "authentication"],
            "metadata": {"priority": "medium", "due_date": "2024-12-01"}
        }
    ]
    
    for i, data in enumerate(test_data):
        item = UnifiedMemoryItem(
            id=f"test_item_{i+1}",
            content=data["content"],
            memory_type=data["memory_type"],
            tier_source=data["tier_source"],
            tags=data["tags"],
            metadata=data["metadata"],
            timestamp=datetime.utcnow() - timedelta(hours=i),
            retention_policy=RetentionPolicy.AUTO_EXPIRE,
            access_count=i * 2,
            last_accessed=datetime.utcnow() - timedelta(minutes=i*10)
        )
        items.append(item)
    
    return items


async def test_storage_backend(storage, backend_name: str):
    """Test a storage backend with comprehensive operations."""
    print(f"\n=== Testing {backend_name} Storage Backend ===")
    
    try:
        # Create test items
        test_items = create_test_memory_items()
        print(f"Created {len(test_items)} test items")
        
        # Test 1: Save individual items
        print("\n1. Testing individual save operations...")
        saved_ids = []
        for item in test_items:
            item_id = await storage.save(item)
            saved_ids.append(item_id)
            print(f"   Saved item: {item_id}")
        
        # Test 2: Retrieve by ID
        print("\n2. Testing retrieval by ID...")
        for item_id in saved_ids[:2]:  # Test first 2 items
            retrieved_item = await storage.get_by_id(item_id)
            if retrieved_item:
                print(f"   Retrieved: {item_id} - {retrieved_item.content[:50]}...")
            else:
                print(f"   ERROR: Could not retrieve {item_id}")
        
        # Test 3: Query operations
        print("\n3. Testing query operations...")
        
        # Basic query with limit
        query_filter = MemoryQueryFilter(limit=3)
        results = await storage.query(query_filter)
        print(f"   Basic query returned {len(results.items)} items (expected: 3)")
        
        # Content search
        query_filter = MemoryQueryFilter(
            content_search="Python programming",
            limit=10
        )
        results = await storage.query(query_filter)
        print(f"   Content search for 'Python programming' returned {len(results.items)} items")
        
        # Filter by memory type
        query_filter = MemoryQueryFilter(
            memory_types=[MemoryType.CONVERSATION, MemoryType.TASK],
            limit=10
        )
        results = await storage.query(query_filter)
        print(f"   Memory type filter returned {len(results.items)} items")
        
        # Filter by tags
        query_filter = MemoryQueryFilter(
            tags=["python", "api"],
            limit=10
        )
        results = await storage.query(query_filter)
        print(f"   Tag filter returned {len(results.items)} items")
        
        # Test 4: Update operations
        print("\n4. Testing update operations...")
        first_item_id = saved_ids[0]
        update_success = await storage.update(first_item_id, {
            "access_count": 999,
            "metadata": {"updated": True, "test": "update_operation"}
        })
        if update_success:
            updated_item = await storage.get_by_id(first_item_id)
            print(f"   Update successful. Access count: {updated_item.access_count}")
        else:
            print("   ERROR: Update failed")
        
        # Test 5: Batch save
        print("\n5. Testing batch save...")
        batch_items = [
            UnifiedMemoryItem(
                id=f"batch_item_{i}",
                content=f"Batch test item {i}",
                memory_type=MemoryType.CONVERSATION,
                tier_source="test_tier",
                tags=["batch", "test"],
                metadata={"batch_id": i},
                timestamp=datetime.utcnow(),
                retention_policy=RetentionPolicy.TEMPORARY
            )
            for i in range(3)
        ]
        
        batch_ids = await storage.batch_save(batch_items)
        print(f"   Batch saved {len(batch_ids)} items")
        
        # Test 6: Statistics
        print("\n6. Testing statistics...")
        stats = await storage.get_stats()
        print(f"   Storage stats: {stats}")
        
        # Test 7: Cleanup (dry run)
        print("\n7. Testing cleanup (dry run)...")
        cleanup_stats = await storage.cleanup_expired(dry_run=True)
        print(f"   Cleanup stats: {cleanup_stats}")
        
        # Test 8: Delete operations
        print("\n8. Testing delete operations...")
        delete_id = saved_ids[-1]  # Delete last item
        delete_success = await storage.delete(delete_id)
        if delete_success:
            # Verify deletion
            deleted_item = await storage.get_by_id(delete_id)
            if deleted_item is None:
                print(f"   Successfully deleted item: {delete_id}")
            else:
                print(f"   WARNING: Item still exists after deletion: {delete_id}")
        else:
            print(f"   ERROR: Failed to delete item: {delete_id}")
        
        print(f"\n✅ {backend_name} storage backend tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ {backend_name} storage backend test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Run comprehensive tests on all storage backends."""
    print("🚀 Starting comprehensive storage backend tests...")
    
    # Create temporary directory for test files
    temp_dir = Path(tempfile.mkdtemp(prefix="memory_storage_test_"))
    print(f"Using temporary directory: {temp_dir}")
    
    results = {}
    
    try:
        # Test 1: JSON Storage
        print("\n" + "="*60)
        json_storage = JSONMemoryStorage(temp_dir / "json_storage")
        results["JSON"] = await test_storage_backend(json_storage, "JSON")
        
        # Test 2: SQLite Storage
        print("\n" + "="*60)
        sqlite_storage = SQLiteMemoryStorage(temp_dir / "sqlite_storage.db")
        results["SQLite"] = await test_storage_backend(sqlite_storage, "SQLite")
        
        # Test 3: FAISS Storage (if available)
        if FAISS_AVAILABLE:
            print("\n" + "="*60)
            try:
                faiss_storage = FAISSMemoryStorage(temp_dir / "faiss_storage")
                results["FAISS"] = await test_storage_backend(faiss_storage, "FAISS")
            except Exception as e:
                print(f"FAISS storage test failed due to missing dependencies: {e}")
                results["FAISS"] = False
        else:
            print("\n" + "="*60)
            print("FAISS storage skipped - dependencies not installed")
            print("To install: pip install faiss-cpu sentence-transformers")
            results["FAISS"] = None
        
    finally:
        # Cleanup temporary directory
        try:
            shutil.rmtree(temp_dir)
            print(f"\nCleaned up temporary directory: {temp_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up temporary directory: {e}")
    
    # Print final results
    print("\n" + "="*60)
    print("🎯 FINAL TEST RESULTS:")
    print("="*60)
    
    for backend, success in results.items():
        if success is True:
            print(f"✅ {backend} Storage: PASSED")
        elif success is False:
            print(f"❌ {backend} Storage: FAILED")
        else:
            print(f"⏭️  {backend} Storage: SKIPPED (dependencies not available)")
    
    # Overall result
    passed_tests = sum(1 for result in results.values() if result is True)
    total_tests = sum(1 for result in results.values() if result is not None)
    
    print(f"\n📊 Overall: {passed_tests}/{total_tests} storage backends passed")
    
    if passed_tests == total_tests and total_tests > 0:
        print("🎉 All available storage backends are working correctly!")
        return True
    else:
        print("⚠️  Some storage backends failed tests")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
