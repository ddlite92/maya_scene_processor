try:
    import maya.standalone
    import maya.cmds as cmds
    MAYA_MODE = True
except ImportError:
    MAYA_MODE = False
    print("Maya modules not found - running in test mode")

class MayaSceneProcessor:
    def __init__(self, scene_files=None):
        self.scene_files = scene_files or []
        self.initialized = False
        
    def initialize_maya(self):
        if not MAYA_MODE:
            return False
            
        try:
            maya.standalone.initialize(name='python')
            self.initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize Maya: {str(e)}")
            return False
            
    def shutdown_maya(self):
        if MAYA_MODE and self.initialized:
            maya.standalone.uninitialize()
            self.initialized = False
            
    def open_scene(self, file_path):
        if not MAYA_MODE:
            return f"[TEST] Would open: {file_path}"
            
        cmds.file(file_path, open=True, force=True)
        return f"Opened scene: {file_path}"
    
    def save_scene(self):
        """Save current scene"""
        cmds.file(save=True, type='mayaAscii')
        return "Scene saved"
        
    def list_references(self):
        """List all references in current scene"""
        return cmds.ls(type='reference')
        
    def process_scene(self, file_path):
        """Process a single scene file"""
        try:
            result = []
            result.append(self.open_scene(file_path))
            
            references = self.list_references()
            result.append(f"Found {len(references)} references:")
            for ref in references:
                result.append(f" - {ref}")
                
            self.save_scene()
            result.append("Scene processed successfully")
            return "\n".join(result)
            
        except Exception as e:
            return f"Error processing scene: {str(e)}"
            
    def process_all(self):
        """Process all scene files"""
        if not self.initialize_maya():
            return ["Failed to initialize Maya"]
            
        results = []
        for scene_file in self.scene_files:
            results.append(self.process_scene(scene_file))
            
        self.shutdown_maya()
        return results