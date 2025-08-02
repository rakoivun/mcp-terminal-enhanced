#!/usr/bin/env python3
"""
Advanced nvdiffrast Complex Demo
Comprehensive showcase of advanced differentiable rendering techniques
Features: Multi-object scenes, PBR materials, dynamic lighting, animations, post-processing
"""

import os
import sys
import math
import time
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import nvdiffrast.torch as dr

# ============================================================================
# Core Infrastructure
# ============================================================================

class SceneObject:
    """Individual object in the scene with transform and material"""
    def __init__(self, vertices, triangles, material, transform=None):
        self.vertices = vertices          # [N, 4] homogeneous coordinates
        self.triangles = triangles        # [M, 3] triangle indices
        self.material = material          # Material properties
        self.transform = transform if transform is not None else torch.eye(4, device='cuda')
        self.uv_coords = None            # [N, 2] UV coordinates
        self.normals = None              # [N, 3] vertex normals
        
    def apply_transform(self, matrix):
        """Apply transformation matrix to object"""
        self.transform = matrix @ self.transform
        
    def get_transformed_vertices(self):
        """Get vertices with current transformation applied"""
        return (self.transform @ self.vertices.T).T

class Material:
    """PBR-style material properties"""
    def __init__(self, albedo=(0.8, 0.8, 0.8), metallic=0.0, roughness=0.5, 
                 emission=(0.0, 0.0, 0.0), normal_scale=1.0):
        self.albedo = torch.tensor(albedo, dtype=torch.float32, device='cuda')
        self.metallic = metallic
        self.roughness = roughness
        self.emission = torch.tensor(emission, dtype=torch.float32, device='cuda')
        self.normal_scale = normal_scale
        self.diffuse_texture = None
        self.normal_texture = None
        self.roughness_texture = None

class Light:
    """Light source with position, color, and type"""
    def __init__(self, position, color=(1.0, 1.0, 1.0), intensity=1.0, light_type='point'):
        self.position = torch.tensor(position, dtype=torch.float32, device='cuda')
        self.color = torch.tensor(color, dtype=torch.float32, device='cuda')
        self.intensity = intensity
        self.light_type = light_type  # 'point', 'directional', 'spot'

class Camera:
    """Camera with projection and view matrices"""
    def __init__(self, fov=45.0, aspect=1.0, near=0.1, far=100.0):
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.position = torch.tensor([0.0, 0.0, 5.0], dtype=torch.float32, device='cuda')
        self.target = torch.tensor([0.0, 0.0, 0.0], dtype=torch.float32, device='cuda')
        self.up = torch.tensor([0.0, 1.0, 0.0], dtype=torch.float32, device='cuda')
        
    def get_view_matrix(self):
        """Calculate view matrix"""
        forward = F.normalize(self.target - self.position, dim=0)
        right = F.normalize(torch.cross(forward, self.up, dim=0), dim=0)
        up = torch.cross(right, forward, dim=0)
        
        # Create view matrix
        view = torch.zeros(4, 4, device='cuda')
        view[0, :3] = right
        view[1, :3] = up
        view[2, :3] = -forward
        view[3, 3] = 1.0
        view[:3, 3] = -torch.stack([
            torch.dot(right, self.position),
            torch.dot(up, self.position), 
            torch.dot(-forward, self.position)
        ])
        return view
        
    def get_projection_matrix(self):
        """Calculate projection matrix (Vulkan-style)"""
        f = 1.0 / math.tan(math.radians(self.fov) / 2.0)
        proj = torch.zeros(4, 4, device='cuda')
        proj[0, 0] = f / self.aspect
        proj[1, 1] = -f  # Flip Y for Vulkan
        proj[2, 2] = self.far / (self.near - self.far)
        proj[2, 3] = (self.far * self.near) / (self.near - self.far)
        proj[3, 2] = -1.0
        return proj

class Scene:
    """Scene graph containing objects, lights, and camera"""
    def __init__(self):
        self.objects = []
        self.lights = []
        self.camera = Camera()
        self.ambient_light = torch.tensor([0.1, 0.1, 0.1], dtype=torch.float32, device='cuda')
        
    def add_object(self, obj):
        self.objects.append(obj)
        
    def add_light(self, light):
        self.lights.append(light)

