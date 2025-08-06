#!/usr/bin/env python3
"""
Project Setup Script

Automates the initial setup of the Agentic Framework project.
This script will grow to include more setup automation over time.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_conda():
    """Check if conda is available."""
    try:
        result = subprocess.run(['conda', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Conda found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Conda not found")
            return False
    except FileNotFoundError:
        print("❌ Conda not found")
        return False

def create_conda_env():
    """Create conda environment from environment.yml."""
    env_file = Path(__file__).parent.parent / "environment.yml"
    
    if not env_file.exists():
        print("❌ environment.yml not found")
        return False
    
    print("🐍 Creating conda environment...")
    try:
        result = subprocess.run([
            'conda', 'env', 'create', '-f', str(env_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Conda environment created successfully")
            return True
        else:
            print(f"❌ Failed to create conda environment: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error creating conda environment: {e}")
        return False

def check_api_key():
    """Check if API key is set in environment."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        print("✅ OPENROUTER_API_KEY found in environment")
        return True
    else:
        print("⚠️  OPENROUTER_API_KEY not found")
        print("   Add to your ~/.zshrc: export OPENROUTER_API_KEY='your_key'")
        print("   Then run: source ~/.zshrc")
        return False

def run_tests():
    """Run the complete test suite."""
    print("🧪 Running test suite...")
    test_file = Path(__file__).parent.parent / "tests" / "complete_test.py"
    
    try:
        result = subprocess.run([
            sys.executable, str(test_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main setup process."""
    print("🚀 Agentic Framework - Project Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_conda():
        print("\n❌ Setup failed: Conda is required")
        print("   Install conda/miniconda and try again")
        sys.exit(1)
    
    # Create environment
    print("\n📦 Setting up conda environment...")
    if not create_conda_env():
        print("\n❌ Setup failed: Could not create conda environment")
        sys.exit(1)
    
    # Check API key
    print("\n🔑 Checking API key...")
    api_key_ok = check_api_key()
    
    # Run tests
    print("\n🧪 Testing setup...")
    if api_key_ok:
        tests_ok = run_tests()
    else:
        print("⏭️  Skipping tests (API key not set)")
        tests_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("SETUP SUMMARY")
    print("=" * 50)
    print("✅ Conda environment: Created")
    print(f"{'✅' if api_key_ok else '⚠️ '} API key: {'Set' if api_key_ok else 'Not set'}")
    print(f"{'✅' if tests_ok else '⚠️ '} Tests: {'Passed' if tests_ok else 'Skipped/Failed'}")
    
    if api_key_ok and tests_ok:
        print("\n🎉 Setup complete! You can now:")
        print("   conda activate agentic-framework")
        print("   python scripts/simple_chat.py")
    else:
        print("\n⚠️  Setup incomplete. Please:")
        if not api_key_ok:
            print("   1. Add API key to ~/.zshrc")
            print("   2. Run: source ~/.zshrc")
        print("   3. Run tests: python tests/complete_test.py")

if __name__ == "__main__":
    main()
