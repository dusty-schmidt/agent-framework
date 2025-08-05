import importlib
import os

class ToolProvider:
    def __init__(self, plugins_folder="tools"):
        self.tools = {}
        self._load_plugins(plugins_folder)

    def _load_plugins(self, folder):
        for filename in os.listdir(folder):
            if filename.endswith(".py") and filename != "__init__.py":
                tool_name = filename[:-3]
                module = importlib.import_module(f"{folder}.{tool_name}")
                if hasattr(module, "run"):
                    self.tools[tool_name] = module.run

    def run(self, name: str, arg: str) -> str:
        if name in self.tools:
            return self.tools[name](arg)
        return f"[Tool '{name}' not found]"

# Instantiate and auto-load all tools in /tools/
tools = ToolProvider()
