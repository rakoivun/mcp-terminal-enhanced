# nvdiffrast Demo Output

This directory contains all generated output from the nvdiffrast demonstrations.

## Directory Structure

### 📁 `advanced_demo/`
**Advanced Complex Rendering Demo Output**
- `advanced_scene_static.png` - High-resolution static scene (1024x1024)
- `advanced_anim_000.png` to `advanced_anim_059.png` - 60 animation frames (512x512)  
- `advanced_animation.mp4` - Compiled animation video (30fps)

**Features demonstrated:**
- Multi-object scene graph system
- PBR materials (metallic/roughness workflow)
- Dynamic lighting with multiple light sources
- Smooth animation with keyframe interpolation
- Professional camera system
- CUDA acceleration on RTX 4090
- Post-processing with HDR tone mapping

### 📁 `basic_demo/`
**Basic Rendering Demo Output**
- `triangle_demo.png` - Simple colored triangle
- `cube_rotation_*.png` - 6 frames showing cube rotation

**Features demonstrated:**
- Basic nvdiffrast rendering pipeline
- Simple geometry and transformations
- Color interpolation

### 📁 `scripts/`
**Demo Source Code**
- `nvdiffrast_advanced_complex_demo.py` - Main advanced demo script
- `create_animation_video.py` - Animation-to-video converter
- `run_complete_advanced_demo.py` - Complete demo runner

### 📁 `docs/`
**Documentation and Plans**
- Various markdown files with implementation plans
- Analysis documents and guides
- Architecture documentation

## Usage

To re-run the demos:

```bash
# Advanced demo (from project root)
python demo_output/scripts/nvdiffrast_advanced_complex_demo.py --static-only --resolution 1024

# Create video from frames  
python demo_output/scripts/create_animation_video.py --input "demo_output/advanced_demo/advanced_anim_%03d.png" --output "new_video.mp4"
```

## Performance

Generated on RTX 4090 with CUDA acceleration:
- Static scene: ~45ms render time
- Animation frames: ~15ms per frame
- Total animation: ~60 frames in <1 second
- Video compilation: <10 seconds

## File Sizes

- Static scene: ~83KB (high quality PNG)
- Animation frames: 25-36KB each (60 frames total)
- Compiled video: ~73KB (H.264 compressed)
- Total demo output: ~2.5MB
