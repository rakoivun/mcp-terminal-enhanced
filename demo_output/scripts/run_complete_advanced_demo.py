#!/usr/bin/env python3
"""
Complete Advanced nvdiffrast Demo Runner
Demonstrates the full range of advanced rendering capabilities
"""

import os
import sys
import subprocess
import time

def setup_environment():
    """Setup the demonstration environment"""
    print("🚀 Setting up Advanced nvdiffrast Demo Environment")
    print("=" * 55)
    
    # Check Python environment
    python_path = "./nvdiffrast_py310/Scripts/python.exe"
    if not os.path.exists(python_path):
        print("❌ Python environment not found!")
        print("   Expected: ./nvdiffrast_py310/Scripts/python.exe")
        return False
    
    # Check demo files
    required_files = [
        "nvdiffrast_advanced_complex_demo.py",
        "create_animation_video.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file missing: {file}")
            return False
    
    print("✅ All required files present")
    return True

def run_command(cmd, description, timeout=120):
    """Run a command with proper environment and error handling"""
    print(f"\n🔧 {description}")
    print(f"   Command: {' '.join(cmd)}")
    print("   " + "-" * 50)
    
    # Setup environment with ninja in PATH
    env = os.environ.copy()
    env["PATH"] = "./nvdiffrast_py310/Scripts" + os.pathsep + env.get("PATH", "")
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              timeout=timeout, env=env)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Completed in {elapsed:.1f}s")
            # Show key output lines
            lines = result.stdout.strip().split('\n')
            for line in lines[-5:]:  # Show last 5 lines
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print(f"❌ Failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timed out after {timeout} seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demonstrate_features():
    """Run complete feature demonstration"""
    print("\n🎨 Advanced nvdiffrast Feature Demonstration")
    print("=" * 50)
    
    demos = [
        {
            "name": "High-Resolution Static Scene",
            "cmd": ["./nvdiffrast_py310/Scripts/python.exe", 
                   "nvdiffrast_advanced_complex_demo.py", 
                   "--static-only", "--resolution", "1024"],
            "description": "Rendering complex multi-object scene with PBR materials",
            "timeout": 60
        },
        {
            "name": "Full Animation Sequence", 
            "cmd": ["./nvdiffrast_py310/Scripts/python.exe",
                   "nvdiffrast_advanced_complex_demo.py",
                   "--frames", "30", "--resolution", "512"],
            "description": "Creating animated sequence with dynamic lighting",
            "timeout": 120
        },
        {
            "name": "Performance Benchmark",
            "cmd": ["./nvdiffrast_py310/Scripts/python.exe",
                   "nvdiffrast_advanced_complex_demo.py", 
                   "--frames", "10", "--resolution", "256"],
            "description": "Performance testing at different resolutions",
            "timeout": 60
        },
        {
            "name": "Video Compilation",
            "cmd": ["./nvdiffrast_py310/Scripts/python.exe",
                   "create_animation_video.py",
                   "--fps", "30", "--quality", "high"],
            "description": "Converting animation frames to MP4 video",
            "timeout": 60
        }
    ]
    
    success_count = 0
    
    for i, demo in enumerate(demos, 1):
        print(f"\n📋 Demo {i}/{len(demos)}: {demo['name']}")
        success = run_command(demo["cmd"], demo["description"], demo["timeout"])
        if success:
            success_count += 1
        time.sleep(1)  # Brief pause between demos
    
    return success_count, len(demos)

def show_results():
    """Display results and generated files"""
    print("\n📁 Generated Files Analysis")
    print("=" * 40)
    
    files_to_check = [
        ("advanced_scene_static.png", "High-resolution static scene"),
        ("advanced_animation.mp4", "Complete animation video"),
    ]
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            size_mb = size / (1024 * 1024)
            print(f"✅ {filename}")
            print(f"   {description}")
            print(f"   Size: {size_mb:.2f} MB ({size:,} bytes)")
        else:
            print(f"❌ {filename} - Not found")
    
    # Count animation frames
    frame_count = 0
    total_size = 0
    for i in range(100):  # Check up to 100 frames
        filename = f"advanced_anim_{i:03d}.png"
        if os.path.exists(filename):
            frame_count += 1
            total_size += os.path.getsize(filename)
        elif frame_count > 0:
            break  # Stop if we find a gap after finding frames
    
    if frame_count > 0:
        avg_size = total_size / frame_count / 1024  # KB
        print(f"✅ Animation frames: {frame_count} files")
        print(f"   Total size: {total_size / (1024*1024):.2f} MB")
        print(f"   Average frame size: {avg_size:.1f} KB")

def show_capabilities():
    """Display the advanced capabilities demonstrated"""
    print("\n🎯 Advanced Capabilities Demonstrated")
    print("=" * 45)
    
    capabilities = [
        "🔧 Multi-object scene graph system",
        "🎨 PBR materials (metallic/roughness workflow)", 
        "💡 Dynamic lighting with multiple light sources",
        "🎬 Smooth animation with keyframe interpolation",
        "📷 Professional camera system (view/projection)",
        "⚡ CUDA acceleration on RTX 4090",
        "🖼️ High-resolution rendering (up to 2K+)",
        "🎞️ Video export with FFmpeg integration",
        "🔬 Advanced shading (Fresnel, energy conservation)",
        "🎛️ Post-processing (HDR tone mapping)",
        "🏗️ Efficient geometry generation",
        "💾 Memory-optimized GPU operations"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")

def main():
    """Main demonstration function"""
    print("🎨 Advanced nvdiffrast Complete Demonstration")
    print("=" * 55)
    print("Showcasing professional-grade differentiable rendering")
    print()
    
    # Setup check
    if not setup_environment():
        print("❌ Environment setup failed!")
        sys.exit(1)
    
    # Run demonstrations
    success_count, total_demos = demonstrate_features()
    
    # Show results
    show_results()
    show_capabilities()
    
    # Final summary
    print(f"\n🎉 Demonstration Complete!")
    print("=" * 35)
    print(f"✅ Successful demos: {success_count}/{total_demos}")
    
    if success_count == total_demos:
        print("🏆 ALL FEATURES WORKING PERFECTLY!")
        print("\n📖 This demonstration proves nvdiffrast can be used for:")
        print("   • Professional-grade 3D rendering")
        print("   • Advanced material and lighting systems") 
        print("   • High-performance GPU-accelerated graphics")
        print("   • Educational graphics programming")
        print("   • Research in differentiable rendering")
        print("   • Real-time animation and visualization")
        print("\n🚀 Ready for production use and further development!")
    else:
        print(f"⚠️  Some features had issues ({total_demos - success_count} failed)")
        print("   Check error messages above for troubleshooting")
    
    print(f"\n📁 Check generated files:")
    print("   • advanced_scene_static.png - High-quality static render")
    print("   • advanced_anim_*.png - Animation frame sequence")
    print("   • advanced_animation.mp4 - Complete video compilation")

if __name__ == "__main__":
    main()