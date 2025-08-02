#!/usr/bin/env python3
"""
nvdiffrast RTX 4090 Demo
Demonstrates high-performance differentiable rendering
"""

import os
import torch
import numpy as np
import nvdiffrast.torch as dr
from PIL import Image

def setup_environment():
    """Setup CUDA environment for RTX 4090"""
    # Add CUDA DLL directories (from our fix)
    cuda_paths = [
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\bin"
    ]
    
    for cuda_path in cuda_paths:
        if os.path.exists(cuda_path):
            os.add_dll_directory(cuda_path)
    
    # Set environment variables
    os.environ['TORCH_CUDA_ARCH_LIST'] = '8.9'  # RTX 4090
    print("🚀 Environment configured for RTX 4090")

def create_triangle_mesh():
    """Create a simple colored triangle"""
    # Triangle vertices in clip space [-1, 1]
    vertices = torch.tensor([
        [-0.5, -0.5, 0.0, 1.0],  # Bottom left
        [ 0.5, -0.5, 0.0, 1.0],  # Bottom right  
        [ 0.0,  0.5, 0.0, 1.0]   # Top center
    ], dtype=torch.float32, device='cuda')
    
    # Triangle indices
    triangles = torch.tensor([
        [0, 1, 2]
    ], dtype=torch.int32, device='cuda')
    
    # Vertex colors (RGB)
    colors = torch.tensor([
        [1.0, 0.0, 0.0],  # Red
        [0.0, 1.0, 0.0],  # Green
        [0.0, 0.0, 1.0]   # Blue
    ], dtype=torch.float32, device='cuda')
    
    return vertices.unsqueeze(0), triangles, colors.unsqueeze(0)

def create_cube_mesh():
    """Create a colorful 3D cube"""
    # Cube vertices
    vertices = torch.tensor([
        # Front face
        [-0.5, -0.5,  0.5, 1.0],
        [ 0.5, -0.5,  0.5, 1.0],
        [ 0.5,  0.5,  0.5, 1.0],
        [-0.5,  0.5,  0.5, 1.0],
        # Back face
        [-0.5, -0.5, -0.5, 1.0],
        [ 0.5, -0.5, -0.5, 1.0],
        [ 0.5,  0.5, -0.5, 1.0],
        [-0.5,  0.5, -0.5, 1.0],
    ], dtype=torch.float32, device='cuda')
    
    # Cube triangles (12 triangles for 6 faces)
    triangles = torch.tensor([
        # Front face
        [0, 1, 2], [2, 3, 0],
        # Back face
        [4, 6, 5], [6, 4, 7],
        # Left face
        [4, 0, 3], [3, 7, 4],
        # Right face
        [1, 5, 6], [6, 2, 1],
        # Top face
        [3, 2, 6], [6, 7, 3],
        # Bottom face
        [4, 5, 1], [1, 0, 4],
    ], dtype=torch.int32, device='cuda')
    
    # Vertex colors
    colors = torch.tensor([
        [1.0, 0.0, 0.0],  # Red
        [0.0, 1.0, 0.0],  # Green
        [0.0, 0.0, 1.0],  # Blue
        [1.0, 1.0, 0.0],  # Yellow
        [1.0, 0.0, 1.0],  # Magenta
        [0.0, 1.0, 1.0],  # Cyan
        [1.0, 0.5, 0.0],  # Orange
        [0.5, 0.0, 1.0],  # Purple
    ], dtype=torch.float32, device='cuda')
    
    return vertices.unsqueeze(0), triangles, colors.unsqueeze(0)

