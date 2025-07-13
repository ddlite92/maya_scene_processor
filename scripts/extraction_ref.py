# maya_scene_info_extractor.py

import maya.standalone
import maya.cmds as cmds
import json
import os
import pathlib


def initialize_maya():
    """Initialize Maya in headless mode"""
    maya.standalone.initialize(name='python')
    print("Maya initialized in headless mode")

def get_scene_info(filepath):
    """Extract scene information from a Maya file"""
    info = {
        'filepath': filepath,
        'shot_name': os.path.splitext(os.path.basename(filepath))[0],
        'references': []
    }

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

def process_scenes(filepaths, output_file):
    """Process list of Maya files and save extracted information"""
    results = []
    
    for filepath in filepaths:
        try:
            print(f"\nProcessing: {filepath}")
            
            # Open scene without loading references for faster processing
            cmds.file(filepath, open=True, force=True, loadReferenceDepth='none')
            
            # Get scene information
            scene_info = get_scene_info(filepath)
            results.append(scene_info)
            
            print(f"Extracted information for: {scene_info['shot_name']}")
            
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
            results.append({
                'filepath': filepath,
                'error': str(e)
            })
    
    # Save results to JSON file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\nSaved results to: {output_file}")

if __name__ == "__main__":
    # List of Maya files to process
    scene_files = [
        r"V:\PAPA\Work\Render\PAPA_Movie\REEL_04\5. INT. KACHAXS CABIN - MOMENTS LATER\PAPA_Chapter_03_05_Sh082d\char.ma",
        r"V:\PAPA\Work\Render\PAPA_Movie\REEL_04\5. INT. KACHAXS CABIN - MOMENTS LATER\PAPA_Chapter_03_05_Sh083\char.ma",
        r"V:\PAPA\Work\Render\PAPA_Movie\REEL_04\5. INT. KACHAXS CABIN - MOMENTS LATER\PAPA_Chapter_03_05_Sh086\char.ma"
    ]
    
    # Output JSON file
    json_filepath = pathlib.Path(__file__).parent.resolve()
    json_file = r"scene_ref_report.json"
    output_json = os.path.join(json_filepath, json_file) 
    
    try:
        # Initialize Maya
        initialize_maya()
        
        # Process scenes
        process_scenes(scene_files, output_json)
        
        # Shutdown Maya
        maya.standalone.uninitialize()
        print("\nProcessing completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'maya.standalone' in globals():
            maya.standalone.uninitialize()
