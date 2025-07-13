# maya_scene_info_extractor.py

import json
import os
import pathlib

try:
    import maya.standalone
    import maya.cmds as cmds
    MAYA_MODE = True
except ImportError:
    MAYA_MODE = False

def get_scene_info(filepath):
    """Extract scene information from a Maya file"""
    info = {
        'filepath': filepath,
        'shot_name': os.path.splitext(os.path.basename(filepath))[0],
        'start_frame': cmds.playbackOptions(query=True, min=True),
        'end_frame': cmds.playbackOptions(query=True, max=True),
        'enabled_layers': [],
        'disabled_layers': [],
        'references': []
    }
    
    # Get render layer information
    all_layers = cmds.ls(type='renderLayer')
    for layer in all_layers:
        if layer not in ['defaultRenderLayer']:
            if cmds.getAttr(f"{layer}.renderable"):
                info['enabled_layers'].append(layer)
            else:
                info['disabled_layers'].append(layer)
    
    # Get reference information
    refs = cmds.ls(references=True)
    if refs:
        for ref in refs:
            ref_node = cmds.referenceQuery(ref, referenceNode=True)
            info['references'].append({
                'name': ref,
                'file': cmds.referenceQuery(ref_node, filename=True)
            })
    
    return info

def process(maya_scenes):
    """Main function to be called from maya_open.py"""
    if not MAYA_MODE:
        return "Error: Maya modules not available - cannot process scenes"
    
    try:
        # Initialize Maya
        maya.standalone.initialize(name='python')
        
        results = []
        for filepath in maya_scenes:
            try:
                # Open scene without loading references for faster processing
                cmds.file(filepath, open=True, force=True, loadReferenceDepth='none')
                
                # Get scene information
                scene_info = get_scene_info(filepath)
                results.append(scene_info)
                
            except Exception as e:
                results.append({
                    'filepath': filepath,
                    'error': str(e)
                })
    
    # Save results to JSON file
        output_file = os.path.join(os.path.dirname(__file__), "scene_info_report.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return f"Successfully processed {len(results)} scenes. Report saved to {output_file}"
    
    except Exception as e:
        return f"Error during processing: {str(e)}"
    
    finally:
        if 'maya.standalone' in globals():
            maya.standalone.uninitialize()

