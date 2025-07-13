# maya_headless_example.py

import maya.standalone  # Maya Python standalone API
import maya.cmds as cmds  # Maya commands

def initialize_headless():
    """Initialize Maya in headless mode"""
    maya.standalone.initialize(name='python')
    print("Maya initialized in headless mode")

def open_scene(file_path):
    """Open a specified Maya scene"""
    cmds.file(file_path, open=True, force=True)
    print(f"Opened scene: {file_path}")

    try:
        cmds.loadPlugin("redshift4maya")
    except Exception as e:
        print(f"Failed to load plugin 'redshift4maya': {e}")

def adjust_layer(layers_to_enable=None, layers_to_disable=None):
    """
    Adjust multiple render layers' visibility
    Args:
        layers_to_enable (list): List of layer names to set as renderable
        layers_to_disable (list): List of layer names to set as not renderable
    """
    if layers_to_enable is None:
        layers_to_enable = []
    if layers_to_disable is None:
        layers_to_disable = []
    
    # First switch to default layer to avoid potential conflicts
    cmds.editRenderLayerGlobals(currentRenderLayer="defaultRenderLayer")
    
    # Disable specified layers
    for layer in layers_to_disable:
        if cmds.objExists(layer) and cmds.objectType(layer) == 'renderLayer':
            cmds.setAttr(f"{layer}.renderable", 0)
            print(f"Disabled render layer: {layer}")
        else:
            print(f"Warning: Layer '{layer}' doesn't exist or is not a render layer")
    
    # Enable specified layers
    for layer in layers_to_enable:
        if cmds.objExists(layer) and cmds.objectType(layer) == 'renderLayer':
            cmds.setAttr(f"{layer}.renderable", 1)
            print(f"Enabled render layer: {layer}")
        else:
            print(f"Warning: Layer '{layer}' doesn't exist or is not a render layer")
    
    # For any enabled layers, set the last one as current
    if layers_to_enable:
        cmds.editRenderLayerGlobals(currentRenderLayer=layers_to_enable[-1])


def save_scene():
    """Save the current scene"""
    cmds.file(save=True, type='mayaAscii')
    print("Scene saved successfully.")

def shutdown_maya():
    """Cleanly shut down Maya"""
    maya.standalone.uninitialize()
    print("Maya shutdown complete")

def process_files(file_paths, layers_to_enable, layers_to_disable):
    """Process each file in the list"""
    for file_path in file_paths:
        try:
            open_scene(file_path)
            adjust_layer(layers_to_enable, layers_to_disable)
            save_scene()
            print(f"Processed file: {file_path}")
        except Exception as e:
            print(f"Error processing file '{file_path}': {str(e)}")

if __name__ == "__main__":
    try:
        initialize_headless()
        
        # List of file paths to process
        file_paths = [
            r"V:\PAPA\Work\Render\PAPA_Movie\REEL_04\5. INT. KACHAXS CABIN - MOMENTS LATER\PAPA_Chapter_03_05_Sh082d\old\PAPA_Chapter_03_05_sh082d_RENDER.ma",
            r"V:\PAPA\Work\Render\PAPA_Movie\REEL_04\5. INT. KACHAXS CABIN - MOMENTS LATER\PAPA_Chapter_03_05_Sh083\old\PAPA_Chapter_03_05_sh083_RENDER.ma",
            r"V:\PAPA\Work\Render\PAPA_Movie\REEL_04\5. INT. KACHAXS CABIN - MOMENTS LATER\PAPA_Chapter_03_05_Sh086\old\PAPA_Chapter_03_05_Sh086_RENDER.ma"
        ]

        adjust_layer(
            layers_to_enable=["CHAR"],      # Enable the CHAR layer
            layers_to_disable=["FOG", "RIM"] # Disable FOG and RIM layers
        )
        save_scene()
        shutdown_maya()
        print("Script completed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'maya.standalone' in globals():
            shutdown_maya()
