# maya_scene_info_extractor.py

import json
import os
import sys
import maya.standalone
import maya.cmds as cmds

def setup_maya_environment():
    """Initialize Maya in batch mode"""
    maya.standalone.initialize(name='python')
    # Suppress UI-related warnings but keep reference info
    cmds.scriptEditorInfo(suppressWarnings=True)
    cmds.scriptEditorInfo(suppressInfo=True)
    cmds.scriptEditorInfo(suppressErrors=True)

def get_scene_info(filepath):
    """Extract reference information from a Maya file"""
    info = {
        'filepath': filepath.replace('\\', '/'),
        'shot_name': os.path.splitext(os.path.basename(filepath))[0],
        'references': []
    }
    
    try:
        # Get all references
        refs = cmds.ls(references=True)
        if refs:
            for ref in refs:
                try:
                    ref_node = cmds.referenceQuery(ref, referenceNode=True)
                    ref_file = cmds.referenceQuery(ref_node, filename=True)
                    info['references'].append({
                        'name': ref,
                        'file': ref_file.replace('\\', '/')
                    })
                except Exception:
                    continue  # Skip problematic references
    except Exception as e:
        info['error'] = f"Error getting references: {str(e)}"
    
    return info

def process(maya_scenes):
    """Main processing function"""
    results = []
    
    try:
        setup_maya_environment()
        
        for filepath in maya_scenes:
            scene_info = {
                'filepath': filepath.replace('\\', '/'),
                'shot_name': os.path.splitext(os.path.basename(filepath))[0],
                'references': []
            }
            
            try:
                # Open scene without forcing (to avoid some warnings)
                cmds.file(filepath, open=True, force=False, loadReferenceDepth='none')
                
                # Get scene information
                scene_info = get_scene_info(filepath)
                
            except Exception as e:
                scene_info['error'] = f"Failed to open scene: {str(e)}"
            finally:
                cmds.file(new=True, force=True)  # Clear the scene
            
            results.append(scene_info)
    
    except Exception as e:
        return json.dumps({
            'error': f"Initialization error: {str(e)}"
        }, indent=4)
    
    finally:
        if 'maya.standalone' in globals():
            maya.standalone.uninitialize()
    
    # Return clean JSON data
    return json.dumps(results, indent=4)

if __name__ == "__main__":
    # When run directly with mayapy, read scenes from command line arguments
    if len(sys.argv) > 1:
        scenes = sys.argv[1:]  # First arg is script path, rest are scene files
        print(process(scenes))