# ============================================================================
# Geometry Generation
# ============================================================================

def create_sphere(radius=1.0, segments=32):
    """Generate sphere geometry with UV coordinates and normals"""
    vertices = []
    normals = []
    uvs = []
    triangles = []
    
    # Generate vertices
    for i in range(segments + 1):
        lat = (i / segments) * math.pi - math.pi/2  # -π/2 to π/2
        for j in range(segments + 1):
            lon = (j / segments) * 2 * math.pi  # 0 to 2π
            
            x = radius * math.cos(lat) * math.cos(lon)
            y = radius * math.sin(lat)
            z = radius * math.cos(lat) * math.sin(lon)
            
            vertices.append([x, y, z, 1.0])
            normals.append([x/radius, y/radius, z/radius])  # Normalized
            uvs.append([j / segments, i / segments])
    
    # Generate triangles
    for i in range(segments):
        for j in range(segments):
            # Current quad vertices
            v1 = i * (segments + 1) + j
            v2 = v1 + 1
            v3 = (i + 1) * (segments + 1) + j
            v4 = v3 + 1
            
            # Two triangles per quad
            triangles.append([v1, v3, v2])
            triangles.append([v2, v3, v4])
    
    vertices = torch.tensor(vertices, dtype=torch.float32, device='cuda')
    triangles = torch.tensor(triangles, dtype=torch.int32, device='cuda')
    uvs = torch.tensor(uvs, dtype=torch.float32, device='cuda')
    normals = torch.tensor(normals, dtype=torch.float32, device='cuda')
    
    return vertices, triangles, uvs, normals

def create_torus(major_radius=1.0, minor_radius=0.3, major_segments=32, minor_segments=16):
    """Generate torus geometry"""
    vertices = []
    normals = []
    uvs = []
    triangles = []
    
    for i in range(major_segments):
        theta = (i / major_segments) * 2 * math.pi
        for j in range(minor_segments):
            phi = (j / minor_segments) * 2 * math.pi
            
            # Torus parametric equations
            x = (major_radius + minor_radius * math.cos(phi)) * math.cos(theta)
            y = minor_radius * math.sin(phi)
            z = (major_radius + minor_radius * math.cos(phi)) * math.sin(theta)
            
            vertices.append([x, y, z, 1.0])
            
            # Normal calculation for torus
            nx = math.cos(phi) * math.cos(theta)
            ny = math.sin(phi)
            nz = math.cos(phi) * math.sin(theta)
            normals.append([nx, ny, nz])
            
            uvs.append([i / major_segments, j / minor_segments])
    
    # Generate triangles
    for i in range(major_segments):
        for j in range(minor_segments):
            v1 = i * minor_segments + j
            v2 = ((i + 1) % major_segments) * minor_segments + j
            v3 = i * minor_segments + ((j + 1) % minor_segments)
            v4 = ((i + 1) % major_segments) * minor_segments + ((j + 1) % minor_segments)
            
            triangles.append([v1, v2, v3])
            triangles.append([v3, v2, v4])
    
    vertices = torch.tensor(vertices, dtype=torch.float32, device='cuda')
    triangles = torch.tensor(triangles, dtype=torch.int32, device='cuda')
    uvs = torch.tensor(uvs, dtype=torch.float32, device='cuda')
    normals = torch.tensor(normals, dtype=torch.float32, device='cuda')
    
    return vertices, triangles, uvs, normals

