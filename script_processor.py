# script_processor.py
import os
import importlib.util

class ScriptProcessor:
    def __init__(self, scripts_folder):
        self.scripts_folder = scripts_folder
        self.scripts = self._discover_scripts()
        
    def _discover_scripts(self):
        """Find all .py files in scripts folder"""
        scripts = {}
        if not os.path.exists(self.scripts_folder):
            return scripts
            
        for file in os.listdir(self.scripts_folder):
            if file.endswith('.py') and not file.startswith('_'):
                script_name = os.path.splitext(file)[0]
                scripts[script_name] = os.path.join(self.scripts_folder, file)
        return scripts
        
    def get_script_names(self):
        """Return list of available script names"""
        return list(self.scripts.keys())
        
    def execute_script(self, script_name, maya_scenes):
        """Execute the selected script"""
        if script_name not in self.scripts:
            return f"Error: Script {script_name} not found"
            
        try:
            spec = importlib.util.spec_from_file_location(script_name, self.scripts[script_name])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.process(maya_scenes)  # All scripts must have process() function
        except Exception as e:
            return f"Error executing {script_name}: {str(e)}"