#!/usr/bin/env python3
"""
Automated nvdiffrast DLL dependency fix
Run this script to resolve runtime DLL loading issues on Windows
"""

import os
import sys
import subprocess
import ctypes
from pathlib import Path

def add_cuda_dll_directories():
    """Add CUDA DLL directories to Python DLL search path"""
    print("🔧 Adding CUDA DLL directories...")
    
    cuda_paths = [
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0\bin", 
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\bin"
    ]
    
    added_paths = []
    for cuda_path in cuda_paths:
        if os.path.exists(cuda_path):
            try:
                os.add_dll_directory(cuda_path)
                added_paths.append(cuda_path)
                print(f"✅ Added CUDA DLL directory: {cuda_path}")
            except Exception as e:
                print(f"⚠️  Failed to add {cuda_path}: {e}")
    
    if not added_paths:
        print("❌ No CUDA installations found!")
        return False
    
    return True

def set_environment_variables():
    """Set required environment variables"""
    print("🔧 Setting environment variables...")
    
    env_vars = {
        'TORCH_CUDA_ARCH_LIST': '8.9',  # RTX 4090 architecture
        'TORCH_EXTENSIONS_DIR': os.path.expanduser(r'~\AppData\Local\torch_extensions'),
        'CUDA_LAUNCH_BLOCKING': '1',  # Better error messages
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✅ Set {key}={value}")

def check_visual_cpp_runtime():
    """Check if Visual C++ redistributables are available"""
    print("🔧 Checking Visual C++ runtime...")
    
    try:
        # Try to load common MSVC runtime DLLs
        msvcrt = ctypes.CDLL("msvcrt.dll")
        print("✅ MSVCRT runtime available")
        
        # Check for MSVCP (C++ runtime)
        try:
            msvcp = ctypes.CDLL("msvcp140.dll")
            print("✅ MSVCP140 runtime available") 
        except OSError:
            print("⚠️  MSVCP140 runtime missing - install Visual C++ 2015-2022 Redistributable")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Visual C++ runtime check failed: {e}")
        return False

def test_cuda_dlls():
    """Test if CUDA runtime DLLs can be loaded"""
    print("🔧 Testing CUDA DLL loading...")
    
    cuda_dlls = [
        "cudart64_110.dll",
        "cudart64_118.dll", 
        "cudart64_12.dll"
    ]
    
    for dll_name in cuda_dlls:
        try:
            cuda_dll = ctypes.CDLL(dll_name)
            print(f"✅ {dll_name} loaded successfully")
            return True
        except OSError:
            print(f"⚠️  {dll_name} not found")
            continue
    
    print("❌ No CUDA runtime DLLs could be loaded")
    return False

def test_nvdiffrast_basic():
    """Test basic nvdiffrast import"""
    print("🧪 Testing nvdiffrast basic import...")
    
    try:
        import nvdiffrast.torch as dr
        print("✅ nvdiffrast import successful")
        return True
    except ImportError as e:
        print(f"❌ nvdiffrast import failed: {e}")
        return False

def test_nvdiffrast_contexts():
    """Test nvdiffrast context creation"""
    print("🧪 Testing nvdiffrast context creation...")
    
    try:
        import nvdiffrast.torch as dr
        
        # Test CUDA context
        print("  Testing CUDA context...")
        try:
            cuda_ctx = dr.RasterizeCudaContext()
            print("✅ CUDA context created successfully")
            cuda_success = True
        except Exception as e:
            print(f"❌ CUDA context failed: {e}")
            cuda_success = False
        
        # Test OpenGL context  
        print("  Testing OpenGL context...")
        try:
            gl_ctx = dr.RasterizeGLContext()
            print("✅ OpenGL context created successfully")
            gl_success = True
        except Exception as e:
            print(f"❌ OpenGL context failed: {e}")
            gl_success = False
        
        return cuda_success or gl_success
        
    except Exception as e:
        print(f"❌ Context testing failed: {e}")
        return False

def run_basic_rendering_test():
    """Run a basic rendering test to verify functionality"""
    print("🧪 Running basic rendering test...")
    
    try:
        import torch
        import nvdiffrast.torch as dr
        
        # Create simple triangle data
        vertices = torch.tensor([[[0.0, 0.0, 0.0, 1.0],
                                 [1.0, 0.0, 0.0, 1.0],
                                 [0.0, 1.0, 0.0, 1.0]]], device='cuda')
        
        triangles = torch.tensor([[0, 1, 2]], dtype=torch.int32, device='cuda')
        
        # Create CUDA context and rasterize
        ctx = dr.RasterizeCudaContext()
        rast_out, _ = dr.rasterize(ctx, vertices, triangles, resolution=[64, 64])
        
        print("✅ Basic rendering test successful")
        print(f"   Output shape: {rast_out.shape}")
        return True
        
    except Exception as e:
        print(f"❌ Rendering test failed: {e}")
        return False

def main():
    """Main execution function"""
    print("🚀 nvdiffrast DLL Dependency Fix Tool")
    print("===================================")
    
    success_count = 0
    total_tests = 6
    
    # Phase 1: Environment setup
    if add_cuda_dll_directories():
        success_count += 1
    
    set_environment_variables()
    success_count += 1
    
    # Phase 2: Runtime checks
    if check_visual_cpp_runtime():
        success_count += 1
    
    if test_cuda_dlls():
        success_count += 1
    
    # Phase 3: nvdiffrast testing
    if test_nvdiffrast_basic():
        success_count += 1
        
        if test_nvdiffrast_contexts():
            success_count += 1
            
            # Bonus: rendering test
            if run_basic_rendering_test():
                print("\n🎉 COMPLETE SUCCESS!")
                print("nvdiffrast is fully functional with your RTX 4090!")
                print("\nYou can now use nvdiffrast for:")
                print("  - High-performance differentiable rendering")
                print("  - CUDA-accelerated rasterization") 
                print("  - Machine learning graphics applications")
                return True
    
    # Summary
    print(f"\n📊 Results: {success_count}/{total_tests} checks passed")
    
    if success_count >= 4:
        print("⚠️  Partial success - some functionality may work")
    else:
        print("❌ Multiple issues detected - manual troubleshooting needed")
        print("\nNext steps:")
        print("1. Install Visual C++ 2015-2022 Redistributable (x64)")
        print("2. Verify CUDA installation")
        print("3. Check Windows DLL search path configuration")
        print("4. Run with administrator privileges")
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)