def create_plane(size=2.0, subdivisions=10):
    """Generate plane geometry for ground"""
    vertices = []
    normals = []
    uvs = []
    triangles = []
    
    for i in range(subdivisions + 1):
        for j in range(subdivisions + 1):
            x = (i / subdivisions - 0.5) * size
            z = (j / subdivisions - 0.5) * size
            y = 0.0
            
            vertices.append([x, y, z, 1.0])
            normals.append([0.0, 1.0, 0.0])
            uvs.append([i / subdivisions, j / subdivisions])
    
    # Generate triangles
    for i in range(subdivisions):
        for j in range(subdivisions):
            v1 = i * (subdivisions + 1) + j
            v2 = v1 + 1
            v3 = (i + 1) * (subdivisions + 1) + j
            v4 = v3 + 1
            
            triangles.append([v1, v3, v2])
            triangles.append([v2, v3, v4])
    
    vertices = torch.tensor(vertices, dtype=torch.float32, device='cuda')
    triangles = torch.tensor(triangles, dtype=torch.int32, device='cuda')
    uvs = torch.tensor(uvs, dtype=torch.float32, device='cuda')
    normals = torch.tensor(normals, dtype=torch.float32, device='cuda')
    
    return vertices, triangles, uvs, normals

# ============================================================================
# Advanced Shading
# ============================================================================