def create_rotation_matrix(angle_x, angle_y, angle_z):
    """Create 3D rotation matrix"""
    cos_x, sin_x = torch.cos(angle_x), torch.sin(angle_x)
    cos_y, sin_y = torch.cos(angle_y), torch.sin(angle_y)
    cos_z, sin_z = torch.cos(angle_z), torch.sin(angle_z)
    
    # Rotation matrices
    R_x = torch.tensor([
        [1, 0, 0, 0],
        [0, cos_x, -sin_x, 0],
        [0, sin_x, cos_x, 0],
        [0, 0, 0, 1]
    ], dtype=torch.float32, device='cuda')
    
    R_y = torch.tensor([
        [cos_y, 0, sin_y, 0],
        [0, 1, 0, 0],
        [-sin_y, 0, cos_y, 0],
        [0, 0, 0, 1]
    ], dtype=torch.float32, device='cuda')
    
    R_z = torch.tensor([
        [cos_z, -sin_z, 0, 0],
        [sin_z, cos_z, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=torch.float32, device='cuda')
    
    return R_z @ R_y @ R_x

def render_scene(ctx, vertices, triangles, colors, resolution=512):
    """Render a 3D scene with nvdiffrast"""
    batch_size = vertices.shape[0]
    
    # Rasterize geometry
    rast_out, rast_out_db = dr.rasterize(ctx, vertices, triangles, resolution=[resolution, resolution])
    
    # Interpolate vertex colors
    color_interpolated, _ = dr.interpolate(colors, rast_out, triangles)
    
    # Alpha blending (set alpha to 1.0 for opaque)
    alpha = torch.ones_like(color_interpolated[..., :1])
    output = torch.cat([color_interpolated, alpha], dim=-1)
    
    return output

def save_image(tensor, filename):
    """Save tensor as image"""
    # Convert from [batch, height, width, channels] to numpy
    img_np = tensor[0].detach().cpu().numpy()
    
    # Convert to 8-bit
    img_np = (img_np * 255).astype(np.uint8)
    
    # Create PIL image and save
    img = Image.fromarray(img_np)
    img.save(filename)
    print(f"💾 Saved image: {filename}")

def demo_triangle():
    """Demo 1: Simple triangle rendering"""
    print("🔺 Demo 1: Rendering colored triangle...")
    
    # Create CUDA context
    ctx = dr.RasterizeCudaContext()
    
    # Create triangle mesh
    vertices, triangles, colors = create_triangle_mesh()
    
    # Render
    output = render_scene(ctx, vertices, triangles, colors, resolution=512)
    
    # Save result
    save_image(output, "triangle_demo.png")
    
    print(f"   Triangle rendered at 512x512 resolution")
    print(f"   Output shape: {output.shape}")

def demo_rotating_cube():
    """Demo 2: Rotating cube animation frames"""
    print("🎲 Demo 2: Rendering rotating cube...")
    
    # Create CUDA context
    ctx = dr.RasterizeCudaContext()
    
    # Create cube mesh
    base_vertices, triangles, colors = create_cube_mesh()
    
    # Render multiple rotation angles
    angles = [0, 30, 60, 90, 120, 150]
    
    for i, angle in enumerate(angles):
        # Create rotation matrix
        angle_rad = torch.tensor(np.radians(angle), device='cuda')
        rotation = create_rotation_matrix(angle_rad * 0.5, angle_rad, angle_rad * 0.3)
        
        # Apply rotation to vertices
        vertices_4d = base_vertices[0]  # Remove batch dimension
        rotated_vertices = (rotation @ vertices_4d.T).T
        vertices = rotated_vertices.unsqueeze(0).contiguous()  # Add batch dimension back and ensure contiguous
        
        # Render
        output = render_scene(ctx, vertices, triangles, colors, resolution=512)
        
        # Save frame
        filename = f"cube_rotation_{i:02d}_{angle:03d}deg.png"
        save_image(output, filename)
    
    print(f"   Rendered {len(angles)} rotation frames")

def demo_performance_test():
    """Demo 3: Performance test with RTX 4090"""
    print("⚡ Demo 3: RTX 4090 performance test...")
    
    # Create CUDA context
    ctx = dr.RasterizeCudaContext()
    
    # Create cube mesh
    vertices, triangles, colors = create_cube_mesh()
    
    # Performance test parameters
    resolutions = [256, 512, 1024, 2048]
    num_iterations = 10
    
    print("   Resolution | Avg Time (ms) | FPS")
    print("   -----------|---------------|----")
    
    for resolution in resolutions:
        # Warm up
        for _ in range(3):
            output = render_scene(ctx, vertices, triangles, colors, resolution)
            torch.cuda.synchronize()
        
        # Timing test
        start_time = torch.cuda.Event(enable_timing=True)
        end_time = torch.cuda.Event(enable_timing=True)
        
        start_time.record()
        for _ in range(num_iterations):
            output = render_scene(ctx, vertices, triangles, colors, resolution)
        end_time.record()
        
        torch.cuda.synchronize()
        elapsed_ms = start_time.elapsed_time(end_time) / num_iterations
        fps = 1000.0 / elapsed_ms
        
        print(f"   {resolution:4d}x{resolution:<4d} | {elapsed_ms:8.2f}    | {fps:4.1f}")

def main():
    """Main demo function"""
    print("🎨 nvdiffrast RTX 4090 Demo")
    print("============================")
    
    # Setup environment
    setup_environment()
    
    # Check CUDA availability
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return
    
    print(f"✅ Using device: {torch.cuda.get_device_name(0)}")
    print(f"✅ CUDA memory: {torch.cuda.get_device_properties(0).total_memory // 1024**3} GB")
    print()
    
    try:
        # Run demos
        demo_triangle()
        print()
        
        demo_rotating_cube()
        print()
        
        demo_performance_test()
        print()
        
        print("🎉 All demos completed successfully!")
        print("📁 Check the generated .png files to see the results")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()