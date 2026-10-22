import bpy
import math
import mathutils
import os
import subprocess
from pathlib import Path

def setup_studio_and_render_turntable(output_video_path, num_frames=180, fps=60, resolution=(1920, 1080)):
    scene = bpy.context.scene
    
    # Engine selection in Blender 5.2
    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except Exception:
        try:
            scene.render.engine = 'BLENDER_EEVEE'
        except Exception:
            scene.render.engine = 'CYCLES'
    
    # Render settings
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = num_frames
    
    # Color management
    try:
        scene.view_settings.view_transform = 'AgX'
    except Exception:
        pass

    # Find character mesh and center
    char_obj = bpy.data.objects.get("Dex_Mesh") or bpy.data.objects.get("Dex_Armature")
    if not char_obj:
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                char_obj = obj
                break

    # Calculate bounding box / height
    bbox = [char_obj.matrix_world @ mathutils.Vector(corner) for corner in char_obj.bound_box] if (char_obj and hasattr(char_obj, "bound_box")) else [mathutils.Vector((0,0,0))]
    min_z = min(b.z for b in bbox) if (char_obj and hasattr(char_obj, "bound_box")) else 0
    max_z = max(b.z for b in bbox) if (char_obj and hasattr(char_obj, "bound_box")) else 1.8
    center_z = (min_z + max_z) / 2.0
    char_height = max(max_z - min_z, 1.2)

    # Clean existing lights & cameras
    for o in list(bpy.data.objects):
        if o.type in ('LIGHT', 'CAMERA') or o.name.startswith(("Studio_", "Center_", "Turntable_")):
            bpy.data.objects.remove(o, do_unlink=True)

    # 1. Studio Lighting Setup
    # Key Light (Warm soft light, top right)
    key_data = bpy.data.lights.new(name="Key_Light", type='AREA')
    key_data.energy = 850
    key_data.size = 2.5
    key_data.color = (1.0, 0.95, 0.88)
    key_obj = bpy.data.objects.new("Key_Light", key_data)
    key_obj.location = (2.2, -2.5, center_z + 2.0)
    bpy.context.collection.objects.link(key_obj)

    # Fill Light (Cool bluish soft light, left)
    fill_data = bpy.data.lights.new(name="Fill_Light", type='AREA')
    fill_data.energy = 400
    fill_data.size = 3.5
    fill_data.color = (0.75, 0.85, 1.0)
    fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
    fill_obj.location = (-2.8, -2.0, center_z + 1.2)
    bpy.context.collection.objects.link(fill_obj)

    # Rim / Back Light (Highlight character edges & silhouette)
    rim_data = bpy.data.lights.new(name="Rim_Light", type='AREA')
    rim_data.energy = 1100
    rim_data.size = 2.0
    rim_data.color = (0.95, 0.75, 0.48)
    rim_obj = bpy.data.objects.new("Rim_Light", rim_data)
    rim_obj.location = (0.5, 2.8, center_z + 1.8)
    bpy.context.collection.objects.link(rim_obj)

    # Bottom Glow / Ground Light
    bottom_data = bpy.data.lights.new(name="Bottom_Light", type='POINT')
    bottom_data.energy = 120
    bottom_data.color = (0.35, 0.55, 0.95)
    bottom_obj = bpy.data.objects.new("Bottom_Light", bottom_data)
    bottom_obj.location = (0, 0, min_z + 0.1)
    bpy.context.collection.objects.link(bottom_obj)

    # Track lights to center target
    target_empty = bpy.data.objects.new("Center_Target", None)
    target_empty.location = (0, 0, center_z)
    bpy.context.collection.objects.link(target_empty)

    for l_obj in (key_obj, fill_obj, rim_obj):
        c = l_obj.constraints.new(type='TRACK_TO')
        c.target = target_empty
        c.track_axis = 'TRACK_NEGATIVE_Z'
        c.up_axis = 'UP_Y'

    # 2. Studio Pedestal Platform
    bpy.ops.mesh.primitive_cylinder_add(radius=1.8, depth=0.08, location=(0, 0, min_z - 0.04))
    pedestal = bpy.context.active_object
    pedestal.name = "Studio_Pedestal"
    mat_pedestal = bpy.data.materials.new(name="MAT_Pedestal")
    nodes = mat_pedestal.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.04, 0.06, 0.12, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.25
        if 'Metallic' in bsdf.inputs:
            bsdf.inputs['Metallic'].default_value = 0.4
    pedestal.data.materials.append(mat_pedestal)

    # 3. Camera Setup & 360 Animation
    cam_data = bpy.data.cameras.new(name="Turntable_Camera")
    cam_data.lens = 65
    cam_data.sensor_width = 36
    cam_obj = bpy.data.objects.new("Turntable_Camera", cam_data)
    scene.camera = cam_obj
    bpy.context.collection.objects.link(cam_obj)

    # Turntable Empty Rig
    turntable_rig = bpy.data.objects.new("Turntable_Rig", None)
    turntable_rig.location = (0, 0, center_z)
    bpy.context.collection.objects.link(turntable_rig)

    cam_distance = max(char_height * 2.6, 2.8)
    cam_obj.location = (0, -cam_distance, center_z + 0.25)
    cam_obj.parent = turntable_rig

    cam_constraint = cam_obj.constraints.new(type='TRACK_TO')
    cam_constraint.target = target_empty
    cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    cam_constraint.up_axis = 'UP_Y'

    # Animate frame by frame handler for deterministic 360 rotation
    def turntable_frame_change(scene_obj):
        current_f = scene_obj.frame_current
        angle = ((current_f - 1) / num_frames) * 2.0 * math.pi
        turntable_rig.rotation_euler = (0, 0, angle)

    bpy.app.handlers.frame_change_pre.append(turntable_frame_change)

    # Output frames directory
    frames_dir = Path("D:/editaVideos/edita/assets/turntable_frames")
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    scene.render.filepath = str(frames_dir / "frame_").replace("\\", "/")
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    # World background setup (Studio dark luxury gradient)
    bg_node = scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.015, 0.025, 0.05, 1.0)
        bg_node.inputs['Strength'].default_value = 0.6

    print(f"[BLENDER] Renderizando turntable 360 em frames PNG ({num_frames} frames @ {fps}fps)...")
    bpy.ops.render.render(animation=True)
    print(f"[BLENDER] Frames renderizados em {frames_dir}!")

if __name__ == "__main__":
    output_mp4 = "D:/editaVideos/edita/assets/dex_360_render.mp4"
    setup_studio_and_render_turntable(output_mp4, num_frames=180, fps=60)
