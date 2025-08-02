#!/usr/bin/env python3
"""
Advanced nvdiffrast RTX 4090 Demos
Showcasing the power of differentiable rendering with gradient-based optimization
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import nvdiffrast.torch as dr
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import math

def setup_environment():
    """Setup CUDA environment for RTX 4090"""
    cuda_paths = [
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\bin"
    ]
    
    for cuda_path in cuda_paths:
        if os.path.exists(cuda_path):
            os.add_dll_directory(cuda_path)
    
    os.environ['TORCH_CUDA_ARCH_LIST'] = '8.9'  # RTX 4090
    print("🚀 Advanced demos configured for RTX 4090")

def save_image(tensor, filename, title=None):
    """Save tensor as image with optional title"""
    img_np = tensor[0].detach().cpu().numpy()
    img_np = np.clip(img_np, 0, 1)
    img_np = (img_np * 255).astype(np.uint8)
    
    if img_np.shape[-1] == 4:  # RGBA
        img_np = img_np[..., :3]  # Convert to RGB
    
    img = Image.fromarray(img_np)
    img.save(filename)
    print(f"💾 Saved: {filename}")

def create_sphere_mesh(radius=1.0, subdivisions=3):
    """Create a sphere mesh using icosphere subdivision"""
    # Start with icosahedron vertices
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    vertices = np.array([
        [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
        [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
        [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
    ], dtype=np.float32)
    
    # Normalize to unit sphere
    vertices = vertices / np.linalg.norm(vertices, axis=1, keepdims=True) * radius
    
    # Icosahedron faces
    faces = np.array([
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ], dtype=np.int32)
    
    # Convert to torch tensors
    vertices_torch = torch.tensor(vertices, device='cuda')
    # Add homogeneous coordinate
    vertices_torch = torch.cat([vertices_torch, torch.ones(vertices_torch.shape[0], 1, device='cuda')], dim=1)
    faces_torch = torch.tensor(faces, device='cuda')
    
    return vertices_torch.unsqueeze(0), faces_torch

def demo_1_mesh_deformation():
    """Demo 1: Neural mesh deformation - optimize vertex positions to match target shape"""
    print("🔄 Demo 1: Neural Mesh Deformation")
    print("   Goal: Deform a sphere into a cube using gradient descent")
    
    ctx = dr.RasterizeCudaContext()
    resolution = 512
    
    # Create initial sphere mesh
    initial_vertices, faces = create_sphere_mesh()
    
    # Create target cube corners as reference points
    target_shape = torch.tensor([
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5],
        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5]
    ], device='cuda')
    
    # Make vertices learnable parameters
    learnable_vertices = nn.Parameter(initial_vertices[0, :, :3].clone())
    optimizer = optim.Adam([learnable_vertices], lr=0.01)
    
    print("   Optimizing vertex positions...")
    losses = []
    
    for epoch in tqdm(range(200), desc="   Deforming mesh"):
        optimizer.zero_grad()
        
        # Add homogeneous coordinate
        vertices_4d = torch.cat([learnable_vertices, torch.ones(learnable_vertices.shape[0], 1, device='cuda')], dim=1)
        vertices_batch = vertices_4d.unsqueeze(0)
        
        # Render current mesh
        rast_out, _ = dr.rasterize(ctx, vertices_batch, faces, resolution=[resolution, resolution])
        
        # Simple loss: encourage vertices to move toward cube-like positions
        # Loss 1: Regularity (smooth deformation)
        center = learnable_vertices.mean(dim=0, keepdim=True)
        distances = torch.norm(learnable_vertices - center, dim=1)
        regularity_loss = torch.var(distances) * 0.1
        
        # Loss 2: Cube-like shape encouragement
        abs_coords = torch.abs(learnable_vertices)
        cube_loss = torch.mean((abs_coords.max(dim=1)[0] - 0.7) ** 2)
        
        total_loss = regularity_loss + cube_loss
        losses.append(total_loss.item())
        
        total_loss.backward()
        optimizer.step()
        
        # Save intermediate results
        if epoch % 50 == 0:
            colors = torch.ones(1, learnable_vertices.shape[0], 3, device='cuda') * 0.7
            colors[0, :, 0] = torch.linspace(0.2, 1.0, learnable_vertices.shape[0])  # Red gradient
            
            color_interpolated, _ = dr.interpolate(colors, rast_out, faces)
            alpha = torch.ones_like(color_interpolated[..., :1])
            output = torch.cat([color_interpolated, alpha], dim=-1)
            
            save_image(output, f"mesh_deformation_epoch_{epoch:03d}.png")
    
    print(f"   ✅ Deformation complete! Loss: {losses[0]:.4f} → {losses[-1]:.4f}")
    
    # Create final comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.plot(losses)
    ax1.set_title('Deformation Loss Over Time')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.grid(True)
    
    # Show vertex displacement
    initial_pos = initial_vertices[0, :, :3].cpu().numpy()
    final_pos = learnable_vertices.detach().cpu().numpy()
    displacement = np.linalg.norm(final_pos - initial_pos, axis=1)
    
    ax2.hist(displacement, bins=20, alpha=0.7)
    ax2.set_title('Vertex Displacement Distribution')
    ax2.set_xlabel('Displacement Distance')
    ax2.set_ylabel('Number of Vertices')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('mesh_deformation_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   📊 Saved analysis: mesh_deformation_analysis.png")

def demo_2_texture_optimization():
    """Demo 2: Neural texture optimization - learn texture to match target image"""
    print("🎨 Demo 2: Neural Texture Optimization")
    print("   Goal: Learn texture that produces target checker pattern")
    
    ctx = dr.RasterizeCudaContext()
    resolution = 512
    
    # Create simple quad mesh
    vertices = torch.tensor([
        [-1, -1, 0, 1], [1, -1, 0, 1], [1, 1, 0, 1], [-1, 1, 0, 1]
    ], dtype=torch.float32, device='cuda').unsqueeze(0)
    
    faces = torch.tensor([[0, 1, 2], [2, 3, 0]], dtype=torch.int32, device='cuda')
    
    # UV coordinates for texture mapping
    uvs = torch.tensor([
        [0, 0], [1, 0], [1, 1], [0, 1]
    ], dtype=torch.float32, device='cuda').unsqueeze(0)
    
    # Create target checker pattern
    checker_size = 8
    target_pattern = torch.zeros(resolution, resolution, 3, device='cuda')
    for i in range(checker_size):
        for j in range(checker_size):
            y_start = i * resolution // checker_size
            y_end = (i + 1) * resolution // checker_size
            x_start = j * resolution // checker_size
            x_end = (j + 1) * resolution // checker_size
            
            if (i + j) % 2 == 0:
                target_pattern[y_start:y_end, x_start:x_end] = torch.tensor([1.0, 0.2, 0.2], device='cuda')  # Red
            else:
                target_pattern[y_start:y_end, x_start:x_end] = torch.tensor([0.2, 0.2, 1.0], device='cuda')  # Blue
    
    # Save target pattern
    target_img = target_pattern.unsqueeze(0)
    alpha = torch.ones_like(target_img[..., :1])
    target_with_alpha = torch.cat([target_img, alpha], dim=-1)
    save_image(target_with_alpha, "texture_target.png")
    
    # Create learnable texture (smaller resolution for efficiency)
    texture_size = 64
    learnable_texture = nn.Parameter(torch.rand(texture_size, texture_size, 3, device='cuda') * 0.5 + 0.25)
    optimizer = optim.Adam([learnable_texture], lr=0.02)
    
    print("   Optimizing texture...")
    losses = []
    
    for epoch in tqdm(range(500), desc="   Learning texture"):
        optimizer.zero_grad()
        
        # Render with current texture
        rast_out, _ = dr.rasterize(ctx, vertices, faces, resolution=[resolution, resolution])
        
        # Interpolate UV coordinates
        uv_interpolated, _ = dr.interpolate(uvs, rast_out, faces)
        
        # Sample texture using bilinear interpolation
        # Convert UV [0,1] to texture coordinates
        tex_coords = uv_interpolated * (texture_size - 1)
        
        # Manual bilinear sampling (simplified)
        u = tex_coords[..., 0].clamp(0, texture_size - 1)
        v = tex_coords[..., 1].clamp(0, texture_size - 1)
        
        u0 = u.floor().long()
        v0 = v.floor().long()
        u1 = (u0 + 1).clamp(max=texture_size - 1)
        v1 = (v0 + 1).clamp(max=texture_size - 1)
        
        # Get texture values at corners
        tex_00 = learnable_texture[v0, u0]
        tex_01 = learnable_texture[v1, u0]
        tex_10 = learnable_texture[v0, u1]
        tex_11 = learnable_texture[v1, u1]
        
        # Bilinear weights
        wu = (u - u0.float()).unsqueeze(-1)
        wv = (v - v0.float()).unsqueeze(-1)
        
        # Bilinear interpolation
        tex_top = tex_00 * (1 - wu) + tex_10 * wu
        tex_bottom = tex_01 * (1 - wu) + tex_11 * wu
        sampled_texture = tex_top * (1 - wv) + tex_bottom * wv
        
        # Create output image
        mask = rast_out[..., 3:4] > 0
        output_color = sampled_texture * mask
        
        # Loss: match target pattern
        loss = torch.mean((output_color - target_pattern.unsqueeze(0)) ** 2 * mask)
        
        # Regularization: smooth texture
        smooth_loss = torch.mean((learnable_texture[1:] - learnable_texture[:-1]) ** 2) + \
                     torch.mean((learnable_texture[:, 1:] - learnable_texture[:, :-1]) ** 2)
        
        total_loss = loss + smooth_loss * 0.001
        losses.append(total_loss.item())
        
        total_loss.backward()
        optimizer.step()
        
        # Clamp texture values
        with torch.no_grad():
            learnable_texture.clamp_(0, 1)
        
        # Save intermediate results
        if epoch % 100 == 0:
            alpha = torch.ones_like(output_color[..., :1])
            output = torch.cat([output_color, alpha], dim=-1)
            save_image(output, f"texture_learning_epoch_{epoch:03d}.png")
    
    print(f"   ✅ Texture optimization complete! Loss: {losses[0]:.4f} → {losses[-1]:.4f}")
    
    # Save final learned texture
    final_texture = learnable_texture.detach().unsqueeze(0)
    alpha = torch.ones_like(final_texture[..., :1])
    texture_with_alpha = torch.cat([final_texture, alpha], dim=-1)
    save_image(texture_with_alpha, "learned_texture.png")
    
    # Loss plot
    plt.figure(figsize=(10, 5))
    plt.plot(losses)
    plt.title('Texture Learning Loss Over Time')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.yscale('log')
    plt.savefig('texture_learning_loss.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   📊 Saved analysis: texture_learning_loss.png")

def demo_3_lighting_optimization():
    """Demo 3: Optimize lighting parameters to match target lighting"""
    print("💡 Demo 3: Neural Lighting Optimization")
    print("   Goal: Learn lighting that produces target shading")
    
    ctx = dr.RasterizeCudaContext()
    resolution = 512
    
    # Create sphere mesh for lighting demo
    vertices, faces = create_sphere_mesh()
    
    # Compute vertex normals (simplified - using vertex positions as normals for sphere)
    normals = vertices[0, :, :3]  # For unit sphere, position = normal
    normals = normals / torch.norm(normals, dim=1, keepdim=True)
    normals = normals.unsqueeze(0)
    
    # Target lighting: create a specific lighting pattern
    target_light_dir = torch.tensor([0.5, 0.7, 0.5], device='cuda')
    target_light_dir = target_light_dir / torch.norm(target_light_dir)
    
    # Render target lighting
    target_lighting = torch.clamp(torch.sum(normals * target_light_dir.unsqueeze(0).unsqueeze(0), dim=2, keepdim=True), 0, 1)
    target_colors = target_lighting.repeat(1, 1, 3) * torch.tensor([0.8, 0.6, 0.9], device='cuda')
    
    rast_out, _ = dr.rasterize(ctx, vertices, faces, resolution=[resolution, resolution])
    target_shading, _ = dr.interpolate(target_colors, rast_out, faces)
    alpha = torch.ones_like(target_shading[..., :1])
    target_output = torch.cat([target_shading, alpha], dim=-1)
    save_image(target_output, "lighting_target.png")
    
    # Learnable lighting parameters
    learnable_light_dir = nn.Parameter(torch.tensor([0.1, 0.1, 0.1], device='cuda'))
    learnable_light_color = nn.Parameter(torch.tensor([0.5, 0.5, 0.5], device='cuda'))
    learnable_ambient = nn.Parameter(torch.tensor([0.1], device='cuda'))
    
    optimizer = optim.Adam([learnable_light_dir, learnable_light_color, learnable_ambient], lr=0.05)
    
    print("   Optimizing lighting...")
    losses = []
    light_directions = []
    
    for epoch in tqdm(range(300), desc="   Learning lighting"):
        optimizer.zero_grad()
        
        # Normalize light direction
        light_dir_normalized = learnable_light_dir / (torch.norm(learnable_light_dir) + 1e-8)
        light_directions.append(light_dir_normalized.detach().cpu().numpy())
        
        # Compute lighting
        diffuse = torch.clamp(torch.sum(normals * light_dir_normalized.unsqueeze(0).unsqueeze(0), dim=2, keepdim=True), 0, 1)
        
        # Apply lighting color and ambient
        lit_colors = (diffuse * learnable_light_color.unsqueeze(0).unsqueeze(0) + 
                     learnable_ambient.unsqueeze(0).unsqueeze(0).unsqueeze(0).repeat(1, normals.shape[1], 3))
        
        # Clamp colors
        lit_colors = torch.clamp(lit_colors, 0, 1)
        
        # Render
        current_shading, _ = dr.interpolate(lit_colors, rast_out, faces)
        
        # Loss: match target shading
        mask = rast_out[..., 3:4] > 0
        loss = torch.mean((current_shading - target_shading) ** 2 * mask)
        losses.append(loss.item())
        
        loss.backward()
        optimizer.step()
        
        # Clamp parameters
        with torch.no_grad():
            learnable_light_color.clamp_(0, 2)
            learnable_ambient.clamp_(0, 0.5)
        
        # Save intermediate results
        if epoch % 75 == 0:
            alpha = torch.ones_like(current_shading[..., :1])
            output = torch.cat([current_shading, alpha], dim=-1)
            save_image(output, f"lighting_learning_epoch_{epoch:03d}.png")
    
    print(f"   ✅ Lighting optimization complete! Loss: {losses[0]:.4f} → {losses[-1]:.4f}")
    print(f"   💡 Final light direction: [{learnable_light_dir[0]:.3f}, {learnable_light_dir[1]:.3f}, {learnable_light_dir[2]:.3f}]")
    print(f"   🎨 Final light color: [{learnable_light_color[0]:.3f}, {learnable_light_color[1]:.3f}, {learnable_light_color[2]:.3f}]")
    print(f"   🌙 Final ambient: {learnable_ambient[0]:.3f}")
    
    # Create analysis plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Loss over time
    ax1.plot(losses)
    ax1.set_title('Lighting Optimization Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.grid(True)
    ax1.set_yscale('log')
    
    # Light direction evolution
    light_dirs = np.array(light_directions)
    ax2.plot(light_dirs[:, 0], label='X')
    ax2.plot(light_dirs[:, 1], label='Y')
    ax2.plot(light_dirs[:, 2], label='Z')
    ax2.set_title('Light Direction Evolution')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Direction Component')
    ax2.legend()
    ax2.grid(True)
    
    # 3D light direction trajectory
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    ax3.plot(light_dirs[:, 0], light_dirs[:, 1], light_dirs[:, 2], 'b-', alpha=0.7)
    ax3.scatter([light_dirs[0, 0]], [light_dirs[0, 1]], [light_dirs[0, 2]], color='green', s=100, label='Start')
    ax3.scatter([light_dirs[-1, 0]], [light_dirs[-1, 1]], [light_dirs[-1, 2]], color='red', s=100, label='End')
    ax3.set_title('Light Direction 3D Trajectory')
    ax3.legend()
    
    # Parameter evolution
    ax4.text(0.1, 0.8, f"Target: [{target_light_dir[0]:.3f}, {target_light_dir[1]:.3f}, {target_light_dir[2]:.3f}]", transform=ax4.transAxes)
    ax4.text(0.1, 0.6, f"Learned: [{learnable_light_dir[0]:.3f}, {learnable_light_dir[1]:.3f}, {learnable_light_dir[2]:.3f}]", transform=ax4.transAxes)
    ax4.text(0.1, 0.4, f"Color: [{learnable_light_color[0]:.3f}, {learnable_light_color[1]:.3f}, {learnable_light_color[2]:.3f}]", transform=ax4.transAxes)
    ax4.text(0.1, 0.2, f"Ambient: {learnable_ambient[0]:.3f}", transform=ax4.transAxes)
    ax4.set_title('Final Parameters')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig('lighting_optimization_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   📊 Saved analysis: lighting_optimization_analysis.png")

def demo_4_inverse_rendering():
    """Demo 4: Inverse rendering - reconstruct 3D shape from 2D silhouette"""
    print("🔍 Demo 4: Inverse Rendering")
    print("   Goal: Reconstruct 3D shape from 2D target silhouette")
    
    ctx = dr.RasterizeCudaContext()
    resolution = 256  # Smaller for faster optimization
    
    # Create target shape silhouette (heart shape)
    target_silhouette = torch.zeros(resolution, resolution, device='cuda')
    
    y, x = torch.meshgrid(torch.linspace(-1, 1, resolution, device='cuda'),
                         torch.linspace(-1, 1, resolution, device='cuda'))
    
    # Heart equation: (x^2 + y^2 - 1)^3 - x^2 * y^3 = 0
    # Simplified heart shape
    heart_condition = ((x**2 + y**2 - 0.5)**3 - x**2 * y**3 < 0.1) & (y > -0.5)
    target_silhouette[heart_condition] = 1.0
    
    # Save target silhouette
    target_img = target_silhouette.unsqueeze(0).unsqueeze(-1).repeat(1, 1, 1, 3)
    alpha = torch.ones_like(target_img[..., :1])
    target_with_alpha = torch.cat([target_img, alpha], dim=-1)
    save_image(target_with_alpha, "inverse_target_silhouette.png")
    
    # Start with sphere mesh
    initial_vertices, faces = create_sphere_mesh(radius=0.8, subdivisions=2)
    
    # Make vertices learnable
    learnable_vertices = nn.Parameter(initial_vertices[0, :, :3].clone())
    optimizer = optim.Adam([learnable_vertices], lr=0.01)
    
    print("   Reconstructing shape from silhouette...")
    losses = []
    
    for epoch in tqdm(range(400), desc="   Shape reconstruction"):
        optimizer.zero_grad()
        
        # Add homogeneous coordinate
        vertices_4d = torch.cat([learnable_vertices, torch.ones(learnable_vertices.shape[0], 1, device='cuda')], dim=1)
        vertices_batch = vertices_4d.unsqueeze(0)
        
        # Render silhouette
        rast_out, _ = dr.rasterize(ctx, vertices_batch, faces, resolution=[resolution, resolution])
        rendered_silhouette = (rast_out[0, :, :, 3] > 0).float()  # Alpha channel as silhouette
        
        # Loss: match target silhouette
        silhouette_loss = torch.mean((rendered_silhouette - target_silhouette) ** 2)
        
        # Regularization: keep shape smooth
        center = learnable_vertices.mean(dim=0, keepdim=True)
        distances = torch.norm(learnable_vertices - center, dim=1)
        smoothness_loss = torch.var(distances) * 0.1
        
        # Prevent degenerate triangles
        edge_lengths = []
        for face in faces:
            v0, v1, v2 = learnable_vertices[face[0]], learnable_vertices[face[1]], learnable_vertices[face[2]]
            edge_lengths.extend([
                torch.norm(v1 - v0),
                torch.norm(v2 - v1),
                torch.norm(v0 - v2)
            ])
        edge_length_loss = torch.var(torch.stack(edge_lengths)) * 0.01
        
        total_loss = silhouette_loss + smoothness_loss + edge_length_loss
        losses.append(total_loss.item())
        
        total_loss.backward()
        optimizer.step()
        
        # Save intermediate results
        if epoch % 100 == 0:
            # Render with colors for visualization
            colors = torch.ones(1, learnable_vertices.shape[0], 3, device='cuda')
            colors[0, :, 0] = torch.sigmoid(learnable_vertices[:, 2] * 3)  # Color by Z coordinate
            colors[0, :, 1] = 0.5
            colors[0, :, 2] = 1 - colors[0, :, 0]
            
            color_interpolated, _ = dr.interpolate(colors, rast_out, faces)
            alpha = rast_out[..., 3:4]
            output = torch.cat([color_interpolated, alpha], dim=-1)
            save_image(output, f"inverse_reconstruction_epoch_{epoch:03d}.png")
            
            # Also save silhouette comparison
            silhouette_comparison = torch.stack([
                target_silhouette,
                rendered_silhouette,
                torch.abs(target_silhouette - rendered_silhouette)
            ], dim=0).unsqueeze(-1).repeat(1, 1, 1, 3)
            alpha_comp = torch.ones_like(silhouette_comparison[..., :1])
            silhouette_with_alpha = torch.cat([silhouette_comparison, alpha_comp], dim=-1)
            save_image(silhouette_with_alpha, f"inverse_silhouette_comparison_epoch_{epoch:03d}.png")
    
    print(f"   ✅ Shape reconstruction complete! Loss: {losses[0]:.4f} → {losses[-1]:.4f}")
    
    # Final analysis
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.plot(losses)
    plt.title('Reconstruction Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.yscale('log')
    
    plt.subplot(1, 3, 2)
    plt.imshow(target_silhouette.cpu().numpy(), cmap='gray')
    plt.title('Target Silhouette')
    plt.axis('off')
    
    final_rast, _ = dr.rasterize(ctx, vertices_batch, faces, resolution=[resolution, resolution])
    final_silhouette = (final_rast[0, :, :, 3] > 0).float()
    
    plt.subplot(1, 3, 3)
    plt.imshow(final_silhouette.detach().cpu().numpy(), cmap='gray')
    plt.title('Reconstructed Silhouette')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('inverse_rendering_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   📊 Saved analysis: inverse_rendering_analysis.png")

def main():
    """Run all advanced demos"""
    print("🌟 Advanced nvdiffrast RTX 4090 Demos")
    print("=====================================")
    print("Showcasing differentiable rendering with gradient-based optimization")
    print()
    
    setup_environment()
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return
    
    print(f"✅ Using device: {torch.cuda.get_device_name(0)}")
    print(f"✅ CUDA memory: {torch.cuda.get_device_properties(0).total_memory // 1024**3} GB")
    print()
    
    try:
        # Run advanced demos
        demo_1_mesh_deformation()
        print()
        
        demo_2_texture_optimization()
        print()
        
        demo_3_lighting_optimization()
        print()
        
        demo_4_inverse_rendering()
        print()
        
        print("🎉 All advanced demos completed successfully!")
        print()
        print("📁 Generated files:")
        print("   🔄 Mesh deformation sequence: mesh_deformation_epoch_*.png")
        print("   🎨 Texture learning sequence: texture_learning_epoch_*.png")
        print("   💡 Lighting optimization: lighting_learning_epoch_*.png")
        print("   🔍 Shape reconstruction: inverse_reconstruction_epoch_*.png")
        print("   📊 Analysis plots: *_analysis.png")
        print()
        print("🧠 These demos showcase the power of differentiable rendering:")
        print("   • Neural mesh optimization using gradients")
        print("   • Texture synthesis through optimization")
        print("   • Lighting parameter estimation")
        print("   • Inverse rendering and 3D reconstruction")
        print()
        print("🚀 Your RTX 4090 is crushing these ML graphics workloads!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()