#!/usr/bin/env python3
"""
Animation Video Creator
Converts nvdiffrast animation frames to MP4 video
"""

import os
import sys
import subprocess
import glob
from pathlib import Path

def find_ffmpeg():
    """Find ffmpeg executable on system"""
    # Common ffmpeg locations
    common_paths = [
        "ffmpeg",
        "ffmpeg.exe", 
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
    ]
    
    for path in common_paths:
        try:
            result = subprocess.run([path, "-version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return path
        except:
            continue
    
    return None

def create_video(input_pattern, output_file, framerate=30, quality="high"):
    """Create MP4 video from image sequence"""
    
    # Find ffmpeg
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        print("❌ ffmpeg not found. Please install ffmpeg:")
        print("   - Download from: https://ffmpeg.org/download.html")
        print("   - Or install via package manager")
        return False
    
    # Convert ffmpeg pattern to glob pattern for validation
    glob_pattern = input_pattern.replace("%03d", "*")
    input_files = glob.glob(glob_pattern)
    if not input_files:
        print(f"❌ No files found matching pattern: {glob_pattern}")
        return False
    
    print(f"📁 Found {len(input_files)} animation frames")
    
    # Quality settings
    quality_settings = {
        "low": ["-crf", "28", "-preset", "fast"],
        "medium": ["-crf", "23", "-preset", "medium"], 
        "high": ["-crf", "18", "-preset", "slow"],
        "lossless": ["-crf", "0", "-preset", "veryslow"]
    }
    
    # Build ffmpeg command
    cmd = [
        ffmpeg_path,
        "-framerate", str(framerate),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        *quality_settings.get(quality, quality_settings["high"]),
        "-y",  # Overwrite output file
        output_file
    ]
    
    print(f"🎬 Creating video: {output_file}")
    print(f"   Framerate: {framerate} fps")
    print(f"   Quality: {quality}")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ Video created successfully: {output_file}")
            
            # Show file size
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"   File size: {size_mb:.1f} MB")
            
            return True
        else:
            print(f"❌ ffmpeg failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ ffmpeg timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running ffmpeg: {e}")
        return False

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert animation frames to video")
    parser.add_argument("--input", default="advanced_anim_%03d.png", 
                       help="Input pattern (default: advanced_anim_%%03d.png)")
    parser.add_argument("--output", default="advanced_animation.mp4",
                       help="Output video file (default: advanced_animation.mp4)")
    parser.add_argument("--fps", type=int, default=30,
                       help="Framerate (default: 30)")
    parser.add_argument("--quality", choices=["low", "medium", "high", "lossless"],
                       default="high", help="Video quality (default: high)")
    
    args = parser.parse_args()
    
    print("🎬 nvdiffrast Animation Video Creator")
    print("====================================")
    
    success = create_video(args.input, args.output, args.fps, args.quality)
    
    if success:
        print("🎉 Video creation completed!")
    else:
        print("❌ Video creation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()