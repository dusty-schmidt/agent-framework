try:
    import textual
    import rich
    print("✅ TUI dependencies available")
    print(f"   textual: {textual.__version__}")
    print(f"   rich: {rich.__version__}")
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
