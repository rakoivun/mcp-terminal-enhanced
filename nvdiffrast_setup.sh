#!/bin/bash
# nvdiffrast_setup.sh - Complete environment setup for nvdiffrast on Windows
# Usage: source nvdiffrast_setup.sh

echo "🚀 Setting up nvdiffrast environment..."

# Phase 1: Base directories
export PROJECT_ROOT="/c/code/nvdiffrast-trials"
export PYTHON_ENV="$PROJECT_ROOT/nvdiffrast_py310"

# Phase 2: CUDA and Visual Studio paths
export CUDA_PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.8"
export CUDA_BIN="$CUDA_PATH/bin"
export CUDA_LIB="$CUDA_PATH/lib/x64"
export VS_PATH="/c/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build"

# Phase 3: Python and build tools paths
export PYTHON_BIN="$PYTHON_ENV/Scripts"
export PYTHON_EXE="$PYTHON_BIN/python.exe"

# Phase 4: Configure complete PATH
export PATH="$PYTHON_BIN:$CUDA_BIN:$CUDA_LIB:$PATH"

# Phase 5: PyTorch extension settings (prevent unnecessary recompilation)
export TORCH_EXTENSIONS_DIR="$HOME/.cache/torch_extensions"
export TORCH_CUDA_ARCH_LIST="8.9"  # RTX 4090 architecture

# Phase 6: Validation functions
check_tool() {
    local tool=$1
    local path=$2
    if [ -f "$path" ]; then
        echo "✅ $tool found: $path"
    else
        echo "❌ $tool missing: $path"
        return 1
    fi
}

echo ""
echo "🔍 Validating environment..."

# Check critical tools
check_tool "Python 3.10" "$PYTHON_EXE"
check_tool "Ninja" "$PYTHON_BIN/ninja.exe"
check_tool "NVCC" "$CUDA_BIN/nvcc.exe"

# Check if nvdiffrast plugins exist
PLUGIN_DIR="$HOME/.cache/torch_extensions/torch_extensions/Cache/py310_cu118"
if [ -d "$PLUGIN_DIR/nvdiffrast_plugin" ] && [ -d "$PLUGIN_DIR/nvdiffrast_plugin_gl" ]; then
    echo "✅ nvdiffrast plugins found in cache"
    echo "   CUDA: $(ls -lh "$PLUGIN_DIR/nvdiffrast_plugin/nvdiffrast_plugin.pyd" 2>/dev/null | awk '{print $5}')"
    echo "   OpenGL: $(ls -lh "$PLUGIN_DIR/nvdiffrast_plugin_gl/nvdiffrast_plugin_gl.pyd" 2>/dev/null | awk '{print $5}')"
else
    echo "⚠️  nvdiffrast plugins not found - will be compiled on first use"
fi

echo ""
echo "🧪 Testing nvdiffrast functionality..."

# Function to test nvdiffrast
test_nvdiffrast() {
    echo "📦 Testing basic import..."
    if "$PYTHON_EXE" -c "import nvdiffrast.torch as dr; print('✅ nvdiffrast import successful')" 2>/dev/null; then
        echo "✅ Import test passed"
        
        echo "🖥️  Testing CUDA context..."
        if "$PYTHON_EXE" -c "import nvdiffrast.torch as dr; ctx = dr.RasterizeCudaContext(); print('✅ CUDA context created successfully')" 2>/dev/null; then
            echo "🎉 SUCCESS: nvdiffrast CUDA is working!"
            return 0
        else
            echo "❌ CUDA context creation failed"
            echo "🔄 Attempting with DLL directory setup..."
            if "$PYTHON_EXE" -c "import os; os.add_dll_directory('$CUDA_BIN'); import nvdiffrast.torch as dr; ctx = dr.RasterizeCudaContext(); print('✅ CUDA context with DLL path')" 2>/dev/null; then
                echo "🎉 SUCCESS: nvdiffrast CUDA working with DLL path!"
                return 0
            else
                echo "❌ CUDA context still failing"
                return 1
            fi
        fi
    else
        echo "❌ Import test failed"
        return 1
    fi
}

# Run the test
if test_nvdiffrast; then
    echo ""
    echo "🎉 Environment setup complete! nvdiffrast is ready to use."
    echo "💡 To use nvdiffrast, run: $PYTHON_EXE your_script.py"
else
    echo ""
    echo "⚠️  Environment setup complete but nvdiffrast needs troubleshooting."
    echo "🔧 Try running Micro-Trial A for detailed diagnostics."
fi

echo ""
echo "📋 Environment Summary:"
echo "   Python: $PYTHON_EXE"
echo "   CUDA: $CUDA_BIN"
echo "   PATH configured with all necessary tools"
echo ""
echo "To use this environment: source $(pwd)/nvdiffrast_setup.sh"