def create_procedural_texture(size=256, pattern='checkerboard'):
    """Generate procedural textures on GPU"""
    if pattern == 'checkerboard':
        # Create checkerboard pattern
        i, j = torch.meshgrid(torch.arange(size, device='cuda'), torch.arange(size, device='cuda'), indexing='ij')
        checker = ((i // 32) + (j // 32)) % 2
        texture = torch.stack([checker, checker, checker], dim=2).float()
        
    elif pattern == 'noise':
        # Simple noise pattern
        texture = torch.rand(size, size, 3, device='cuda')
        
    elif pattern == 'gradient':
        # Gradient pattern
        i, j = torch.meshgrid(torch.arange(size, device='cuda'), torch.arange(size, device='cuda'), indexing='ij')
        r = i.float() / size
        g = j.float() / size
        b = (r + g) / 2
        texture = torch.stack([r, g, b], dim=2)
        
    return texture.unsqueeze(0)  # Add batch dimension

def pbr_lighting(vertices, normals, uvs, material, lights, camera_pos):
    """Advanced PBR-style lighting calculation"""
    # Get surface properties
    albedo = material.albedo
    metallic = material.metallic
    roughness = material.roughness
    
    # Initialize lighting
    final_color = torch.zeros_like(vertices[:, :3])
    
    for light in lights:
        # Calculate light direction
        light_dir = F.normalize(light.position.unsqueeze(0) - vertices[:, :3], dim=1)
        
        # Calculate view direction
        view_dir = F.normalize(camera_pos.unsqueeze(0) - vertices[:, :3], dim=1)
        
        # Calculate half vector
        half_dir = F.normalize(light_dir + view_dir, dim=1)
        
        # Dot products
        n_dot_l = torch.clamp(torch.sum(normals * light_dir, dim=1, keepdim=True), 0.0, 1.0)
        n_dot_v = torch.clamp(torch.sum(normals * view_dir, dim=1, keepdim=True), 0.0, 1.0)
        n_dot_h = torch.clamp(torch.sum(normals * half_dir, dim=1, keepdim=True), 0.0, 1.0)
        
        # Simplified PBR calculations
        # Diffuse component (Lambertian)
        diffuse = albedo * n_dot_l / math.pi
        
        # Specular component (simplified)
        alpha = roughness * roughness
        d = (n_dot_h * n_dot_h * (alpha * alpha - 1.0) + 1.0)
        d = alpha * alpha / (math.pi * d * d)
        
        # Fresnel (Schlick approximation)
        f0 = torch.lerp(torch.tensor(0.04, device='cuda'), albedo, metallic)
        fresnel = f0 + (1.0 - f0) * torch.pow(1.0 - n_dot_v, 5.0)
        
        # Combine lighting
        kd = (1.0 - fresnel) * (1.0 - metallic)
        specular = d * fresnel * 0.25  # Simplified G term
        
        # Final lighting contribution
        light_contrib = (kd * diffuse + specular) * light.color * light.intensity * n_dot_l
        final_color += light_contrib
    
    return final_color

def apply_tone_mapping(color, exposure=1.0, method='reinhard'):
    """Apply tone mapping for HDR to LDR conversion"""
    if method == 'reinhard':
        # Reinhard tone mapping
        color = color * exposure
        return color / (1.0 + color)
    elif method == 'filmic':
        # Simple filmic tone mapping
        color = color * exposure
        return torch.clamp((color * (6.2 * color + 0.5)) / (color * (6.2 * color + 1.7) + 0.06), 0.0, 1.0)
    else:
        return torch.clamp(color * exposure, 0.0, 1.0)

# ============================================================================
# Animation System
# ============================================================================

class Animation:
    """Simple keyframe animation system"""
    def __init__(self):
        self.keyframes = {}
        self.duration = 0.0
        
    def add_keyframe(self, time, property_name, value):
        if property_name not in self.keyframes:
            self.keyframes[property_name] = []
        self.keyframes[property_name].append((time, value))
        self.duration = max(self.duration, time)
        
    def evaluate(self, time, property_name):
        if property_name not in self.keyframes:
            return None
            
        keyframes = self.keyframes[property_name]
        if len(keyframes) == 0:
            return None
        if len(keyframes) == 1:
            return keyframes[0][1]
            
        # Find surrounding keyframes
        t = time % self.duration if self.duration > 0 else 0
        
        for i in range(len(keyframes) - 1):
            t1, v1 = keyframes[i]
            t2, v2 = keyframes[i + 1]
            
            if t1 <= t <= t2:
                # Linear interpolation
                alpha = (t - t1) / (t2 - t1) if t2 != t1 else 0
                if isinstance(v1, (list, tuple)):
                    return [v1[j] + alpha * (v2[j] - v1[j]) for j in range(len(v1))]
                else:
                    return v1 + alpha * (v2 - v1)
        
        return keyframes[-1][1]

def create_rotation_matrix(axis, angle):
    """Create rotation matrix around arbitrary axis"""
    axis = F.normalize(torch.tensor(axis, dtype=torch.float32, device='cuda'), dim=0)
    angle_tensor = torch.tensor(angle, dtype=torch.float32, device='cuda')
    cos_a = torch.cos(angle_tensor)
    sin_a = torch.sin(angle_tensor)
    
    # Rodrigues' rotation formula
    K = torch.tensor([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ], device='cuda')
    
    R = torch.eye(3, device='cuda') + sin_a * K + (1 - cos_a) * (K @ K)
    
    # Convert to 4x4 homogeneous matrix
    R_4x4 = torch.eye(4, device='cuda')
    R_4x4[:3, :3] = R
    return R_4x4

def create_translation_matrix(translation):
    """Create translation matrix"""
    T = torch.eye(4, device='cuda')
    T[:3, 3] = torch.tensor(translation, dtype=torch.float32, device='cuda')
    return T

def create_scale_matrix(scale):
    """Create scale matrix"""
    S = torch.eye(4, device='cuda')
    if isinstance(scale, (list, tuple)):
        S[0, 0] = scale[0]
        S[1, 1] = scale[1]
        S[2, 2] = scale[2]
    else:
        S[:3, :3] *= scale
    return S

# ============================================================================
# Main Rendering Pipeline
# ============================================================================

def setup_environment():
    """Setup CUDA environment"""
    cuda_paths = [
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\bin"
    ]
    
    for cuda_path in cuda_paths:
        if os.path.exists(cuda_path):
            os.add_dll_directory(cuda_path)
    
    os.environ['TORCH_CUDA_ARCH_LIST'] = '8.9'
    print("🚀 Advanced rendering environment configured")

def render_scene(ctx, scene, resolution, time=0.0, enable_lighting=True, enable_tonemapping=True):
    """Main scene rendering function"""
    all_vertices = []
    all_triangles = []
    all_colors = []
    triangle_offset = 0
    
    # Prepare camera matrices
    view_matrix = scene.camera.get_view_matrix()
    proj_matrix = scene.camera.get_projection_matrix()
    mvp_matrix = proj_matrix @ view_matrix
    
    # Render each object
    for obj in scene.objects:
        # Apply object transformations
        vertices = obj.get_transformed_vertices()
        
        # Apply camera transformation
        vertices_clip = (mvp_matrix @ vertices.T).T
        
        if enable_lighting and obj.normals is not None:
            # Apply lighting
            colors = pbr_lighting(
                vertices, obj.normals, obj.uv_coords, 
                obj.material, scene.lights, scene.camera.position
            )
            # Add ambient lighting
            colors += scene.ambient_light * obj.material.albedo
        else:
            # Use material albedo directly
            colors = obj.material.albedo.unsqueeze(0).expand(vertices.shape[0], -1)
        
        # Adjust triangle indices for batching
        triangles = obj.triangles + triangle_offset
        
        all_vertices.append(vertices_clip)
        all_triangles.append(triangles)
        all_colors.append(colors)
        triangle_offset += vertices.shape[0]
    
    if not all_vertices:
        return torch.zeros(1, resolution, resolution, 4, device='cuda')
    
    # Concatenate all geometry
    vertices = torch.cat(all_vertices, dim=0).unsqueeze(0)  # Add batch dimension
    triangles = torch.cat(all_triangles, dim=0)
    colors = torch.cat(all_colors, dim=0).unsqueeze(0)  # Add batch dimension
    
    # Rasterize
    rast_out, rast_out_db = dr.rasterize(ctx, vertices, triangles, resolution=[resolution, resolution])
    
    # Interpolate colors
    color_interpolated, _ = dr.interpolate(colors, rast_out, triangles)
    
    # Apply tone mapping
    if enable_tonemapping:
        color_interpolated = apply_tone_mapping(color_interpolated)
    
    # Alpha channel
    alpha = torch.ones_like(color_interpolated[..., :1])
    output = torch.cat([color_interpolated, alpha], dim=-1)
    
    return output

def save_image(tensor, filename):
    """Save tensor as image"""
    img_np = tensor[0].detach().cpu().numpy()
    img_np = (img_np * 255).astype(np.uint8)
    img = Image.fromarray(img_np)
    img.save(filename)
    print(f"💾 Saved: {filename}")

# ============================================================================
# Demo Scenes
# ============================================================================

def create_demo_scene():
    """Create complex demo scene"""
    scene = Scene()
    
    # Setup camera
    scene.camera.position = torch.tensor([3.0, 2.0, 5.0], dtype=torch.float32, device='cuda')
    scene.camera.target = torch.tensor([0.0, 0.0, 0.0], dtype=torch.float32, device='cuda')
    
    # Create materials
    metal_material = Material(
        albedo=(0.7, 0.7, 0.8), 
        metallic=0.9, 
        roughness=0.1,
        emission=(0.0, 0.0, 0.0)
    )
    
    plastic_material = Material(
        albedo=(0.8, 0.2, 0.2), 
        metallic=0.0, 
        roughness=0.6,
        emission=(0.0, 0.0, 0.0)
    )
    
    glass_material = Material(
        albedo=(0.9, 0.9, 1.0), 
        metallic=0.0, 
        roughness=0.05,
        emission=(0.0, 0.0, 0.0)
    )
    
    ground_material = Material(
        albedo=(0.5, 0.5, 0.5), 
        metallic=0.0, 
        roughness=0.8,
        emission=(0.0, 0.0, 0.0)
    )
    
    # Create objects
    # Central sphere (metal)
    sphere_verts, sphere_tris, sphere_uvs, sphere_normals = create_sphere(radius=0.8)
    sphere = SceneObject(sphere_verts, sphere_tris, metal_material)
    sphere.uv_coords = sphere_uvs
    sphere.normals = sphere_normals
    scene.add_object(sphere)
    
    # Orbiting torus (plastic)
    torus_verts, torus_tris, torus_uvs, torus_normals = create_torus()
    torus = SceneObject(torus_verts, torus_tris, plastic_material)
    torus.uv_coords = torus_uvs
    torus.normals = torus_normals
    torus.transform = create_translation_matrix([2.5, 0.0, 0.0])
    scene.add_object(torus)
    
    # Small sphere (glass)
    small_sphere_verts, small_sphere_tris, small_sphere_uvs, small_sphere_normals = create_sphere(radius=0.4)
    small_sphere = SceneObject(small_sphere_verts, small_sphere_tris, glass_material)
    small_sphere.uv_coords = small_sphere_uvs
    small_sphere.normals = small_sphere_normals
    small_sphere.transform = create_translation_matrix([-1.5, 1.0, 1.0])
    scene.add_object(small_sphere)
    
    # Ground plane
    plane_verts, plane_tris, plane_uvs, plane_normals = create_plane(size=8.0)
    ground = SceneObject(plane_verts, plane_tris, ground_material)
    ground.uv_coords = plane_uvs
    ground.normals = plane_normals
    ground.transform = create_translation_matrix([0.0, -2.0, 0.0])
    scene.add_object(ground)
    
    # Setup lighting
    main_light = Light(
        position=[3.0, 4.0, 3.0], 
        color=[1.0, 0.9, 0.8], 
        intensity=1.5
    )
    scene.add_light(main_light)
    
    fill_light = Light(
        position=[-2.0, 2.0, 2.0], 
        color=[0.5, 0.7, 1.0], 
        intensity=0.8
    )
    scene.add_light(fill_light)
    
    # Ambient lighting
    scene.ambient_light = torch.tensor([0.15, 0.15, 0.2], dtype=torch.float32, device='cuda')
    
    return scene

def demo_advanced_rendering():
    """Advanced rendering demo with multiple features"""
    print("🎨 Advanced nvdiffrast Complex Demo")
    print("=====================================")
    
    setup_environment()
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return
    
    print(f"✅ Device: {torch.cuda.get_device_name(0)}")
    print()
    
    # Create rendering context
    ctx = dr.RasterizeCudaContext()
    
    # Create demo scene
    scene = create_demo_scene()
    
    # Render static scene
    print("🖼️  Rendering static scene...")
    output = render_scene(ctx, scene, resolution=1024)
    save_image(output, "advanced_scene_static.png")
    
    # Render animated sequence
    print("🎬 Rendering animation sequence...")
    num_frames = 60
    
    for frame in range(num_frames):
        time = frame / num_frames * 2 * math.pi
        
        # Animate torus rotation around center
        torus = scene.objects[1]  # Second object is torus
        rotation = create_rotation_matrix([0, 1, 0], time)
        translation = create_translation_matrix([2.5, 0.0, 0.0])
        torus.transform = rotation @ translation
        
        # Animate small sphere bobbing
        small_sphere = scene.objects[2]
        bob_y = 1.0 + 0.5 * math.sin(time * 3)
        small_sphere.transform = create_translation_matrix([-1.5, bob_y, 1.0])
        
        # Animate main light position
        light_x = 3.0 * math.cos(time * 0.5)
        light_z = 3.0 * math.sin(time * 0.5)
        scene.lights[0].position = torch.tensor([light_x, 4.0, light_z], dtype=torch.float32, device='cuda')
        
        # Render frame
        output = render_scene(ctx, scene, resolution=512)
        filename = f"advanced_anim_{frame:03d}.png"
        save_image(output, filename)
        
        if frame % 10 == 0:
            print(f"   Frame {frame}/{num_frames}")
    
    print("🎉 Advanced demo completed!")
    print("📁 Generated files:")
    print("   - advanced_scene_static.png (high-res static scene)")
    print("   - advanced_anim_*.png (60-frame animation)")

def main():
    """Main demo function with command line options"""
    parser = argparse.ArgumentParser(description='Advanced nvdiffrast Complex Demo')
    parser.add_argument('--resolution', type=int, default=1024, help='Render resolution')
    parser.add_argument('--frames', type=int, default=60, help='Animation frames')
    parser.add_argument('--no-lighting', action='store_true', help='Disable advanced lighting')
    parser.add_argument('--no-tonemapping', action='store_true', help='Disable tone mapping')
    parser.add_argument('--static-only', action='store_true', help='Render static scene only')
    
    args = parser.parse_args()
    
    try:
        demo_advanced_rendering()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()